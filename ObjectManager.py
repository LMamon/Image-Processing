'''Focuses on geometric analysis and computations, like finding contours, 
    moments, centroids, and axes of least/most moment.'''

import os
import _heapq
import numpy as np
import cv2 as cv


class ObjectManager:
    def __init__(self, binary_file='results/binary.npy', output='results'):
        self.output = output
        self.binary_file = binary_file

        if not os.path.exists(self.binary_file):
            print(f"No such file: {self.binary_file}")
            self.binary_mtx = None
            return
        
        self.binary_mtx = np.load(self.binary_file)
        if self.binary_mtx is None:
            print(f"Failed to load binary matrix from {self.binary_file}")
            return
        
        os.makedirs(self.output, exist_ok=True)
        #find of contours of binary matrix
        self.contours, _ = cv.findContours(self.binary_mtx.copy(), 
                                                cv.RETR_EXTERNAL,
                                                cv.CHAIN_APPROX_NONE)
        if not self.contours:
            print("no contours found")
            self.contours = []
            return 
        
        self.component_heap = []
        
        self.gen_components()

    def get_area(self, contour): #calculate area from contours
        return cv.contourArea(contour)
    
    def get_moments(self, contour): #calculate moments from contours
        return cv.moments(contour)

    def get_centroid(self, contour):
        M = cv.moments(contour)
        #use moments (M) to calculate centroid (C)
        if M["m00"] == 0:  # Handle division by zero gracefully
            print("Invalid contour with zero area.")
            return None
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return (cx, cy)
    
    def get_axis(self, contour):
        M = cv.moments(contour)
        if M["m00"] == 0:
            return None
        
        #pull mean‐centered moments
        mu20 = M["mu20"]
        mu02 = M["mu02"]
        mu11 = M["mu11"]

        #divide by m00 to get normalized second moments
        cov = np.array([
            [mu20, mu11],
            [mu11, mu02]
        ]) / M["m00"]
        
        #eigen‐decomposition
        vals, vecs = np.linalg.eig(cov)
        #sort
        idx = np.argsort(vals)[::-1]
        vals = vals[idx]
        vecs = vecs[:, idx]

        if vals[0] <= 0 or vals[1] <= 0:
            return None

        angle = np.arctan2(vecs[1, 0], vecs[0, 0])
        
        major_len = 2.0 * np.sqrt(2.0 * vals[0])
        minor_len = 2.0 * np.sqrt(2.0 * vals[1])
        
        return (major_len, minor_len, angle)

    def save_to_text(self): #save data to .txt file
        text_path = os.path.join(self.output, 'properties.txt')
        #write text to file
        with open(text_path, 'w') as f:
            for data in self.component_heap:
                area = -data[0]
                centroid = data[1]
                major_len = data[3]
                minor_len = data[4]
                label = data[5]
                angle = data[6]

                f.write(
                    f"Object {label}: "
                    f"Area={area:.2f} px, "
                    f"Centroid={centroid}, "
                    f"MajorAxis={major_len:.2f}, "
                    f"MinorAxis={minor_len:.2f}, "
                    f"Angle={angle:.2f}\n"
                )
        print(f'\nObjects detected printed to: {text_path}')
    
    def save_to_npy(self): #save data to .npy for visualization
        npy_path =os.path.join(self.output, "components.npy")
        component_data = []
        for data in self.component_heap:
            area = -data[0]
            centroid = data[1]
            moments = data[2]
            major_len = data[3]
            minor_len = data[4]
            label = data[5]
            angle = data[6]

            components = {
                'label': label,
                'area': area,
                'centroid': centroid,
                'moments': moments,
                'major_axis': major_len,
                'minor_axis': minor_len,
                'angle': angle
                }
            
            component_data.append(components)

        np.save(npy_path, component_data, allow_pickle=True)
        print(f'\nComponents saved to: {npy_path}')


    def gen_components(self): #get relevant information from detected objects
        print(f"Number of contours found: {len(self.contours)}")
        for label, contour in enumerate(self.contours, start=1):
            A = self.get_area(contour)
            if A == 0:
                continue

            M = self.get_moments(contour)
            centroid = self.get_centroid(contour)
            if centroid is None:
                continue
            
            axes  = self.get_axis(contour)
            if axes is None:
                continue #skipped if axis is none
                
            major_axis_len, minor_axis_len, angle = axes
            #insert data into heap
            _heapq.heappush(self.component_heap,(-A, centroid, M, major_axis_len, minor_axis_len, label, angle)) 

        self.save_to_npy()
        self.save_to_text()
