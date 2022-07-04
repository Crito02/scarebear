# scarebear

Currently working on detection arduino and serial messages.
Need to get back to look at direving angle in radians to target on screen
- make relyable
- find distance relyability
- make into class
- make a function return a distance to centre

# Currently working on:
- arduino servo driver
- serial connection to servo

# Final idea:
-----
Image process:
- TODO: find any movement
- find bodies
- if body, find face

- if degub-image, show frame with date and boxes
- return array of bodies, faces and if the face has eyes, movement centre
-----
-----
Targeting:
- decide target logic
    - maybe after 1sec (a few frames) if no body move to movement
    - randomly move to bodies if no face
    - if face, freeze
    - if face with taking up X frame, move fast and talk
- return centre if timeout..  real slowely
-----
-----
Movement:
- Arduino via serial
- Give arduino direction in radians and speed.. nice and simple
- Arduino feeds back current position of rotation and tilt
- All movement logic held by the pi, needs to stop movement or update direction/speed

-----
