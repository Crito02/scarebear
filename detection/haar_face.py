import cv2
import sys
import time
from tracker import EuclideanDistTracker as Edt

class face_and_eyes:
    def __init__(self):     
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        self.tracker = Edt()
        self.box_ids = []
        
        self.now = 0
        self.then = time.time()

    def face_detection(self, video = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)): #change form video device to just the from..  state machine should control timing
        ret, frame = video.read() # remove this as just a frame ^^

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []
        faces = self.face_cascade.detectMultiScale(gray)
        detections = []
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            detections.append([x,y,w,h])
            self.box_ids = self.tracker.update(detections)

            #this should be for the target only
            test = self.box_ids[len(self.box_ids)-1]
            centre_x = (int(test[0]+test[2]/2))
            
            centre_y = (int(test[1]+test[3]/2))
            cv2.line(frame, (200,200), (centre_x,centre_y), (255,0,0), 4) 

        j=0
        for box_id in self.box_ids:
            x, y, w, h, id, _ = box_id
            cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            i=0
            for (x2,y2,w2,h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2)*0.25))
                cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 1)
                self.box_ids[j][5] +=1 
                if self.box_ids[j][5] >= 2:

                    break
            j+=1

        #box_ids has x, y, width, height, id, eye count!. Time to find the target
        #This is targeting and should be handled seperatly
        min_id = 999999999
        target = [0,0,0,0,0]
        for ppl in self.box_ids:
            x, y, w, h, id, eyes = ppl
            if eyes ==2 and min_id > id:
                target= [x, y, w, h, id]
                break
        if target[4] !=0:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        
        #frames per second
        self.now = time.time()
        total = self.now - self.then
        self.then = self.now
        cv2.putText(frame, str(int(1/total)), (20, 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Display the resulting frame Should be in main loop..  
        cv2.imshow('Video', frame)



if __name__ == "__main__":
    
    faces = face_and_eyes()
    while True:
        faces.face_detection()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
