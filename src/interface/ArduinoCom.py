#!/usr/bin/python2
"""
Contains all classes and functions for communication with an arduino via
serial port.
"""

import serial
import serial.tools.list_ports

class ArduinoCom:
    """
    An instance of this class allows for communication with a single arduino on
    a /dev/ttyACMX port.
    """

    def __init__(self, port, baud):
        """
        Initialises the class.
        """
        self.port = port
        self.baud = baud
        self.connection = serial.Serial(self.port, self.baud, timeout = 2)

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

    def setServo(self, pos):
        """
        Moves the servo arm to the desired position pos. Pos should be an
        integer between 0 and 180 inclusive.
        """
        toWrite="GT"
        num = str(pos)
        while(len(num)<3):
            num="0"+num
        toWrite = toWrite + num+"_"
        print(toWrite)
        self.write(toWrite)


def test():

    print("Available ports:")
    for p in serial.tools.list_ports.comports():
        print("\t"+p[0]+"\t"+p[1]+"\t"+p[2])

    import time
    print("ArduinoCom.py testbench is running....")
    port = "/dev/ttyACM0"
    baud = 9600
    con = ArduinoCom(port, baud)
    print "Init: '" + con.readLine()+"'"
    if(con.handshake()):
        print("handshake successful!")
        time.sleep(2)
        print("Set servo: 0")
        con.setServo(0)
        time.sleep(2)
        print("Set servo: 90")
        con.setServo(90)
        time.sleep(2)
        print("Set servo: 180")
        con.setServo(180)
        time.sleep(2)
        print("Set servo: 45")
        con.setServo(45)
        time.sleep(2)
        print("Set servo: 135")
        con.setServo(135)
        time.sleep(2)
        print("Set servo: 0")
        con.setServo(0)
        time.sleep(2)
    else:
        print("handshake failed. Exiting....")
    print("Closing connection...")
    con.close()

if(__name__=="__main__"):
    # script is the main module so run the tests....
    test()
else:
    # the module has been imported so do nothing!
    pass