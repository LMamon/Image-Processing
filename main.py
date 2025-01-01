import sys
import ImageManager as img
import ObjectManager as obj

    

def main():#main menu prompt
    im_mgr = img.ImageManager()
    obj_mgr = obj.ObjectManager()

    choice = input("\t\tWelcome!\n \n1) Convert image to binary \n2) Show centroid of object\
                   \n3) Show least and max Axis\n0) Exit\n")
    options = {
        '1' : im_mgr.convert,
        '2' : obj_mgr.show_centroid,
        '3' : obj_mgr.show_axis,
        '0' : sys.exit
    }
    if choice == '0':
        print("\n\n\t\tGoodbye")
    options[choice]()
    main()

if __name__=="__main__":
    main()
