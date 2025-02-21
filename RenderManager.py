'''Handles vizualizing/displaying image and geometric properties'''

import numpy as np
import cv2 as cv
import math


class RenderManager:
    def __init__(self, object_manager):
        self.obj_manager = object_manager

        self.components = np.load('results/components.npy', allow_pickle=True) #load components from matrix
        self.threshold_jpg = cv.imread('results/binary.jpg', cv.IMREAD_GRAYSCALE) #load thresholded image
        if self.threshold_jpg is None:
            print("no .jpg found")
        
        #load color matrix
        try:
            self.color_mtx = np.load('results/color.npy')
        except FileNotFoundError:
            print("no color.npy found")
            self.color_mtx = None

    def show_binary(self):#display binary threshold jpg
        if self.threshold_jpg is None:
            print("No binary image to show")
            return
        cv.imshow("Binary image", self.threshold_jpg)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def show_color(self): #display color image from npy
        if self.color_mtx is None:
            print("No color matrix")
            return
        
        #convert to displayable image format
        color_img = self.color_mtx.astype(np.uint8)
        cv.imshow("Color image from matrix", color_img)
        cv.waitKey(0)
        cv.destroyAllWindows()


    def show_centroid(self):
        components = np.load('results/components.npy', allow_pickle=True) #load components from matrix
        render = cv.cvtColor(self.threshold_jpg, cv.COLOR_GRAY2BGR)
        
        for component in components: #get centroids
            centroid = component['centroid']
            if centroid is None or len(centroid) != 2:
                print("Invalid centroid data")
                continue

            #draw centroids on image
            x, y = centroid
            cv.circle(img= render,
                      center= (x, y),
                      radius= 3, 
                      color=(0, 0, 255), 
                      thickness=1)
            cv.putText(img= render, 
                    text= f"Centroid: ({x}, {y})", 
                    org= (x + 5, y - 5), #offset text for visibility
                    fontFace= cv.FONT_HERSHEY_PLAIN, 
                    fontScale= .3,
                    color= (0,0,255),
                    lineType= 1)
        
        valid_objects = [c for c in components if c['centroid'] is not None]
        print(f"Objects detected: {len(valid_objects)/3}")
        
        cv.imshow("Centroids", render)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def show_axis(self):
        #load components from matrix
        components = np.load('results/components.npy', allow_pickle=True)
        render = cv.cvtColor(self.threshold_jpg, cv.COLOR_GRAY2BGR)

        for component in components:
            centroid = component['centroid']
            major_axis = component['major_axis']
            minor_axis = component['minor_axis']
            angle = component['angle']
            if centroid is None:
                continue

            #draw centroids on image
            cx, cy = centroid
            cv.circle(render, (cx, cy), 3, color=(0, 0, 255), thickness=1)

            # Draw major axis
            half_major = major_axis / 2
            x1_major = int(cx + half_major * math.cos(angle))
            y1_major = int(cy + half_major * math.sin(angle))
            x2_major = int(cx - half_major * math.cos(angle))
            y2_major = int(cy - half_major * math.sin(angle))
            cv.line(render, (x1_major, y1_major), (x2_major, y2_major), color= (0, 0, 255), thickness=2)

            # Draw minor axis
            half_minor = minor_axis / 2
            x1_minor = int(cx + half_minor * (-math.sin(angle)))
            y1_minor = int(cy + half_minor * math.cos(angle))
            x2_minor = int(cx - half_minor * (-math.sin(angle)))
            y2_minor = int(cy - half_minor * math.cos(angle))
            cv.line(render, (x1_minor, y1_minor), (x2_minor, y2_minor), color= (255, 0, 0), thickness=1)

        # Show result
        cv.imshow("Axes", render)
        cv.waitKey(0)
        cv.destroyAllWindows()
        