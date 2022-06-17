from targeting.target import targeter
from detection.haar_body_then_face import body_and_faces

import cv2

if __name__ == "__main__":
    
    bodys = body_and_faces()
    video = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    tgt = targeter()
    while True:
        ret, frame = video.read() # remove this as just a frame ^^
        
        # Detect
        frame_bodys, box_ids = bodys.body_detection(frame)

        # Target
        
        target_id = tgt.body_no_face_then_latest(box_ids)
        if target_id != 0:
            for body in box_ids:
                if body[4] == target_id:
                    x, y, w, h, id, faces = body
                    print("target!!!!!!")
                    cv2.rectangle(frame, (x-2, y-2), (x + w+4, y + h+4), (0, 0, 255), 3)

        # Show frame
        cv2.imshow('Video', frame_bodys)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
