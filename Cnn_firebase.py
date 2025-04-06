# import pyrebase

# config = {
#   "apiKey": "AIzaSyCKO9e-yaMoB-N0vb8LUDlxXL4yr_Svs-g",
#   "authDomain": "base-pro-b0a43.firebaseapp.com",
#   "databaseURL": "https://base-pro-b0a43-default-rtdb.firebaseio.com",
#   "projectId": "base-pro-b0a43",
#   "storageBucket": "base-pro-b0a43.appspot.com",
#   "messagingSenderId": "136225829076",
#   "appId": "1:136225829076:web:44088bd8f52a16beddcb41"
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# path_on_cloud = "images/image.png"
# path_on_local = "images_Take/image.png"

# storage.child(path_on_cloud).put(path_on_local)

import firebase_admin
from firebase_admin import credentials, firestore, storage

# Initialize Firebase Admin SDK
cred = credentials.Certificate("base-pro-b0a43-firebase-adminsdk-wrgmm-b647523251.json")
firebase_admin.initialize_app(cred, {"storageBucket": "base-pro-b0a43.appspot.com"})


def add_To_dataBase(cloud_path , local_path ,date ,name ):
 

    db = firestore.client()
    bucket = storage.bucket()
        
    # to Firebase Storage BUCKET FOR FIRESTORAGE
    # reference file reference
    blob = bucket.blob(cloud_path)
    blob.upload_from_filename(local_path)
    blob.make_public()


    # Store metadata in Firestore under "images" collection
    image_data = {
        "name": name,  
        "date": date,  
    }

    # Add document of name and date  to images collection "-"
    db.collection("images").add(image_data) 

