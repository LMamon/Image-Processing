'''Focuses on geometric analysis and computations, like finding contours, 
    moments, centroids, and axes of least/most moment.'''

import os
import _heapq
import numpy as np
import cv2 as cv


class ObjectManager:
    def __init__(self):
        self.binary_mtx = np.load('results/binary.npy')
        self.output = 'results'
        #find of contours of binary matrix
        self.contours, _ = cv.findContours(self.binary_mtx, 
                                                cv.RETR_LIST,
                                                cv.CHAIN_APPROX_NONE)
        if not self.contours:
            print("Binary matrix not detected")
            return 
        
        self.component_heap = []
        os.makedirs({self.output}, exist_ok=True)

    def get_area(self, contour): #calculate area from contours
        return cv.contourArea(contour)
    
    def get_moments(self, contour): #calculate moments from contours
        return cv.moments(contour)

    def get_centroid(self, contour):
        M = cv.moments(contour)
        #use moments (M) to calculate centroid (C)
        if M["m00"] != 0: #to avoid division by 0
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy)
    
    def get_axis(self, contour):
        M = cv.moments(contour)
        
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #get central moments
        mu20 = M['m20'] - cx * M['m10']
        mu02 = M['m02'] - cy * M['m01']
        mu11 = M['m11'] - cx * M['m01'] - cy * M['m10']

        #calculate angle of major axis
        angle = 0.5 * np.arctan2(2 * mu11, mu20 - mu02)
    
        #alculate length of the major and minor axes
        area = M['m00']
        major_axis_len = np.sqrt((2 * (mu20 + mu02 + np.sqrt((mu20 - mu02)**2 + 4 * mu11**2))) / area)
        minor_axis_len = np.sqrt((2 * (mu20 + mu02 - np.sqrt((mu20 - mu02)**2 + 4 * mu11**2))) / area)

        return major_axis_len, minor_axis_len, angle

        
    def gen_components(self): #get relevant information from detected objects
        for label, contour in enumerate(self.contours, start=1):
            A = self.get_area(contour)
            M = self.get_moments(contour)
            centroid = self.get_centroid(contour)
            major_axis_len, minor_axis_len, angle = self.get_axis(contour)

            #insert data into heap
            _heapq.heappush(self.component_heap,(-A, centroid, M, major_axis_len, minor_axis_len, label, angle)) 
 
        self.save_to_text()
        self.save_to_npy()            
            

    def save_to_text(self): #save data to .txt file
        text_path = os.path.join({self.output}, 'properties.txt')
        #write text to file
        with open(text_path, 'w') as f:
            for data in self.component_heap:
                f.write(f'{data[5]}: Area: {-data[0]} px, Centroid: {data[1]}, Angle: {data[6]}\n')
        print(f'Objects detected printed to: {text_path}')
    
    def save_to_npy(self): #save data to .npy for visualization
        npy_path =os.path.join({self.output}, "components.npy")
        component_data = []
        for data in self.component_heap:
            components = {'label': data[5],
                          'area': -data[0],
                          'centroid' : data[1],
                          'moments' : data[2],
                          'major_axis' : data[3],
                          'minor_axis' : data[4],
                          'angle' : data[6]}
            
            component_data.append(components)

        np.save(npy_path, component_data)
        print(f'Componnets saved to: {npy_path}')


analyzer = ObjectManager
analyzer.gen_components()
