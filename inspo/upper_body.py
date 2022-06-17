import cv2
import sys
import time
from tracker import EuclideanDistTracker as Edt

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

#video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

tracker = Edt()
box_ids = []
faces = []
now = 0
then = time.time()
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray)

    # Draw a rectangle around the faces
    detections = []

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        detections.append([x,y,w,h])
        box_ids = tracker.update(detections)

    for box_id in box_ids:
        x, y, w, h, id = box_id
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        i=0
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 1)
            i+=1
            if i >= 2:
                break

    #frames per second
    now = time.time()
    total = now - then
    then = now
    cv2.putText(frame, str(int(1/total)), (20, 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
