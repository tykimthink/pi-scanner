#!/usr/bin/python2
"""
This file contains all of the required classes and functions for extracting a laser line
from a given image and processing it into a collection of points.
"""

import cv2
import numpy as np
import ConfigParser
import time
import os

from LineFinder import Point2

calibrationFilesRoot = "configFiles/"

class Point:
    """
    Stores the XYZ values of a single point within the pointcloud
    """
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y;
        self.Z = z;

class Calibrator:
    """
    Acts as a wrapper around a collection of measured reference points relating
    laser line X position to Z value (distance from camera).
    Also creates a function that will map an X value to a Z value using a polynomial
    created using a line of best fit for the calibration points.
    """

    def __init__(self):
        """
        Initialises the class.
        """
        self.points = []
        self.config = ConfigParser.ConfigParser()
        self.config.add_section("header")
        self.config.add_section("data")

        self.config.set("header", "name", "New Empty Config File")
        self.config.set("header", "notes", "A blank empty config file.")
        self.config.set("header", "camera", "default camera")
        self.config.set("header", "laser-camera-distance", 10)
        self.config.set("header", "laser-camera-angle", 45)
        self.config.set("header", "polynomial-coefficients", "1")

    def get_title(self):
        """
        Returns the title of the calibration file
        """
        return self.config.get("header", "name")

    def clear_points(self):
        """
        Removes all previously added calibration points.
        """
        self.points = []
        self.config.remove_section("data")
        self.config.add_section("data")

    def add_point(self, x, y):
        """
        Adds a new point to the list of calibration measurements
        """
        self.points.append(Point2(x,y))
        self.config.set("data", str(x), y)

    def save_to(self, path):
        """
        Saves the config file to the supplied file path.
        """
        with open(path, 'wb') as configfile:
            self.config.write(configfile)

    def load_from(self, path):
        """
        Loads a config from the specified file path.
        """
        self.config.read(path)


def newBlankFile():
    """
    Creates a new blank calibration file. Returns the name of the newly created file.
    """
    c = Calibrator()
    name = str(time.time())
    c.save_to(calibrationFilesRoot+name+".calib.txt")
    return name

def listCalibrationFiles():
    """
    Returns a list of all previously created calibration files in the form
    [filename, title]
    """
    toReturn = {}
    for file in os.listdir(calibrationFilesRoot):
        if(file.endswith(".calib.txt")):
            print(file)
            c = Calibrator()
            c.load_from(calibrationFilesRoot+file)
            toReturn[file.replace(".calib.txt","")] = c.get_title()
    return toReturn

def getElement(fileName, element):
    """
    Returns a string containing the calibration file information. The element determines
    the section to grame. This can be any sub section from the HEAD or if it is "data" then
    the entire data section will be returned as a csv file.
    """
    c = Calibrator()
    c.load_from(calibrationFilesRoot+fileName+".calib.txt")
    tr = ""
    if(element == "data"):
        for i in c.config.items("data"):
            tr += i[0]+","+i[1]+"\n"
    else:
        tr = str(c.config.get("header", element))
    return tr

def test():
    """
    A simple test function for debugging the line finder module.
    """
    print("calibrate Test Framework...\n")
    c = Calibrator()
    c.add_point(10, 15)
    c.add_point(15, 35)
    c.add_point(22, 55)
    c.add_point(27, 79)
    c.add_point(35, 90)
    c.save_to(calibrationFilesRoot+"test_save.calib.txt")
    print(listCalibrationFiles())

if(__name__=="__main__"):
    # script is the main module so call test()
    test()
else:
    # the module has been imported so do nothing!
    pass