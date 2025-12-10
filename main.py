import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import image_processing

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

    canvas.delete("all")
    canvas.create_rectangle(1, 1, MAX_RENDER_SIZE[0] - 1, MAX_RENDER_SIZE[1] - 1, outline="black")
    canvas.create_image(
        MAX_RENDER_SIZE[0] // 2,
        MAX_RENDER_SIZE[1] // 2,
        image=image_tk,
        anchor="center"
    )

    img_data.config(text=str(image_processing.image.size) + " - " + str(image_processing.image.mode))

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

    print(path + ext)

    image_processing.save_image(path)

window = tk.Tk()
window.title("Editor de imagini")
window.resizable(False, False)
image_tk = None

top_bar = tk.Frame(window, background="#286CA1")
top_bar.pack(anchor="nw", fill="x")

select_button = tk.Button(top_bar, text="Selectare",foreground="white", background="#1E4E78", highlightthickness=0, command=file_select)
select_button.pack(anchor="nw", side="left", pady=10)

save_button = tk.Button(top_bar, text="Salvare", foreground="white", background="#1E4E78", highlightthickness=0, command=file_save)
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
