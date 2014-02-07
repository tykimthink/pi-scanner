#!/usr/bin/python3
"""
Provides access to the camera. This level of abstraction means that as long as the rest of the 
program only uses this interface we can switch between the raspberry pi camera module and a
USB webcam.
"""
try:
    import picamera
except:
    print("[ERROR] Could not import the picamera module!")

cam_defaults = {"resolution": (840, 640),
"rotation": 180}

class CameraInterface:

    def __init__(self):
        try:
            self.cam = picamera.PiCamera()
            self.configure_camera(cam_defaults)
            print("Initialized camera interface!")
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
        self.cam.capture("web/cam_latest.jpg")


if(__name__=="__main__"):
    # script is the main module so call main()
    pass
else:
    # Open a connection to the camera!
    pass