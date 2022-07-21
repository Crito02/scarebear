import cv2
import argparse
from serial import SerialException

from targeting.target import BodyNoFaceThenLatest, LatestFace
from detection.haar_body_then_face import body_and_faces
from comms.arduino_serial import ArduinoComm
from brain import decisions


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', nargs='+', help='Choose level of debug.  eg -d show-freame commandline',
                        choices=['show-frame', 'commandline'])
    parser.add_argument('-v', '--video', help='Video device', default='/dev/video0')
    parser.add_argument('-t', '--targeter', help='Targeter decision', choices=['LatestFace', 'BodyNoFaceThenLatest'],
                        default='LatestFace')
    args = parser.parse_args()
    
    debug = []
    if args.debug:
        debug = args.debug
    print(debug)
    if args.video:
        video = cv2.VideoCapture(args.video, cv2.CAP_V4L)
        video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    
    if args.targeter == 'LatestFace':
        targeter = LatestFace()
    elif args.targeter == 'BodyNoFaceThenLatest':
        targeter = BodyNoFaceThenLatest()
    else:
        raise NotImplementedError()

    comms = ArduinoComm()
    bodys = body_and_faces()
    brain = decisions(targeter=targeter, bodys=bodys, video=video, comms=comms, debug=debug)


# When everything is done, release the capture
    cv2.video_capture.release()
    cv2.destroyAllWindows()
