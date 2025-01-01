'''Handles vizualizing/displaying image and geometric properties'''

import cv2 as cv
import ImageManager as img
import ObjectManager as obj


class RenderManager:
    def __init__(self):
        self.img_mgr = img.ImageManager()
        self.obj_mgr = obj.ObjectManager()

    def show_binary(self):
        self.img_mgr.load_binary_mtx()
        if self.img_mgr.binary_mtx is None:
            print("No binary image to show")
            return
        cv.imshow("Binary image",self.img_mgr.binary_mtx)
        print("Click on Window And Press Any Key To Close Image")
        cv.waitKey(0)
        cv.destroyAllWindows()

    def show_color(self):
        self.img_mgr.load_color_mtx()
        if self.img_mgr.color_mtx is None:
            print("No color image to show")
            return
        cv.imshow("Color image",self.img_mgr.color_mtx)
        print("Click on Window And Press Any Key To Close Image")
        cv.waitKey(0)
        cv.destroyAllWindows()