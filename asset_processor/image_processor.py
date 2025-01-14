import cv2
import os
from PIL import Image
import numpy as np

frames_folder = os.path.abspath(os.path.join('asset_processor','frames'))  
output_folder = os.path.abspath(os.path.join('asset_processor','output'))

def remove_background_and_crop(image_path, 
                               output_path, 
                               top, bottom, 
                               left, right, 
                               threshold_r=10,
                               threshold_g=100,
                               threshold_b=10):
    
    image = Image.open(image_path)
    image_rgba = image.convert("RGBA")
    data = np.array(image_rgba)
    r, g, b, a = data.T

    mask_areas = (r <= threshold_r) & (g >= threshold_g) & (b <= threshold_b)
    mask = np.invert(mask_areas).astype(np.uint8) * 255
    alpha_channel = Image.fromarray(mask.T, mode='L')
    image_rgba.putalpha(alpha_channel)

    width, height = image_rgba.size
    cropped_image = image_rgba.crop((left, top, width - right, height - bottom))
    cropped_image.save(output_path, format="PNG")
    print(f"traitement de l'image {output_path}")

def process_images_in_folder(source_folder, destination_folder, top, bottom, left, right, blue_threshold=50):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(source_folder, filename)
            output_path = os.path.join(destination_folder, os.path.splitext(filename)[0] + "_modified.png")
            remove_background_and_crop(image_path, output_path, top, bottom, left, right, blue_threshold)
            
    print("\n----- Job's done ! ------\n")



process_images_in_folder(frames_folder, output_folder, top=0, bottom=0, left=0, right=0)


# import os
# from PIL import Image
# import numpy as np

# frames_folder = os.path.abspath(os.path.join('asset_processor','frames'))  
# output_folder = os.path.abspath(os.path.join('asset_processor','output'))

# def refine_edges(mask, iterations=6):
#     """
#     Affine les contours en supprimant les pixels restants des bords avec érosion et flou.
#     """
#     import cv2
#     kernel = np.ones((2, 2), np.uint8)
#     mask = cv2.erode(mask, kernel, iterations=iterations)  # Réduit les bords verts résiduels
#     mask = cv2.GaussianBlur(mask, (3, 3), 0)  # Lisse les transitions
#     return mask

# def remove_background_and_crop(image_path, output_path, top, bottom, left, right, threshold=10):
#     image = Image.open(image_path)
#     image_rgba = image.convert("RGBA")
#     data = np.array(image_rgba)
#     r, g, b, a = data.T

#     mask_areas = (r < threshold) & (g > 100) & (b < threshold)
#     mask = np.invert(mask_areas).astype(np.uint8) * 255
#     mask = refine_edges(mask)  # Affiner les contours avant application
    
#     alpha_channel = Image.fromarray(mask.T, mode='L')
#     image_rgba.putalpha(alpha_channel)

#     width, height = image_rgba.size
#     cropped_image = image_rgba.crop((left, top, width - right, height - bottom))
#     cropped_image.save(output_path, format="PNG")
#     print(f"traitement de l'image {output_path}")

# def process_images_in_folder(source_folder, destination_folder, top, bottom, left, right, blue_threshold=50):
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)

#     for filename in os.listdir(source_folder):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             image_path = os.path.join(source_folder, filename)
#             output_path = os.path.join(destination_folder, os.path.splitext(filename)[0] + "_modified.png")
#             remove_background_and_crop(image_path, output_path, top, bottom, left, right, blue_threshold)
            
#     print("\n----- Job's done ! ------\n")

# process_images_in_folder(frames_folder, output_folder, top=100, bottom=100, left=530, right=400)
