#!/usr/bin/python2
"""
This file contains all of the required classes and functions for extracting a laser line
from a given image and processing it into a collection of points.
"""

import cv2
import numpy as np

class Point3:
    """
    Stores the XYZ values of a single point within the pointcloud
    """
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y;
        self.Z = z;

class Point2:
    """
    Stores the XY values of a single cartesian cordinate on a plane
    """
    def __init__(self, x, y):
        self.X = x
        self.Y = y;

class LineFinder:
    """
    This class is used to process the images containing laser lines into a collection of
    3d points or pointclound.
    """

    red_min = 10
    red_max = 350
    
    # contains a list of all points within the point cloud thus far generated.
    points = []

    def __init__(self):
        """
        Initialises the class.
        """
        self.points = []

    def clear():
        """
        Empties the point cloud.
        """
        self.points = []

    def get_hue(pixel):
        """
        takes a single pixel as its input and returns its hue value
        """
        rgbmax = max(pixel)
        rgbmin = min(pixel)
        blue, red, green = pixel
        if(rgbmax == red):
            return 0 + 43*(green - blue)/(rgbmax - rgbmin);
        elif(rgbmax == blue):
            return 85 + 43*(blue - red)/(rgbmax - rgbmin);
        else:
            return 171 + 43*(red - green)/(rgbmax - rgbmin);


    def process(self,img_in):
        """
        process the supplied image and adds the extracted points to the pointcloud.
        The image MUST be in the form of a cv2.Mat image.
        """
        row_count = 0
        for row in img_in:
            col_count = 0
            best_val = 0
            sel_col = -1
            for pix in row:
                hue = 10
                if(hue < 18 or hue > 138):
                    v = max(pix)
                    if(v>best_val):
                        best_val = v
                        sel_col = col_count
                col_count +=1
            if(sel_col>1):
                self.points.append(Point3(sel_col, row_count, -1))
                row[sel_col] = [0,255,0]
            row_count +=1

def test():
    """
    A simple test function for debugging the line finder module.
    """
    print("LineFinder Test Framework...\n")
    cam = cv2.VideoCapture(1)
    ret, frame = cam.read()

    proc = LineFinder()
    proc.process(frame)
    cv2.imshow("result", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if(__name__=="__main__"):
    # script is the main module so call test()
    test()
else:
    # the module has been imported so do nothing!
    pass