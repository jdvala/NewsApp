import os
import pyrebase
class FirebaseDB:
    def __init__(self):
        self.config = {
            "apiKey": os.environ['FIREBASE_API_KEY'],
            "authDomain": os.environ['FIREBASE_AUTHDOMAIN'],
            "databaseURL": os.environ['FIREBASE_DATABASEURL'],
            "projectID": os.environ['FIREBASE_PROJECTID'],
            "storageBucket": os.environ['FIREBASE_STORAGEBUCKET'],
        }
        self.firebase = pyrebase.initialize_app(self.config)
    
    def kvell_database(self):
        self.kvell_db = self.firebase.database()
        return self.kvell_db