import os
import cv2 as cv
import ImageManager as Im

class ObjectManager:
    def __init__(self):
        self.moments = None
        self.obj_center = None
        self.contours = None
        self.image_visual = None
        self.lst_axis = None
        self.max_axis = None
        #self.centroid()

    def centroid(self):#finds centroid of image selected by user
        self.contours, hierarchy = cv.findContours(self.image_visual, 
                                                mode= 1,
                                                method= 2)
        if not self.contours:
            print("no contours found")
            return 
        cnt = max(self.contours, key=cv.contourArea) #using first contour to calculate moments
        self.moments = cv.moments(cnt)
        M = self.moments
        
        #use moments (M) to calculate centroid (C)
        if M["m00"] != 0: #to avoid division by 0
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            self.obj_center = [cx, cy]

    def show_centroid(self): #finds second moments
         #load image
        self.image_visual = cv.imread("results/binary.jpg", cv.IMREAD_GRAYSCALE)
        if self.image_visual is None:
            print("No binary image found, run '1) Convert image' first \n")
            return
        
        #get centroid and moments
        self.centroid()
        if self.obj_center is None:
            print("No centroid or moments found")
            return
        C = self.obj_center

        render = cv.cvtColor(self.image_visual, cv.COLOR_GRAY2BGR)
        
        #draw centroid
        cv.circle(render, C,3, color=(0, 0, 255), thickness=1)
        cv.putText(render, 
                f"Centroid: ({C[0]}, {C[1]})", 
                (C[0]+4, C[1]), 
                cv.FONT_HERSHEY_PLAIN, 
                .3,
                (0,0,255),
                1,
                bottomLeftOrigin=False)
        
        cv.imshow("Centroid of object", render)
        print("Press 'Enter' to close image")
        cv.waitKey(0)
        cv.destroyAllWindows()


    def show_axis(self):
        cmx = self.moments
        
        #("m20") - (self.centroid[0] * self.moments.get("m10"))
        #cmy = self.moments.get("m02") - (self.centroid[1] * self.moments.get("m01"))
        #mcm = self.moments.get("m11") - (self.centroid[0] * self.moments.get("m01"))
        print((cmx), "+")


        '''print("\nMoments: ")
        for key, value in self.moments.items():
            print(f"{key}: {value}")'''

    

    