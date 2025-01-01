'''main menu provides navigation and options for user'''

import sys
import ImageManager as img
import ObjectManager as obj

    

def main():#main menu prompt
    img_mgr = img.ImageManager()
    obj_mgr = obj.ObjectManager()

    choice = input("\t\tWelcome!\n \n1) Choose image with object(s) \n2) Convert image to binary \
                   \n3) Show centroid of object \n4) Show least and max moment Axis\n0) Exit\n")
    options = {
        '1' : img_mgr.get_img, #get user to select image
        '2' : img_mgr.convert, #threshold> binary>store binary in results
        '5' : img_mgr.show_color,
        '3' : obj_mgr.show_centroid,
        '4' : obj_mgr.show_axis,
        '0' : sys.exit
    }
    if choice == '0':
        print("\n\n\t\tGoodbye")
    options[choice]()
    main()

if __name__=="__main__":
    main()
