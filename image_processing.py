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

def img_invert():
    global image
    image = ImageOps.invert(image)
