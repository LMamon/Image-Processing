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
        self.color_img = None
        self.color_mtx = None
        self.file_path = None

        self.gray_mtx = None
        
        self.binary_img = None
        self.binary_mtx = None
        self.binary_path = None
        
        os.makedirs(self.output, exist_ok=True)
        

    def get_img(self):#user gets color image and loaded to self.color_matrix
        root=tk.Tk()
        root.withdraw() #hide root window
        root.attributes("-topmost", True)
        
        #open file explorer
        types = [('JPEG', '*.png'),('JPEG','*.jpeg'), ('PDF','*.pdf'), ('TIFF', '*.tiff')]
        self.file_path = filedialog.askopenfilename(parent=root, title="Select an image", filetypes=types)
        if self.file_path is None:
            print("No image loaded")
        root.quit()
        #small window doesnt close for whatever reason
        
        if self.color_mtx is None:
            self.color_mtx = cv.imread(self.file_path) #sets self.color_img to image in file_path
            self.save_color_mtx()
            self.grayscale()
            if self.color_mtx is None:
                print("No color image")
    

    def save_color_mtx(self): #save color image matrix to results folder
        color_mtx_path = os.path.join(self.output, "color.npy")
        np.save((color_mtx_path), self.color_mtx)
        print(f'Color Matrix saved to: {color_mtx_path}')
    
    def load_color_mtx(self): #load color image matrix
        try:
            color_mtx_path = os.path.join(self.output, "color.npy")
            self.color_mtx = np.load(color_mtx_path)
        except FileNotFoundError:
            print(f'Color matix not found at: {color_mtx_path}')


    def save_binary_mtx(self): #save binary matrix to results folder
        binary_mtx_path = os.path.join(self.output, "binary.npy")
        if self.binary_mtx is None:
            print("No binary matrix to save")
            return
        np.save((binary_mtx_path), self.binary_mtx)
        print(f'Binary matrix saved to: {binary_mtx_path}')
    
    def load_binary_mtx(self): #load binary matrix
        try:
            binary_mtx_path = os.path.join(self.output, "binary.npy")
            self.binary_mtx = np.load(binary_mtx_path)
        except FileNotFoundError:
            print(f'Binary matix not found at: {binary_mtx_path}')
        

    def grayscale(self): #set.gray_mtx with greyscaled color image
        if self.color_mtx is None:
            try:
                self.load_color_mtx()
            except Exception:
                print("Loaded color matrix is empty")
                return
        self.gray_mtx = cv.cvtColor(self.color_mtx, cv.COLOR_BGR2GRAY)


    def convert(self): #convert grayscale image to binary image and save
        if self.gray_mtx is None:
            self.grayscale()
            if self.gray_mtx is None:
                print("No grayscale image to apply threshold to")
                return
        
        _,self.binary_mtx = cv.threshold(self.gray_mtx, 230,250, 0) #convert threshold to binary
        self.binary_mtx = cv.bitwise_not(self.binary_mtx) #invert image, shapes should be white

        if self.binary_mtx is None:
            print("Error generating binary image")
            return
        
        #create output path for binary_mtx
        self.binary_path = os.path.join(self.output, "binary.jpg")
        
        #write bianry image to output folder
        try:
            cv.imwrite(self.binary_path, self.binary_mtx)
            print(f'Binary image saved to: {self.binary_path}')            
        except Exception as e:
            print(f'Error saving image: {self.binary_path}. Error {e}')
            return
        self.save_binary_mtx()
        
