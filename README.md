# scarebear

Currently working on detection - haar_face.py
- make relyable
- find distance relyability
- make into class
- make a function return a distance to centre

# Currently working on:
- finishing inspo of body, face and eye detection with picam

# Final idea:
-----
Image process:
- find any movement
- find bodies
- find faces
- if faces find eyes
- if degub-image, show frame with date and boxes
- return array of bodies, faces and if the face has eyes, movement centre
-----
-----
Targeting:
- decide target logic
    - maybe after 1sec (a few frames) if no body move to movement
    - randomly move to bodies if no face
    - if face, freeze
    - if face with 2 eyes and taking up X frame, move fast and talk
- return centre to go to 
-----
-----
Movement:
- Maybe ardino nano via serial comand maybe not
- takes fast or slow movement bool
- receives direction (maybe a vector, maybe a deltax deltay expected)
- maybe needs a feedback loop to correct everything..  test this
-----