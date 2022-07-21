import cv2
from math import atan2, radians

class decisions():
    def __init__(self, targeter, bodys, video, comms, debug) -> None:
        self.targeter = targeter
        self.bodys = bodys
        self.video = video
        self.comms = comms
        self.debug = debug

    def run(self):
        while True:
            # Get the frame
            _, frame = self.video.read()
            
            # Detect bodys and faces
            frame_bodys, box_ids = self.bodys.body_detection(frame)

            # Look for target
            target_id = self.targeter.latest_target(box_ids)
            if target_id != 0:
                for body in box_ids:
                    if body[4] == target_id:   # TODO make this not a for loop
                        x, y, w, h, id, faces = body

                    # calc radians
                    (frame_h, frame_w) = frame.shape[:2]
                    centre_x = (int(x+w/2))
                    centre_y = (int(y+h/2))
                    frame_centre_x = frame_w/2
                    frame_centre_y = frame_h/2
                    angle = atan2(frame_centre_y - centre_y, frame_centre_x - centre_x)

                    self.comms.write(angle,1)

                    if  "commandline" in self.debug:
                        print("target at: %f rad", angle)

                    if "show-frame" in self.debug:
                        # Rectangle target
                        cv2.rectangle(frame, (x-2, y-2), (x + w+4, y + h+4), (0, 0, 255), 3)
                        # Show vector
                        cv2.line(frame, (int(frame_centre_x), int(frame_centre_y)), (centre_x,centre_y), (255,0,0), 4) 
                        cv2.imshow('Video', frame_bodys)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break