from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageChops
import numpy as np

image = None

def open_image(path):
    global image

    try:
        image = Image.open(path)
    except FileNotFoundError:
        return FileNotFoundError
    
def save_image(path):
    global image
    image.save(path)

def img_greyscale():
    global image
    image = image.convert("L")

def img_blur():
    global image
    image = image.filter(ImageFilter.BLUR)

def img_emboss():
    global image
    image = image.filter(ImageFilter.EMBOSS)

def img_search_similarity(img1, img2):
    size = (256, 256)
    aux_img1 = np.array(img1.convert("L").resize(size))
    aux_img2 = np.array(img2.convert("L").resize(size))

    h1, bin1 = np.histogram(aux_img1, bins=256, range=(0, 255), density=True)
    h2, bin2 = np.histogram(aux_img2, bins=256, range=(0, 255), density=True)

    dist = np.linalg.norm(h1 - h2)

    return dist

