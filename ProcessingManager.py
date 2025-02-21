'''Handles linear and non-linear image filters, converting to fourier transforms'''

import os
import numpy as np
import cv2 as cv


#constructor
class ProcessingManager:
    def __init__(self, color_mtx= "results/color.npy", output= "processing-results"):
        self.color_mtx = color_mtx
        self.output = output

        if not os.path.exists(self.color_mtx):
            print(f"No such file: {self.color_mtx}")
            self.color_mtx = None
            
        else:
            self.color_mtx = np.load(self.color_mtx)
        
        os.makedirs(self.output, exist_ok=True)


    def save_processed(self, blurredimg, filename):
        save_path = os.path.join(self.output, filename)
        np.save(save_path, blurredimg)


    #gaussian blur, median blur, sharpening
    def gaussian(self, sigma):
        img_rgb = cv.cvtColor(self.color_mtx, cv.COLOR_BGR2RGB)
        g_blur = cv.GaussianBlur(img_rgb, (5, 5), sigma)
        self.save_processed(g_blur, "gaussian.npy")

    def median(self):
        img_rgb = cv.cvtColor(self.color_mtx, cv.COLOR_BGR2RGB)
        m_blur = cv.medianBlur(img_rgb, 5)
        self.save_processed(m_blur, "median.npy")
    
    def sharpen(self, blurred_img='processing-results/gaussian.npy', strength= .5): #unmasking
        #adjust strength and gaussian sigma, results may vary
        self.gaussian(5)
        blurry = np.load(blurred_img)
        sharpened = cv.addWeighted(self.color_mtx, 1.0 + strength, blurry, -strength, 0)
        self.save_processed(sharpened, "sharpened.npy")






