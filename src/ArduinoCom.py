#!/usr/bin/python2
"""
Contains all classes and functions for communication with an arduino via
serial port.
"""

import serial

class ArduinoCom:
    """
    An instance of this class allows for communication with a single arduino on
    a /dev/ttyACMX port.
    """

    def write(self, toSend):
        """
        Writes the supplied string to the serial port.
        """
        self.connection.write(bytes(toSend))


    def read(self, byteCount):
        """
        Reads the specified number of bytes from the serial port.
        """
        return self.connection.read(byteCount)

    def readLine(self):
        """ 
        Returns a single line of output from the port, terminated by \n.
        """
        return self.connection.readline()

    def close(self):
        """
        Closes the conenction
        """
        self.write("CLOSE_")
        self.connection.close()

    def __init__(self, port, baud):
        """
        Initialises the class.
        """
        self.port = port
        self.baud = baud
        self.connection = serial.Serial(self.port, self.baud, timeout = 2)

    def handshake(self):
        """
        Tries to establish a connection with the arduino with a simple handshake.
        Returns true if successful.
        """
        self.write("HELLO_")
        result = self.read(5)
        print("'"+result+"'")
        if(result == "HELLO"):
            return True
        else:
            return False


def test():
    print("ArduinoCom.py testbench is running....")
    port = "/dev/ttyACM0"
    baud = 9600
    con = ArduinoCom(port, baud)
    print "Init: '" + con.readLine()+"'"
    if(con.handshake()):
        print("handshake successful!")
    else:
        print("handshake failed. Exiting....")
    con.close()

if(__name__=="__main__"):
    # script is the main module so run the tests....
    test()
else:
    # the module has been imported so do nothing!
    pass