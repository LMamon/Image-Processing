'''Handles vizualizing/displaying image and geometric properties'''

import numpy as np
import cv2 as cv


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
        render = self.threshold_jpg.copy()
        
        for component in components: #get centroids
            centroid = component['centroid']
            if centroid is None or len(centroid) != 2:
                print("Invalid centroid data")
                continue

            #draw centroids on image
            x, y = centroid
            cv.circle(render, (x, y), 3, color=(0, 0, 255), thickness=1)
            cv.putText(render, 
                    f"Centroid: ({x}, {y})", 
                    (x + 5, y - 5), #offset text for visibility
                    cv.FONT_HERSHEY_PLAIN, 
                    .3,
                    (0,0,255),
                    1)
        
        valid_objects = [c for c in components if c['centroid'] is not None]
        print(f"Objects detected: {len(valid_objects)}")
        
        cv.imshow("Centroids", render)
        cv.waitKey(0)
        cv.destroyAllWindows()
    