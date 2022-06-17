import cv2
import sys
import time

from detection.tracker import EuclideanDistTracker as Edt

class body_and_faces:
    def __init__(self):     
        self.body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.tracker = Edt()
        self.box_ids = []
        
        self.now = 0
        self.then = time.time()

    def body_detection(self, frame, scale=100): #change form video device to just the from..  state machine should control timing

        self.frame = frame
        scale_percent = scale # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
  
        # resize image
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        bodys = []
        bodys = self.body_cascade.detectMultiScale(gray)

        # Detection
        detections = []
        for (x, y, w, h) in bodys:
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            detections.append([x,y,w,h])
            self.box_ids = self.tracker.update(detections)

            #this should be for the target only
            test = self.box_ids[len(self.box_ids)-1]
            centre_x = (int(test[0]+test[2]/2))
            
            centre_y = (int(test[1]+test[3]/2))
            cv2.line(self.frame, (200,200), (centre_x,centre_y), (255,0,0), 4) 

        # Frame
        j=0
        for box_id in self.box_ids:
            x, y, w, h, id, _ = box_id
            cv2.putText(self.frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
            roi_gray = gray[y:y+h, x:x+w]

            # Find Face
            faces = self.face_cascade.detectMultiScale(roi_gray)
            for (x2,y2,w2,h2) in faces:
                face_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2)*0.25))
                cv2.circle(self.frame, face_center, radius, (255, 0, 0 ), 1)
                self.box_ids[j][5] +=1 
                if self.box_ids[j][5] >= 2:
                    break
            j+=1

        #box_ids has x, y, width, height, id, face count!. Time to find the target
        #This is targeting and should be handled seperatly
        target = [0,0,0,0,0]
        for ppl in self.box_ids:
            x, y, w, h, id, faces = ppl
            if faces ==1:
                break
        if target[4] !=0:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

        #self.frames per second
        self.now = time.time()
        total = self.now - self.then
        self.then = self.now
        cv2.putText(self.frame, str(int(1/total)), (20, 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        return self.frame, self.box_ids


if __name__ == "__main__":
    
    bodys = body_and_faces()
    video = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    video.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    while True:
        ret, frame = video.read() # remove this as just a frame ^^
        frame_bodys, box_ids = bodys.body_detection(frame)
        cv2.imshow('Video', frame_bodys)
        print(box_ids)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
