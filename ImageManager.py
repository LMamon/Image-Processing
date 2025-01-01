import os
import tkinter as tk
import cv2 as cv

from tkinter import filedialog

class ImageManager:
    def __init__(self):
        self.image = None
        self.file_path = None
        self.binary_img = None
        self.binary_path = None
        self.convert()

    def get_img(self):
        root=tk.Tk()
        root.withdraw() #hide root window
        root.attributes("-topmost", True)
        
        #open file explorer
        types = [('JPEG', '*.png'),('JPEG','*.jpeg'), ('PDF','*.pdf'), ('TIFF', '*.tiff')]
        self.file_path = filedialog.askopenfilename(parent=root, title="Select an image", filetypes=types)
        root.update()
        #small window doesnt close for whatever reason

        self.image = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE) #reads and grayscales image
        if self.image is None:
            print("No image loaded")
        
        
    #method to convert to binary with objects/shapes white
    def convert(self, output="results"): 
        ImageManager.get_img(self) #get image and path

        _,self.binary_img = cv.threshold(self.image,230, 255, 0) #binary threshold

        #invert image, shapes should be white
        self.binary_img = cv.bitwise_not(self.binary_img)

        #save binary image to results folder
        os.makedirs(output, exist_ok=True)
        self.binary_path = os.path.join(output,"binary.jpg")

        try:
            cv.imwrite(self.binary_path,self.binary_img)
        except Exception as e:
            print(f"Error saving image: {self.binary_path}. Error {e}")
            return None
        return
        
        
    def show(self):
        cv.imshow("Binary image",self.binary_img)