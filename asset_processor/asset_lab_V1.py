import cv2
import os
from PIL import Image, ImageOps
import numpy as np



video = "test.mkv"

video_path = os.path.abspath(os.path.join('asset_processor','video', video))

frames_folder = os.path.abspath(os.path.join('asset_processor','frames'))  
output_folder = os.path.abspath(os.path.join('asset_processor','output'))  

# Vérifiez si les dossiers existent ou créez-les
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Ouverture de la vidéo
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f'Error: Cannot open video file {video_path}')
else:
    currentFrame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  
        
        # Sauvegarder chaque frame dans le dossier "frames"
        name = os.path.join(frames_folder, f'frame_{currentFrame}.jpg')
        if frame is not None:
            cv2.imwrite(name, frame)
            print(f'Creating... {name}')
        else:
            print(f'Skipping empty frame {currentFrame}')

        currentFrame += 1

    print("------ fin du traitement -------")
    cap.release()
    cv2.destroyAllWindows()

def remove_background_and_crop(image_path, output_path, top, bottom, left, right, blue_threshold=50):
    image = Image.open(image_path)
    image_rgba = image.convert("RGBA")
    data = np.array(image_rgba)
    r, g, b, a = data.T

    blue_areas = (r < blue_threshold) & (g < blue_threshold) & (b > 200)
    mask = np.invert(blue_areas).astype(np.uint8) * 255
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

# =====================================================================================

# source_folder = frames_folder  
# destination_folder = output_folder  

process_images_in_folder(frames_folder, output_folder, top=100, bottom=100, left=530, right=400)






