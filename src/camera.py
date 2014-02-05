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

# this variable stores the single picamera object in the program. The rest of this file simply
# contains various functions for accessing and manippulating it.
_cam = None

def open_camera():
    """
    Opens a connection to the raspberry pi camera module. Must always be called before any
    camera data can be accessed or processed.
    """
    try:
        _cam = picamera.PiCamera()
        return True
    except:
        return "ERROR: " + sys.exc_info()[0]

def configure_camera(confgDict):
    """
    Used to set the camera settings. Takes a single dictionary of key value pairs. Each key
    MUST correspond exactly to a property the PiCamera _cam object possesses and that can
    be retrieved through a getattribute call. The corresponding value should be of the correct
    type to allow it to be set.
    """
    for key, value in confgDict.iteritems():
        setattr(_cam, key, value)

def get_property(prop):
    """
    Returns the value of a PiCamera attribute. The name of the attribute must be supplied
    in prop
    """
    return getattr(_cam, prop)

def set_property(prop, val):
    """
    Sets the value of a PiCamera attribute. The name of the attribute must be supplied
    in prop. Works as a single property version of configure_camera
    """
    return setattr(_cam, prop, val)


def test():
    print("camera.py | testbench running\n")
    testConfigDict = {"meter_mode" : "matrix", "resoloution": (640, 480)}
    configure_camera(testConfigDict)

if(__name__=="__main__"):
    # script is the main module so call main()
    test()
else:
    # the module has been imported so do nothing!
    pass