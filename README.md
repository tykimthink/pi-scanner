Raspberry PI Laser Scanner - PIScan
===============================================================================

This project aims to create a functioning laser scanner that will run on a
raspberry pi and arduino board. It will use a web interface powered by python
along with the raspberry pi camera module and an arduino (for IO interfacing)
to gather a series of images of the subject and then create a point cloud of
the object for display on the PI's HDMI display.

### ToDo list ###
-------------------------------------------------------------------------------
1. Implement a class for extracting the laser line from a camera image
2. Implement a callibration class that takes a selection of 2d vector and
returns a polynomial function describing a best fit line for the measured
distance data.



### Materials and Components ###
-------------------------------------------------------------------------------
- Raspberry PI with Raspbian installed
    - picamera python library
    - opencv with python support enabled.
    - network connection for the pi for the control interface.
- Arduino Uno
    - Servo and Line Laser pair
