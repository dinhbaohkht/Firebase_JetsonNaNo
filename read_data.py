import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore
import pyrebase
import json
import os
#set up
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#Read data

#geting a document with a known ID 

result = db.collection('cameraIp').document("7OcuvIELFU7IYGnlBN4S").get()

# if result.exists:
#     print(result.to_dict())
data = result.to_dict()

Ipcamera = data["Ipcamera"]
point_center1_begin = data["point_center1_begin"]
point_center1_end = data["point_center1_end"]
point_center2_begin = data["point_center2_begin"]
point_center2_end = data["point_center2_end"]

point_left1_begin = data["point_center1_begin"]
point_left1_end = data["point_left1_end"]
point_left2_begin = data["point_left2_begin"]
point_left2_end = data["point_left2_end"]

point_right1_begin = data["point_right1_begin"]
point_right1_end = data["point_right1_end"]
point_right2_begin = data["point_right2_begin"]
point_right2_end = data["point_right2_end"]

lane_center = point_center1_begin + point_center1_end
lane_left = point_left1_begin + point_left1_end
lane_right = point_right1_begin + point_right1_end

capture = data['Ipcamera']

print(lane_left)
print(lane_right)
print(lane_center)

config = {
    "capture": capture ,
    "detect_license": True ,
    "lane_center": lane_center, 
    "lane_left": lane_left,
    "lane_right": lane_right

}
# Chuyển đổi dữ liệu thành định dạng JSON
config_json = json.dumps(config, indent=4)

# Đường dẫn đến tệp config.json
config_file_path = 'config.json'

# Kiểm tra nếu tệp config.json đã tồn tại, thì xóa nó
if os.path.exists(config_file_path):
    os.remove(config_file_path)
    print("Đã xóa tệp config.json")

# Tạo một tệp mới và ghi dữ liệu JSON vào tệp đó
with open(config_file_path, 'w') as config_file:
    config_file.write(config_json)

print("Đã tạo và ghi dữ liệu vào tệp config.json")

#get all document in a collection 
'''docs = db.collection('cameraIP').get()
for doc in docs :
    print(doc.to_dict())'''

#query
'''docs = db.collection('cameraIP').where('district', "array_contains", "linkedin").get()
for doc in docs :
    print(doc.to_dict())'''
'''docs = db.collection('cameraIP').where('district', '==', 'Bắc Ninh').stream()
for doc in docs:
    print(doc.to_dict())
'''