import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageOps
import image_processing
import tkinter.font as tkFont
import sys
import webbrowser

MAX_RENDER_SIZE = (600, 600)

def resize(image):
    w, h = image.size
    resized_image = image
    ratio = 0
    status = 1

    try:
        if h > MAX_RENDER_SIZE[1]:
            ratio = h / MAX_RENDER_SIZE[1]
            resized_image = image.resize((int(w/ratio), MAX_RENDER_SIZE[1]))

        if w > MAX_RENDER_SIZE[0]:
            ratio = w / MAX_RENDER_SIZE[0]
            resized_image = image.resize((MAX_RENDER_SIZE[0], int(h/ratio)))
    except:
        resized_image = None

    if ratio != 0:
        status = messagebox.askokcancel("Modificare imagine", "Imaginea este prea mare. Va fi rescalata de editor.", type='okcancel')

    return (status, resized_image)

def render(image_tk):
    global canvas
    
    canvas.delete("all")
    canvas.create_rectangle(2, 2, MAX_RENDER_SIZE[0], MAX_RENDER_SIZE[1], outline="black")
    canvas.create_image(MAX_RENDER_SIZE[0] // 2, MAX_RENDER_SIZE[1] // 2, image=image_tk, anchor="center")

def file_select():
    global filepath
    global img_data
    global image_tk

    path = filedialog.askopenfilename()

    if len(path) == 0:
        return

    path = os.path.basename(path)

    if path[len(path) - 3::] != "bmp" and path[len(path) - 3::] != "jpg" and path[len(path) - 3::] != "png":
        path = "Nu se poate deschide fisierul: " + path
        filepath.config(text=path)
        return
    
    image_processing.open_image(path)
    print(image_processing.image.size)
    status, aux = resize(image_processing.image)

    if aux is None:
        img_data.config(text="Nu se poate rescala imagea.")
        return
    elif status == 0:
        return
    elif status == 1:
        image_processing.image = aux

    image_tk = ImageTk.PhotoImage(image_processing.image)

    filepath.config(text=path)
    
    render(image_tk)

    img_data.config(text=str(image_processing.image.size) + " - " + str(image_processing.image.mode))

def processing(type):
    global image_tk
    
    if type == 'greyscale':
        image_processing.img_greyscale()
    if type == 'blur':
        image_processing.img_blur()
    if type == 'emboss':
        image_processing.img_emboss()

    image_tk = ImageTk.PhotoImage(image_processing.image)
    render(image_tk)

def image_search(org_image_path):
    path = filedialog.askdirectory()

    print(org_image_path)

    if len(path) == 0:
        return
    
    images = []
    for f in os.listdir(path):
        if f.lower().endswith((".png", ".jpg", ".jpeg")) and org_image_path != f:
            images.append(os.path.join(path, f))

    close_image = None
    min = sys.maxsize

    for img in images:
        aux_image = Image.open(img)
        dif = image_processing.img_search_similarity(image_processing.image.copy(), aux_image.copy())

        if min > dif:
            min = dif
            close_image = img

    if close_image != None:
        os.system(close_image)

def file_save():
    global filepath

    ext_map = {
        ".png": ("PNG Image", "*.png"),
        ".jpg": ("JPEG Image", "*.jpg *.jpeg"),
        ".jpeg": ("JPEG Image", "*.jpg *.jpeg"),
        ".bmp": ("BMP Image", "*.bmp"),
    }

    _, ext = os.path.splitext(filepath.cget("text"))

    path = filedialog.asksaveasfilename(filetypes=[ext_map[ext]])

    if len(path) == 0:
        return

    image_processing.save_image(path)

window = tk.Tk()
window.title("Editor de imagini")
window.resizable(False, False)
image_tk = None

ui_font = tkFont.Font(family="Verdana", size=12)
button_font = tkFont.Font(family="Verdana", size=10)

top_bar = tk.Frame(window, background="#286CA1")
top_bar.pack(anchor="nw", fill="x")

select_button = tk.Button(top_bar, text="Selectare",foreground="white", font=button_font, background="#1E4E78", highlightthickness=0, command=file_select)
select_button.pack(anchor="nw", side="left", pady=10)

save_button = tk.Button(top_bar, text="Salvare", foreground="white", font=button_font, background="#1E4E78", highlightthickness=0, command=file_save)
save_button.pack(anchor="nw", side="left", pady=10)

left_bar = tk.Frame(window, background="#286CA1")
left_bar.pack(side="left", fill="y")

image_area = tk.Frame(window, background="white")
image_area.pack(side="left", expand="True")

filepath = tk.Label(image_area, font=ui_font, background="white", text="Selectati o image.")
filepath.pack(side="top")

canvas = tk.Canvas(image_area, width=MAX_RENDER_SIZE[0]+2, height=MAX_RENDER_SIZE[1]+2, background="white")
canvas.create_rectangle(2, 2, MAX_RENDER_SIZE[0]+1, MAX_RENDER_SIZE[1]+1, outline="black")
canvas.pack(anchor="center")

img_data = tk.Label(image_area, text="", font=ui_font, background="white")
img_data.pack(side="top")

#butoanele de prelucrare
grey_button = tk.Button(left_bar, text="Greyscale", foreground="white", font=button_font, background="#1E4E78", highlightthickness=0, command=lambda: processing('greyscale'))
grey_button.pack(anchor="n", side="top", padx=10, pady=10)

blur_button = tk.Button(left_bar, text="Blur", foreground="white", font=button_font, background="#1E4E78", highlightthickness=0, command=lambda: processing('blur'))
blur_button.pack(anchor="n", side="top", padx=10, pady=10)

emboss_button = tk.Button(left_bar, text="Emboss", foreground="white", font=button_font, background="#1E4E78", highlightthickness=0, command=lambda: processing('emboss'))
emboss_button.pack(anchor="n", side="top", padx=10, pady=10)

img_search_button = tk.Button(left_bar, text="Image Search", foreground="white", font=button_font, background="#1E4E78", highlightthickness=0, command=lambda: image_search(filepath.cget("text")))
img_search_button.pack(anchor="n", side="top", padx=10, pady=10)

window.mainloop()