import sys
import cv2 
import imutils
from yoloDet import YoloTRT
import torch
import tracker
from datetime import datetime
from law import colorDetector, midPoint, intersect
from bytetrack.byte_tracker import BYTETracker
import csv
import cv2
import os
import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import firestore
# import datetime as firebaseDatetime
from firebase_admin import storage
import json 


tracker2 = BYTETracker()

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

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
licenplate = "38A3326"
local = "camera Máy Bảo"
violatedTime = datetime.now().strftime('%Y-%m-%d %H_%M_%S.%f')[:-2]
violation = 'sai làn đường'
videoName = violatedTime + " Sai làn đường " + licenplate +" "+ local

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

f= open('config.json')
datajson = json.load(f)
current = {}
previous = {}
t_counter1 = []
lane_left = datajson["lane_left"]
lane_center = datajson["lane_center"]
lane_right = datajson["lane_right"]
v_counter = []


def updateCrossLight(img, x0, y0, track_id, time_stamp):
    v_counter.append(track_id)
    cv2.rectangle(img, (x0, y0 - 10), (x0 + 10, y0), (0, 0, 255), -1)
    
    saveDir = "./law_img"
    file_name = "vuot_den_{}".format(time_stamp)
    image_path = "{}/{}.jpg".format(saveDir, file_name)
    cv2.imwrite(image_path, img)

    data = {
	    'licenplate':licenplate,
	    'local':local,
	    'time':violatedTime, 
	    'video_name':videoName, 
	    'violation':violation
            }
    db.collection('violation').add(data)
    firebaseVideoPath = "Video/" + videoName +'.mp4'
    storage.child(firebaseVideoPath).put("1.mp4","mp4")
	#
   
# use path for library and engine file
model = YoloTRT(library="yolov5/build/libmyplugins.so", engine="yolov5/build/yolov5s.engine", conf=0.5, yolo_ver="v5")
cap = cv2.VideoCapture("/home/ctarg_lab_1/Desktop/video_output.mp4")
#cap = cv2.VideoCapture("rtsp://admin:Admin@123@27.72.149.50:1554/profile3/media.smp") # open one video
torch.cuda.empty_cache()
time_list =[]
stt = 0
while True:
    box=[]
    classes = []
    score = []
    ret, frame = cap.read()
    if ret:
        pass
    else:
        break
    # 
    boxes, totalInference, infernceTime1, infernceTime2, infernceTime3 = model.Inference(frame)
    t_track = datetime.now()
    if len(boxes):
        boxes = tracker.update(boxes,frame)
       
    t_track = datetime.now() - t_track
    frame = tracker.draw_bboxes(frame, boxes, None)
    t_error = datetime.now()
    current_color = colorDetector(frame)
    time_stamp = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    for i in range(len(boxes)):
        box = boxes[i][:4]
        track_id = boxes[i][-1]
        cls = boxes[i][4]
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        current[track_id]  = midPoint(x0,y0,x1,y1)
        if track_id in previous:
            cv2.line(frame, previous[track_id], current[track_id], (0,255,0), 1)
            line_group0 = [lane_left, lane_center, lane_right]
            for element in line_group0:
                if len(element):
                    start_line = element[0],element[1]
                    end_line = element[2], element[3]
                    if intersect(previous[track_id],current[track_id], start_line, end_line):
                        print(intersect(previous[track_id],current[track_id], start_line, end_line))
                        if line_group0.index(element) == 1:
                            t_counter1.append(track_id)
                            """
                            if current_color != "red":
                                print("Fined")
                                updateCrossLight(frame, x0, y0, track_id, time_stamp)
                            """
                            print("Fined")
                            updateCrossLight(frame, x0, y0, track_id, time_stamp)
        previous[track_id] = current[track_id]
    #t_error = datetime.now() - t_error
    print("Total FPS: {} sec".format(1/totalInference))
    print("Total inferrence_time: {} sec".format(totalInference))
    print("Total FPS1: {} sec".format(1/infernceTime1))
    print("Total FPS2: {} sec".format(1/infernceTime2))
    print("Total FPS3: {} sec".format(1/infernceTime3))
    #time_list.append([stt,t, t_track, t_error])
    #stt = stt + 1
    torch.cuda.empty_cache()
    cv2.imshow("Output", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
       break
#    if stt > 50000:
#       break
#with open('yolov5_deepsort.csv','w',newline='') as f:
#    write = csv.writer(f)
#    write.writerow(['stt','detection time', 'track time', 'error time'])
#    write.writerows(time_list)
'''
time_list =[]
stt = 0
cap = cv2.VideoCapture("/home/ctarg_lab_1/Desktop/video_output.mp4")
while True:
    box=[]
    classes = []
    score = []
    ret, frame = cap.read()
    if ret:
        pass
    else:
        break
    boxes, t = model.Inference(frame)
    for i in range(len(boxes)):
        box.append([int(boxes[i][0]),int(boxes[i][1]),int(boxes[i][2]),int(boxes[i][3])])
        classes.append(boxes[i][4])
        score.append(boxes[i][5])
    t_track = datetime.now()
    if len(boxes):
        #boxes = tracker.update(boxes,frame)
        boxes = tracker2.update(box, score, classes)
    t_track = datetime.now()-t_track
    frame = tracker.draw_bboxes(frame, boxes, None)
    t_error = datetime.now()
    current_color = colorDetector(frame)
    time_stamp = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    for i in range(len(boxes)):
        box = boxes[i][:4]
        track_id = boxes[i][-1]
        cls = boxes[i][4]
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        current[track_id]  = midPoint(x0,y0,x1,y1)
        if track_id in previous:
            cv2.line(frame, previous[track_id], current[track_id], (0,255,0), 1)
            line_group0 = [lane_left, lane_center, lane_right]
            for element in line_group0:
                if len(element):
                    start_line = element[0],element[1]
                    end_line = element[2], element[3]
                    if intersect(previous[track_id],current[track_id], start_line, end_line):
                        print(intersect(previous[track_id],current[track_id], start_line, end_line))
                        if line_group0.index(element) == 1:
                            t_counter1.append(track_id)
                            if current_color != "red":
                                print("Fined")
                                updateCrossLight(frame, x0, y0, track_id, time_stamp)
        previous[track_id] = current[track_id]
 
#    t_error = datetime.now() - t_error
#    time_list.append([stt,t, t_track, t_error])
#    stt = stt + 1
#    torch.cuda.empty_cache()
    #cv2.imshow("Output", frame)
    #key = cv2.waitKey(1)
    #if key == ord('q'):
       #break
#    if stt > 50000:
#       break
with open('yolov5_bytetrack.csv','w',newline='') as f:
    write = csv.writer(f)
    write.writerow(['stt','detection time', 'track time', 'error time'])
    write.writerows(time_list)
cap.release()
cv2.destroyAllWindows()
'''
