import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
config = {
    "apiKey": "AIzaSyAGEyO4ZN7gdrvuqY4Vd1SMMCUVmt6UDno",
    "authDomain": "aaaa-dbb41.firebaseapp.com",
    "databaseURL": "https://aaaa-dbb41-default-rtdb.firebaseio.com/",
    "projectId": "aaaa-dbb41",
    "storageBucket": "aaaa-dbb41.appspot.com",
    "messagingSenderId": "91945409393",
    "appId": "1:91945409393:web:1b17b16a8ad8d978bb74d0",
    "measurementId": "G-V374LENXFS",
    "serviceAccount":"serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
storage.child("2002_cam.jpg").put("2002.jpg")
#storage.download("2002_cam.jpg","2002_cam_new.jpg")
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

