import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from google.oauth2 import service_account
from datetime import datetime

class Firebase:
    def __init__(self, json_credentials_path) -> None:
        self.cred = credentials.Certificate(json_credentials_path)
        self.app = firebase_admin.initialize_app(self.cred)
        # ✅ Google Auth Credentials for Firestore
        google_cred = service_account.Credentials.from_service_account_file(json_credentials_path)
        # ✅ Now initialize Firestore with Google credentials
        self.db = firestore.Client(credentials=google_cred)

    ######### USER FUNCTIONS ##########
    def register_user(self, user_info):
        try:
            print(user_info)
            user_id = user_info["uid"]
            print('user_id')
            if not user_id:
                return {}, False, "Missing 'uid' in user_info"
            
            now = datetime.now()

            # Add defaults if missing
            default_data = {
                "email": user_info.get("email", ""),
                "username": user_info.get("username", ""),
                "full_name": user_info.get("full_name", ""),
                "bio": user_info.get("bio", ""),
                "profile_picture": user_info.get("profile_picture", ""),
                "created_at": now,
                "last_active": now,
                "followers": [],
                "following": [],
                "is_private": user_info.get('is_private', ''), # public or private
                "friends": [],
                "friend_requests": [],
                "follow_requests": [],
                "location": user_info.get("location", {}),
                "is_online": True,
                "uid": user_id
            }
            self.db.collection("users").document(user_id).set(default_data)
            return default_data, True, ""

        except Exception as e:
            return {}, False, str(e)

    def get_user(self, user_id):
        try:
            # 1: Retrieve the document from firestore
            doc = self.db.collection("users").document(user_id).get()
            # 2: Return the document as dictionary
            if doc.exists:
                return doc.to_dict(), True, ""
            else:
                return {}, False, "User not found"
        except Exception as e:
            return {}, False, str(e)

    def delete_user(self, user_id):
        try:
            self.db.collection("users").document(user_id).delete()
            return True, ""
        except Exception as e:
            return False, str(e)

    def update_user(self, user_id, user_updates):
        try:
            self.db.collection("users").document(user_id).update(user_updates)
            doc = self.db.collection("users").document(user_id).get()
            return doc.to_dict(), True, ""
        except Exception as e:
            return {}, False, str(e)
        
    
    ######### FOLLOWER/FRIEND FUNCTIONS ##########
    def follow_user(self, follower_id, target_user_id):
        try:
            # Add follower_id to the target user's followers list
            self.db.collection("users").document(target_user_id).update({
                "followers": firestore.ArrayUnion([follower_id])
            })

            # Add target_user_id to the follower's following list
            self.db.collection("users").document(follower_id).update({
                "following": firestore.ArrayUnion([target_user_id])
            })
            return True, "Successfully followed"
        except Exception as e:
            return False, str(e)

    def request_follow(self, follower_id, target_user_id):
        try:
            if follower_id == target_user_id:
                return False, "Cannot follow yourself"

            target_doc = self.db.collection("users").document(target_user_id).get()
            if not target_doc.exists:
                return False, "Target user does not exist"

            target_info = target_doc.to_dict()
            is_private = target_info['is_private']

            if is_private:
                # Add to follow_requests
                self.db.collection("users").document(target_user_id).update({
                    "follow_requests": firestore.ArrayUnion([follower_id])
                })
                return True, "Follow request sent"
            else:
                # Auto-follow
                success, message = self.follow_user(follower_id, target_user_id)
                return success, message
        except Exception as e:
            return False, str(e)

    def approve_follow_request(self, target_user_id, follower_id):
        try:
            self.db.collection("users").document(target_user_id).update({
                "follow_requests": firestore.ArrayRemove([follower_id]),
                "followers": firestore.ArrayUnion([follower_id])
            })
            self.db.collection("users").document(follower_id).update({
                "following": firestore.ArrayUnion([target_user_id])
            })
            return True, ""
        except Exception as e:
            return False, str(e)

    def reject_follow_request(self, target_user_id, follower_id):
        try:
            self.db.collection("users").document(target_user_id).update({
                "follow_requests": firestore.ArrayRemove([follower_id])
            })
            return True, ""
        except Exception as e:
            return False, str(e)

    def get_pending_follow_requests(self, user_id):
        try:
            doc = self.db.collection("users").document(user_id).get()
            if doc.exists:
                user_info = doc.to_dict()
                return user_info['follow_requests'], True, "Follow requests successfully retrieved"
            return [], False, "User not found"
        except Exception as e:
            return [], False, str(e)

        
    

    
firebase_manager = Firebase('./login-example-cf97f-firebase-adminsdk-fbsvc-61ea023a82.json')