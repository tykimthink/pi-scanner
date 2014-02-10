#!/usr/bin/python2
"""
Contains the server component class for the application. It handles all web interface features
including client-side API calls.
"""
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import SimpleHTTPServer

from camera import CameraInterface
import Calibrate

apiPrefix = "/API/"
apiArgStringSep = "?"
apiArgStringDelim = "&"
apiClassFuncSep = "."

cam = CameraInterface()

class APIHandler(SimpleHTTPServer.SimpleHTTPRequestHandler, object):

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

            if(function == "saveLatestFrame"):
                result = cam.save_latest()
                if(result):
                    print("Updated latest frame!")
                    self.send_response(200)
                else:
                    self.send_response(500)

            elif(function == "getLatestFrame"):
                result = cam.capture()
                if(result != None):
                    print("Captured latest frame!")
                    self.send_response(200)
                    self.send_header("Content-type", "image/jpeg")
                    self.end_headers()
                    self.wfile.write(result)
                else:
                    self.send_response(500)
            elif(page == "Calibration"):
                if(function=="newBlank"):
                    newFile = Calibrate.newBlankFile()
                    print("Created new calibration file: "+newFile)
                    self.send_response(200)
                    self.send_header("Content-type", "text/text")
                    self.end_headers()
                    self.wfile.write(bytes(newFile))
                elif(function == "getAll"):
                    print("Fetching list of available config files...")
                    self.send_response(200)
                    self.send_header("Content-type", "text/text")
                    self.end_headers()
                    files = Calibrate.listCalibrationFiles()
                    for f in files:
                        self.wfile.write(bytes(f+","+files[f]+"\n"))
                elif(function == "LoadEl"):
                    print("Loading element from file...")
                    result = Calibrate.getElement(args["file"], args["el"])
                    self.send_response(200)
                    self.send_header("Content-type", "text/text")
                    self.end_headers()
                    self.wfile.write(bytes(result))


        else:
            super(APIHandler, self).do_GET()

class InterfaceServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def test():
    print("server.py testbench is running....")

if(__name__=="__main__"):
    # script is the main module so run the tests....
    test()
else:
    # the module has been imported so do nothing!
    pass