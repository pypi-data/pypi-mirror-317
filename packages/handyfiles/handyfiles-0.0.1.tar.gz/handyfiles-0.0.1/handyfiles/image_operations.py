from PIL import Image
import os
import shutil

def list_images(directory):
    try:
        return [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."

def copy_image(source, destination):
    try:
        shutil.copy(source, destination)
        return f"Image '{source}' copied to '{destination}'."
    except Exception as e:
        return f"Error: {e}"

def resize_image(image_path, output_path, size):
    try:
        pass
        #TODO
    except Exception as e:
        return f"Error: {e}"
