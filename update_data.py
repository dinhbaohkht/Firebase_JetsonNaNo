import cv2
import os
import pyrebase

# Cấu hình Firebase
config = {
    "apiKey": "your-api-key",
    "authDomain": "your-auth-domain.firebaseapp.com",
    "databaseURL": "https://your-database-url.firebaseio.com/",
    "projectId": "your-project-id",
    "storageBucket": "your-storage-bucket.appspot.com",
    "messagingSenderId": "your-messaging-sender-id",
    "appId": "your-app-id",
    "measurementId": "your-measurement-id",
    "serviceAccount": "path/to/serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def updateCrossLight(img, x0, y0, track_id, time_stamp):
    v_counter.append(track_id)
    cv2.rectangle(img, (x0, y0 - 10), (x0 + 10, y0), (0, 0, 255), -1)
    
    saveDir = "./law_img"
    file_name = "vuot_den_{}".format(time_stamp)
    image_path = "{}/{}.jpg".format(saveDir, file_name)
    cv2.imwrite(image_path, img)
    
    # Đặt ảnh lên Firebase Storage
    storage.child("images/{}".format(file_name)).put(image_path)
    
    # Lấy URL của ảnh trên Firebase Storage
    image_url = storage.child("images/{}".format(file_name)).get_url(None)
    
    # Gửi dữ liệu lên Firebase Realtime Database
    db = firebase.database()
    data = {
        "track_id": track_id,
        "time_stamp": time_stamp,
        "image_url": image_url,
        "violation":"vượt đèn đỏ"
        
    }
    db.child('violation').push(data)
    
    


