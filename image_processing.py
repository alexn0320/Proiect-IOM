from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageChops
import numpy as np
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps

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

def hsv_hist(img_pil, size=(128,128), h_bins=32, s_bins=32):
    img = img_pil.convert("RGB").resize(size)
    hsv = np.asarray(img.convert("HSV"), dtype=np.uint8)

    H = hsv[:,:,0]
    S = hsv[:,:,1]
    V = hsv[:,:,2]

    # Ignore dark background
    mask = V > 40
    if not np.any(mask):
        return np.zeros((h_bins, s_bins), dtype=np.float32)

    H = H[mask]
    S = S[mask]

    h_idx = (H * h_bins) // 255
    s_idx = (S * s_bins) // 255

    hist = np.zeros((h_bins, s_bins), dtype=np.float32)
    np.add.at(hist, (h_idx, s_idx), 1)

    hist /= hist.sum()
    return hist

def img_search_similarity(img1, img2): 
    size = (512, 512) 
    aux_img1 = np.array(img1.convert("L").resize(size)) 
    aux_img2 = np.array(img2.convert("L").resize(size)) 
    h1, bin1 = np.histogram(aux_img1, bins=256, range=(0, 255), density=True) 
    h2, bin2 = np.histogram(aux_img2, bins=256, range=(0, 255), density=True) 
    dist = np.linalg.norm(h1 - h2) 

    return dist

def img_invert():
    global image
    image = ImageOps.invert(image)
