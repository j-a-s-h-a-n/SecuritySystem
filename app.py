import cv2
import time
import datetime
import os
from mailer import Email
from uploader import VideoUpload

drive = VideoUpload()
outlook = Email()


cam = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_fullbody.xml")
profile_cascade= cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_profileface.xml")

recording=False
detection_stopped_time = None
timer_started=False
seconds_to_record=5

captured=False

frame_size = (int(cam.get(3)),int(cam.get(4)))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')


images_folder='images/'
videos_folder='videos/'

def clearvideos():
    for f in os.listdir(videos_folder):
        os.remove(os.path.join(videos_folder, f))

def clearimages():
    for f in os.listdir(images_folder):
        os.remove(os.path.join(images_folder, f))

clearvideos()
clearimages()


while True:
    _ , frame = cam.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    bodies = body_cascade.detectMultiScale(gray,1.3,5)
    profiles = profile_cascade.detectMultiScale(gray,1.3,5)

    if len(bodies)+ len(faces)>0:
        if recording:
            timer_started=False
        else:
            recording=True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = (cv2.VideoWriter(f"{videos_folder}{current_time}.mp4",fourcc,10,frame_size),current_time)
    elif recording:
        if timer_started:
            if time.time()-detection_stopped_time>=seconds_to_record:
                recording=False
                timer_started=False
                out[0].release()
                drive.uploadFile(out[1]+'.mp4')
                clearvideos()
        else:
            timer_started=True
            detection_stopped_time=time.time()

    if recording:
        out[0].write(frame)

    if len(bodies)+ len(faces)+len(profiles)>0:
        if captured is False:
            captured_time=time.time()
            image_name=datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            cv2.imwrite(f'{images_folder}{image_name}.png',frame)
            outlook.sendEmail(image_name)
            clearimages()
            captured = True
    if captured and (time.time()-captured_time>=180):
        captured = False

    for (x,y,width,height) in faces:
        cv2.rectangle(frame,(x,y),(x+width,y+height),(0,255,0),5) #BGR #TOP of Rect Bottom left of Rect

    for (x, y, width, height) in bodies:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)  # BGR #TOP of Rect Bottom left of Rect

    for (x, y, width, height) in profiles:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)  # BGR #TOP of Rect Bottom left of Rect


    cv2.imshow('Security Camera',frame)


    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

for f in os.listdir(videos_folder):
    drive.uploadFile(f)
clearvideos()

