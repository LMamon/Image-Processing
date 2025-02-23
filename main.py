'''main menu provides navigation and options for user'''

import sys
import ImageManager
import RenderManager as rnd
import ObjectManager as obj
import ProcessingManager as prc    

def main():#main menu prompt
    print("\n\t\tWelcome!\n")

    img_mgr = ImageManager.ImageManager() #instanace of image manager
    obj_mgr = None
    rnd_mgr = None
    prc_mgr = None

    while True: 
        print("1) Choose image with object(s)")
        print("2) Show binary")
        print("3) Show color")
        print("4) Show centroid of objects")
        print('5) Show least and max moments')
        print('6) Show Gaussian blur')
        print('7) Show Median blur')
        print('8) Show Sharpened')
        print('9) Show FT')

        print("0) Exit")

        choice = input(">>")

        if choice == '1':
            img_mgr.get_image()
            obj_mgr = obj.ObjectManager()
            prc_mgr = prc.ProcessingManager()
            rnd_mgr = rnd.RenderManager(obj_mgr)

        
        elif choice == '2':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                rnd_mgr.show_binary()
        elif choice == '3':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                rnd_mgr.show_color()
        elif choice == '4':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                obj_mgr.gen_components()
                rnd_mgr.show_centroid()
        elif choice == '5':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                obj_mgr.gen_components()
                rnd_mgr.show_axis()
        elif choice == '6':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                prc_mgr.gaussian(5)
                rnd_mgr.show_gaussian()
        elif choice == '7':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                prc_mgr.median()
                rnd_mgr.show_median()
        elif choice == '8':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                prc_mgr.sharpen()
                rnd_mgr.show_sharpened()
        elif choice == '9':
            if rnd_mgr is None:
                print("please load an image first (option 1)")
            else:
                prc_mgr.opencvFT()
                rnd_mgr.showFT()
        elif choice == '0':
            print("\n\tGoodbye")
            sys.exit()

        else:
            print("Please input a valid option")

if __name__=="__main__":
    main()
