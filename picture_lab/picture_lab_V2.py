from PIL import Image, ImageOps
import numpy as np
import os



def remove_background_and_crop(image_path, output_path, top, bottom, left, right, blue_threshold=50):
    """
    Fonction remove_background_and_crop : 
    Cette fonction prend en entrée le chemin de l'image à traiter et le chemin de sortie où l'image résultante sera enregistrée. 
    Un paramètre blue_threshold est utilisé pour définir la tolérance lors de la détection des zones bleues dans l'image.

    alpha_channel.getbbox() : Cette méthode permet de trouver la "bounding box" qui englobe tous les pixels non transparents. En d'autres termes, elle détecte les limites du personnage dans l'image.

    Rogner l'image : Le résultat de getbbox() est utilisé pour rogner l'image autour du personnage, en supprimant les parties où il n'y a que le fond transparent.

    Enregistrement en PNG : L'image est ensuite sauvegardée au format PNG pour conserver la transparence.

    """

    # Charger l'image
    image = Image.open(image_path)

    # Convertir l'image en RGBA pour gérer la transparence
    image_rgba = image.convert("RGBA")

    # Convertir l'image en tableau numpy
    data = np.array(image_rgba)

    # Séparer les canaux de couleur
    r, g, b, a = data.T

    # Définir un seuil pour identifier les zones bleues (fond)
    blue_areas = (r < blue_threshold) & (g < blue_threshold) & (b > 200)

    # Créer un masque avec les zones bleues en False, et le reste en True
    mask = np.invert(blue_areas).astype(np.uint8) * 255

    # Créer un canal alpha basé sur le masque
    alpha_channel = Image.fromarray(mask.T, mode='L')

    # Appliquer le canal alpha à l'image
    image_rgba.putalpha(alpha_channel)

    # Cropping avec les valeurs données
    width, height = image_rgba.size
    cropped_image = image_rgba.crop((left, top, width - right, height - bottom))

    # Enregistrer le résultat au format PNG
    cropped_image.save(output_path, format="PNG")

    print(f"L'image a été enregistrée à {output_path}")

def process_images_in_folder(source_folder, destination_folder, top, bottom, left, right, blue_threshold=50):
    # Vérifier si le dossier de destination existe, sinon le créer
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Parcourir tous les fichiers du dossier source
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Filtrer les fichiers d'image
            image_path = os.path.join(source_folder, filename)
            output_path = os.path.join(destination_folder, os.path.splitext(filename)[0] + "_modified.png")

            # Appliquer le traitement à chaque image
            remove_background_and_crop(image_path, output_path, top, bottom, left, right, blue_threshold)
            
    print("\n----- Job's done ! ------\n")
# Utilisation de la fonction pour traiter toutes les images dans un dossier

source_folder = f"data/"  # Remplacez par le chemin de votre dossier source
destination_folder = f"output/"  # Remplacez par le chemin de votre dossier de destination

# Spécifiez ici les marges pour le rognage (top, bottom, left, right)
process_images_in_folder(source_folder, destination_folder, top=100, bottom=100, left=530, right=400)







# def remove_background_and_crop(image_path, output_path, top, bottom, left, right, blue_threshold=50):
#     # Charger l'image
#     image = Image.open(image_path)

#     # Convertir l'image en RGBA pour gérer la transparence
#     image_rgba = image.convert("RGBA")

#     # Convertir l'image en tableau numpy
#     data = np.array(image_rgba)

#     # Séparer les canaux de couleur
#     r, g, b, a = data.T

#     # Définir un seuil pour identifier les zones bleues (fond)
#     blue_areas = (r < blue_threshold) & (g < blue_threshold) & (b > 200)

#     # Créer un masque avec les zones bleues en False, et le reste en True
#     mask = np.invert(blue_areas).astype(np.uint8) * 255

#     # Créer un canal alpha basé sur le masque
#     alpha_channel = Image.fromarray(mask.T, mode='L')

#     # Appliquer le canal alpha à l'image
#     image_rgba.putalpha(alpha_channel)

#     # Cropping avec les valeurs données
#     width, height = image_rgba.size
#     cropped_image = image_rgba.crop((left, top, width - right, height - bottom))

#     # Enregistrer le résultat au format PNG
#     cropped_image.save(output_path, format="PNG")

#     print(f"L'image a été enregistrée à {output_path}")


# ========================================================






