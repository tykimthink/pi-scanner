#!/usr/bin/python3
"""
Contains the server component class for the application. It handles all web interface features
including client-side API calls.
"""

import http.server
from socketserver import ThreadingMixIn
import threading

import picamera

from camera import CameraInterface

apiPrefix = "/API/"
apiArgStringSep = "?"
apiArgStringDelim = "&"
apiClassFuncSep = "."

cam = CameraInterface()

class APIHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if(self.path.startswith(apiPrefix)):
            # All API request calls are handled and parsed within this function.
            # They are then passed onto the appropriate handler function.
            args = {}
            function = self.path.replace(apiPrefix, "").split(apiArgStringSep)[0]
            page = "self"
            if(apiClassFuncSep in function):
                page = function.split(apiClassFuncSep)[0]
                function = function.split(apiClassFuncSep)[1]
            if(apiArgStringSep in self.path):
                argString = self.path.split("?")[1]
                for kvp in argString.split("&"):
                    key = kvp.split("=")[0]
                    value = kvp.split("=")[1]
                    args[key] = value
                    print(key+":\t"+value)
            print("Page: \t"+page)
            print("Function:\t"+function)

            if(function == "getLatestFrame"):
                print("Updated latest frame!")
                cam.save_latest()

        else:
            super().do_GET()

class InterfaceServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""

def test():
    print("server.py testbench is running....")

if(__name__=="__main__"):
    # script is the main module so run the tests....
    test()
else:
    # the module has been imported so do nothing!
    pass