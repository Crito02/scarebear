from math import atan2, radians
from targeting.target import targeter
from detection.haar_body_then_face import body_and_faces
from comms.arduino_serial import ArduinoComm
import cv2


if __name__ == "__main__":
    
    bodys = body_and_faces()
    video = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    tgt = targeter()
    comm = ArduinoComm()

    while True:
        ret, frame = video.read() # remove this as just a frame ^^
        
        # Detect
        frame_bodys, box_ids = bodys.body_detection(frame)

        # Target
        target_id = tgt.latest_face(box_ids)        
        # target_id = tgt.body_no_face_then_latest(box_ids)
        if target_id != 0:
            for body in box_ids:
                if body[4] == target_id:   # TODO make this not a for loop
                    x, y, w, h, id, faces = body

                print("target!!!!!!")
                # Rectangle target
                cv2.rectangle(frame, (x-2, y-2), (x + w+4, y + h+4), (0, 0, 255), 3)

                # Show vector
                (frame_h, frame_w) = frame.shape[:2]
                centre_x = (int(x+w/2))
                centre_y = (int(y+h/2))
                frame_centre_x = frame_w/2
                frame_centre_y = frame_h/2
                cv2.line(frame, (int(frame_centre_x), int(frame_centre_y)), (centre_x,centre_y), (255,0,0), 4) 
                
                # calc radians
                angle = atan2(frame_centre_y - centre_y, frame_centre_x - centre_x)
                #angle = radians(angle)
                print(angle)
                comm.write(angle,1)
                break 
            
        # Show frame
        #cv2.imshow('Video', frame_bodys)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture
    cv2.video_capture.release()
    cv2.destroyAllWindows()
