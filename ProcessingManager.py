'''Handles linear, non-linear image filters, and conversion to fourier transform'''

import os
import numpy as np
import cv2 as cv 

#constructor
class ProcessingManager:
    def __init__(self, color_mtx= "object-results/color.npy", output= "processing-results"):
        self.color_mtx = color_mtx
        self.output = output

        if not os.path.exists(self.color_mtx):
            print(f"No such file: {self.color_mtx}")
            self.color_mtx = None
            
        else:
            self.color_mtx = np.load(self.color_mtx)
            self.color_img = self.get_color()
        
        os.makedirs(self.output, exist_ok=True)


    def save_processed(self, new_img, filename):
        save_path = os.path.join(self.output, filename)
        np.save(save_path, new_img)

    def get_color(self):
        jpg = os.path.join('object-results', 'binary.jpg')
        color_img = cv.imread(jpg, cv.IMREAD_COLOR)

        #convert img to 3channel
        if len(color_img.shape) == 2 or (len(color_img.shape) == 3 and color_img.shape[2] == 1):
            color_img = cv.cvtColor(color_img, cv.COLOR_GRAY2RGB)

        return color_img

    #gaussian blur, median blur, sharpening
    def gaussian(self, sigma):
        img = self.color_mtx
        g_blur = cv.GaussianBlur(img, (5, 5), sigma)
        self.save_processed(g_blur, "gaussian.npy")

    def median(self):
        img = self.color_mtx
        m_blur = cv.medianBlur(img, 5)
        self.save_processed(m_blur, "median.npy")
    
    def sharpen(self, blurred_img='processing-results/gaussian.npy', strength= .5): #unmasking
        #adjust strength and gaussian sigma, results may vary
        self.gaussian(5)
        blurry = np.load(blurred_img)
        sharpened = cv.addWeighted(self.color_mtx, 1.0 + strength, blurry, -strength, 0)
        self.save_processed(sharpened, "sharpened.npy")

    #fourier transforms using opencv
    def opencvFT(self):
        img = cv.cvtColor(self.color_img, cv.COLOR_BGR2GRAY)

        img = img.astype(np.float32)

        dft = cv.dft(img, flags= cv.DFT_COMPLEX_OUTPUT) 
        dft_shift = np.fft.fftshift(dft)

        magnitude = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
        self.save_processed(magnitude, 'magnitude.npy')






