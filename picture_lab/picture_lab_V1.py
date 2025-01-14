from PIL import Image
import os
import json


###############################
"""
module de traitement image et construction de spritesheets
"""


filename_list = []

def audit_folder(file_path):    
    
    for file in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, file)):
                        
            f_name, f_ext = file.split(".")

            filename_list.append({f_name:f_ext})

    file_count = len(filename_list)
    print("\nil y a {} fichier(s) dans {}\n".format(file_count, file_path))

    for file in filename_list:
        print(list(file.items())) 

    return file_count

###############################

lab = "picture_lab"
project = "test2"            # anim_1b
src_type = "fpf"                #  ss -> spritesheet  | fpf ->frame per frame
file_format ="jpg"
resolution_swap = False 

resize = True
resize_value = (32, 32)

save_path = rf"C:\Users\Vivien\My_py\GAN_pixelart\labs\{lab}"
file_path = rf"{save_path}\{project}"

file_count = audit_folder(file_path)
frame_count = int(file_count/2) if resolution_swap else file_count

file_list = []

data = {
    "frames": 
    {
        # "walk_front_1.png":
        # {
        #     "frame": {"x":0,"y":0,"w":32,"h":32},
        #     "rotated": False,
        #     "trimmed": False,
        #     "spriteSourceSize": {"x":0,"y":0,"w":32,"h":32},
        #     "sourceSize": {"w":32,"h":32}
        # },
    },
    
    "meta": 
    {
        "app": "HKSN_Picture_lab",
        "version": "1.0",
        "image": "new_spritesheet.png",
        "format": "RGBA",
        "size": {"w":94,"h":130},
        "scale": "1",
        "smartupdate": ""
    }
}

# output settings
new_spritesheet = Image.new('RGB',(file_count*resize_value[0], resize_value[1]), (250,250,250))


for index, name in enumerate(filename_list):

    file_info= {"{}.{}".format(name, file_format):
    {
            "frame": {"x":0,"y":0,"w":32,"h":32},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x":0,"y":0,"w":32,"h":32},
            "sourceSize": {"w":32,"h":32}
        }}
    
    # Read the images---------------------------------------------------
    file = Image.open(r'{}/{}.{}'.format(file_path, list(name.keys())[0], file_format))

    # Crop ----------------------------------------- 1280x720 -> 640x640
    width, height = file.size
    # positives values
    left = 390
    top = 80
    # negatives values
    right = width - 250
    bottom = height

    file = file.crop((left, top, right, bottom)) 

    # resize -----------------------------------------> 32x32
    if resize:                                       
        file = file.resize(resize_value)
        width, height = file.size

    # add img to spritesheet ----------------------------------------------
    new_spritesheet.paste(file,((index*width),0))
    print("image {}: index {} ajoutée".format(name, index))

    # file_list.append(file)

    # backup --------------------------------------------------------------
with open(save_path + r"\new_spritesheet.json", 'w') as file:
    # Écrire le dictionnaire JSON dans le fichier
    json.dump(data, file, indent=4)
    print("Fichier JSON vierge puis enregistré avec succès.")

new_spritesheet.save(r"{}/new_spritesheet.jpg".format(save_path),"JPEG")
new_spritesheet.show()


#====================================================================================
# Lab


