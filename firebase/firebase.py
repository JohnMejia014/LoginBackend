import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore

class Firebase:
    def __init__(self, json_credentials_path) -> None:
        self.cred = credentials.Certificate(json_credentials_path)
        self.app = firebase_admin.initialize_app(self.cred)
        self.db = firestore.Client()

    def register_user(self, user_info):
        try:
            user_id = user_info.get("uid")
            if not user_id:
                return {}, False, "Missing 'uid' in user_info"
            
            self.db.collection("users").document(user_id).set(user_info)
            return user_info, True, ""
        except Exception as e:
            return {}, False, str(e)

    def get_user(self, user_id):
        try:
            doc = self.db.collection("users").document(user_id).get()
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

    def update_user(self, user_id, updates):
        try:
            self.db.collection("users").document(user_id).update(updates)
            doc = self.db.collection("users").document(user_id).get()
            return doc.to_dict(), True, ""
        except Exception as e:
            return {}, False, str(e)

    


firebase_manager = Firebase('../login-example-cf97f-firebase-adminsdk-fbsvc-61ea023a82.json')