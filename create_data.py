import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import pyrebase
import datetime
#set up
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

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
#add document with auto ID
# data = {'licenplate':'38A3326','local':"camera Ha Tinh", 'video_name':"2023-08-16 14_20_22.56 Sai làn đường 38A3326 Cam Ha Tinh", 'violation':'sai lan đường'}
# db.collection('person').add(data)
licenplate = "38A3326"
local = "camera Máy Bảo"
violatedTime = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S.%f')[:-2]
violation = 'sai làn đường'
videoName = violatedTime + " Sai làn đường " + licenplate + " " + local


#set documents with known ID 
data = {
    'licenplate':licenplate,
    'local':local,
    'time':violatedTime, 
    'video_name':videoName, 
    'violation':violation
}

db.collection('violation').add(data)


firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
firebaseVideoPath = "Video/" + videoName +'.mp4'
storage.child(firebaseVideoPath).put("1.mp4","mp4")
#

