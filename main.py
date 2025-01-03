'''main menu provides navigation and options for user'''

import sys
import ImageManager
import RenderManager as rnd

    

def main():#main menu prompt
    img_mgr = ImageManager.ImageManager() #instanace of image manager
    rnd_mgr = rnd.RenderManager()    
    

    choice = input("\t\tWelcome!\n \n1) Choose image with object(s) \n2) Show binary \
                   \n3) Show color image \n4) Show centroid of object(s) \
                   \n5) Show least and max moment Axis\n0) Exit\n>>")
    options = {
        '1' : img_mgr.get_image, #get user to select image
        '2' : rnd_mgr.show_binary,
        '3' : rnd_mgr.show_color,
        '4' : rnd_mgr.show_centroid,
        
        '0' : sys.exit
    }
    if choice == '0':
        print("\n\n\t\tGoodbye")
    options[choice]()
    main()

if __name__=="__main__":
    main()
