import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import image_processing

MAX_RENDER_SIZE = (600, 600)
MIN_RENDER_SIZE = (300, 300)

def resize(image):
    w, h = image.size
    resized_image = image

    if h >= MAX_RENDER_SIZE[1]:
        ratio = h / MAX_RENDER_SIZE[1]
        resized_image = image.resize((int(w/ratio), MAX_RENDER_SIZE[1]))
    elif h <= MIN_RENDER_SIZE[1]:
        ratio = h / MIN_RENDER_SIZE[1]
        resized_image = image.resize((int(w/ratio), MIN_RENDER_SIZE[1]))

    if w >= MAX_RENDER_SIZE[0]:
        ratio = w / MAX_RENDER_SIZE[0]
        resized_image = image.resize((MAX_RENDER_SIZE[0], int(h/ratio)))
    elif w <= MIN_RENDER_SIZE[0]:
        ratio = w / MIN_RENDER_SIZE[0]
        resized_image = image.resize((MIN_RENDER_SIZE[0]), int(h/ratio))

    return resized_image

def file_select():
    global filepath
    global canvas
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
    image_processing.image = resize(image_processing.image)
    image_tk = ImageTk.PhotoImage(image_processing.image)

    filepath.config(text=path)

    canvas.delete("all")
    canvas.create_rectangle(1, 1, MAX_RENDER_SIZE[0] - 1, MAX_RENDER_SIZE[1] - 1, outline="black")
    canvas.create_image(
        MAX_RENDER_SIZE[0] // 2,
        MAX_RENDER_SIZE[1] // 2,
        image=image_tk,
        anchor="center"
    )

    img_data.config(text=str(image_processing.image.size) + " - " + str(image_processing.image.mode))

window = tk.Tk()
window.title("Editor de imagini")
window.resizable(False, False)
image_tk = None

top_bar = tk.Frame(window, background="#286CA1")
top_bar.pack(anchor="nw", fill="x")

select_button = tk.Button(top_bar, text="Selectare",foreground="white", background="#1E4E78", highlightthickness=0, command=file_select)
select_button.pack(anchor="nw", side="left", pady=10)

save_button = tk.Button(top_bar, text="Salvare", foreground="white", background="#1E4E78", highlightthickness=0)
save_button.pack(anchor="nw", side="left", pady=10)

image_area = tk.Frame(window, background="white")
image_area.pack(anchor="center")

filepath = tk.Label(image_area, font="bold", background="white", text="Selectati o image.")
filepath.pack(side="top")

canvas = tk.Canvas(image_area, width=MAX_RENDER_SIZE[0], height=MAX_RENDER_SIZE[1], background="white")
canvas.create_rectangle(1, 1, MAX_RENDER_SIZE[0] - 1, MAX_RENDER_SIZE[1] - 1, outline="black")
canvas.pack(anchor="center")

img_data = tk.Label(image_area, text="", font="bold", background="white")
img_data.pack(side="top")

window.mainloop()
