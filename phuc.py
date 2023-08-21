import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import pyrebase

config = {
   "apiKey": "AIzaSyBLKJzZT-it5evKo7Gt2R_v4mK9-5337xo",
   "authDomain": "web-thi-online-92393.firebaseapp.com",
   "databaseURL": "https://web-thi-online-92393-default-rtdb.firebaseio.com/",
   "projectId": "web-thi-online-92393",
   "storageBucket": "web-thi-online-92393.appspot.com",
   "messagingSenderId": "139904512267",
   "appId": "1:139904512267:web:240c23d5376ab18eb8720e",
   "measurementId": "G-J5GC4G5YKL",
   "serviceAccount": "serviceAccountkey.json",
}

cred = credentials.Certificate("serviceAccountkey.json")
firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
storage.child("1.mp4").put("1.mp4","mp4")