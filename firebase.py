import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import pyrebase

#set up
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#add documents with auto id 
data = {'name':'John Smith','age':40}
# db.collection('people').add(data)

#set document with known ID 
data = {'name':'John Smith','age':40}
db.collection('person').document('janedoe').set(data)