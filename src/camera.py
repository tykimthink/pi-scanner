#!/usr/bin/python2
"""
Provides access to the camera. This level of abstraction means that as long as the rest of the 
program only uses this interface we can switch between the raspberry pi camera module and a
USB webcam.
"""

import numpy

raspi_available = False
opencv_available = False

try:
    import picamera
    raspi_available = True
    print("Imported picamera module")
except:
    print("[ERROR] Could not import the picamera module!")
try:
    import cv2
    opencv_available = True
    print("Imported opencv module")
except:
    print("[ERROR] Could not import the opencv2 module!")

cam_defaults = {"resolution": (840, 640),
"rotation": 180}

class CameraInterface:

    def __init__(self):
        try:
            if(raspi_available):
                self.cam = picamera.PiCamera()
                self.configure_camera(cam_defaults)
                print("Initialized camera interface using picamera")
            elif(opencv_available):
                self.cam = cv2.VideoCapture(0)
                print("Initialized camera interface using opencv")
            else:
                print("[ERROR] No webcam interface opencv_available!")

        except:
            print("[ERROR] Could not initialize the camera interface!")

    def configure_camera(self, configDict):
        """
        Used to set the camera settings. Takes a single dictionary of key value pairs. Each key
        MUST correspond exactly to a property the PiCamera _cam object possesses and that can
        be retrieved through a getattribute call. The corresponding value should be of the correct
        type to allow it to be set.
        """
        for key in configDict:
            setattr(self.cam, key, configDict[key])
            print("Set '"+key+"' to "+str(configDict[key]))

    def get_property(self, prop):
        """
        Returns the value of a PiCamera attribute. The name of the attribute must be supplied
        in prop
        """
        return getattr(self.cam, prop)

    def set_property(self, prop, val):
        """
        Sets the value of a PiCamera attribute. The name of the attribute must be supplied
        in prop. Works as a single property version of configure_camera
        """
        return setattr(self.cam, prop, val)

    def save_latest(self):
        """
        Saves the latest frame taken to web/cam_latest.jpg
        """
        if(raspi_available):
            self.cam.capture("web/cam_latest.jpg")
            return True
        elif(opencv_available):
            ret, frame = self.cam.read()
            cv2.imwrite("web/cam_latest.jpg", frame)
            return ret
        else:
            print("[ERROR] No webcam interface opencv_available!")
            return False


    def capture(self):
        """
        Saves the latest frame taken a memory buffer for sending over a network.
        """

        tr = None
        if(raspi_available):
            self.cam.capture(stream, "jpeg")
            tr = io.BytesIO()
        elif(opencv_available):
            ret, frame = self.cam.read()
            if(ret):
                ret, val = cv2.imencode(".jpg", frame)
                tr = val
            else:
                return None
        else:
            print("[ERROR] No webcam interface opencv_available!")
            return None

        return numpy.array(tr).tostring()


if(__name__=="__main__"):
    # script is the main module so call main()
    pass
else:
    # Open a connection to the camera!
    pass