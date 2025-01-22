'''Handles all image-related operations, such as loading, preprocessing, 
    and storing images.'''

import os

import numpy as np
import tkinter as tk
import cv2 as cv
from tkinter import filedialog

class ImageManager: 
    def __init__(self, output="results"):
        self.output = output
        self.file_path = None

        self.color_mtx = None
        self.gray_mtx = None
        self.binary_mtx = None
        
        os.makedirs(self.output, exist_ok=True)
        
    def convert_to_gray(self): #convert color mtx to grayscale
        self.gray_mtx = cv.cvtColor(self.color_mtx, cv.COLOR_BGR2GRAY)

    def convert_to_binary(self): #convert grayscale to binary using thresholding and invert so objects are white
        _, self.binary_mtx = cv.threshold(self.gray_mtx, 190, 250, cv.THRESH_BINARY_INV)
        if self.binary_mtx is None:
            print("Error converting grayscale image")
    
    def save_color_mtx(self): #save color mtx to results for optional visualization 
        color_path = os.path.join(self.output, "color.npy")
        np.save(color_path, self.color_mtx)
    
    def save_binary(self):
        if self.binary_mtx is None:
            print("Binary image not saved")
            return
        binary_path = os.path.join(self.output, "binary.npy")
        np.save(binary_path, self.binary_mtx)
        
        jpg_path = os.path.join(self.output, "binary.jpg")
        cv.imwrite(jpg_path, self.binary_mtx)

        print(f"Saved binary image to: {jpg_path}")
        print(f"Saved binary array to: {binary_path}")
    
    def get_image(self): #user picks image to use
        root= tk.Tk()
        root.withdraw() #hide root window
        root.attributes("-topmost", True)

        filetypes = [('JPEG', '*.png'),('JPEG','*.jpeg'), ('PDF','*.pdf'), ('TIFF', '*.tiff')]
        self.file_path = filedialog.askopenfilename(parent=root, title="Select an image", filetypes=filetypes)
        if not self.file_path:
            print("No image loaded")
            return
        root.quit() #small window doesnt close for some reason

        self.color_mtx = cv.imread(self.file_path, cv.IMREAD_ANYCOLOR)
        if self.color_mtx is None:
            print("Failed to load color image")
            return

        self.save_color_mtx()
        self.convert_to_gray()
        self.convert_to_binary()
        self.save_binary()
