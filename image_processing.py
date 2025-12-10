from PIL import Image

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

