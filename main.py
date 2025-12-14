import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageEnhance
import image_processing
import tkinter.font as tkFont

coord_label = None
color_label = None
selected_palette_btn = None

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
    if type == 'negativ':
        image_processing.img_invert()

    image_tk = ImageTk.PhotoImage(image_processing.image)
    render(image_tk)

def img_contrast():
    global image_tk
    
    if getattr(image_processing, 'image', None) is None:
        return

    valoare = contrast_slider.get()
    valoare = float(valoare)
    
    enhancer = ImageEnhance.Contrast(image_processing.image)
    image_processing.image = enhancer.enhance(valoare)
    
    image_tk = ImageTk.PhotoImage(image_processing.image)
    render(image_tk)

def img_brightness():
    global image_tk
    
    if getattr(image_processing, 'image', None) is None:
        return

    valoare = brightness_slider.get()
    valoare = float(valoare)
    
    enhancer = ImageEnhance.Brightness(image_processing.image)
    image_processing.image = enhancer.enhance(valoare)
    
    image_tk = ImageTk.PhotoImage(image_processing.image)
    render(image_tk)

def img_sharpness():
    global image_tk
    
    if getattr(image_processing, 'image', None) is None:
        return

    valoare = sharpness_slider.get()
    valoare = float(valoare)
    
    enhancer = ImageEnhance.Sharpness(image_processing.image)
    image_processing.image = enhancer.enhance(valoare)
    
    image_tk = ImageTk.PhotoImage(image_processing.image)
    render(image_tk)

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


def update_coords(event):
    global coords_label,  color_label, image_tk

    # daca nu exista inca imagine
    if image_tk is None or image_processing.image is None:
        coords_label.config(text="x: -  y: -")
        color_label.config(text="#------")
        return

    img_w, img_h = image_processing.image.size

    # imaginea este desenata centrat, in render()
    canvas_w = MAX_RENDER_SIZE[0] + 2
    canvas_h = MAX_RENDER_SIZE[1] + 2

    offset_x = (canvas_w - img_w) // 2
    offset_y = (canvas_h - img_h) // 2

    # coordonate mouse in canvas
    cx, cy = event.x, event.y

    # coordonate in imagine
    ix = cx - offset_x
    iy = cy - offset_y

    # daca mouse-ul e in afara imaginii
    if ix < 0 or iy < 0 or ix >= img_w or iy >= img_h:
        coords_label.config(text="x: -  y: -")
        return

    coords_label.config(text=f"x: {ix}  y: {iy}")
    px = image_processing.image.getpixel((ix, iy))

    if isinstance(px, int):
        r = g = b = px
    else:
        r, g, b = px[0], px[1], px[2]

    color_label.config(text=f"#{r:02X}{g:02X}{b:02X}")

def clear_coords(_event=None):
    global coords_label, color_label
    coords_label.config(text="x: -  y: -")
    color_label.config(text="#------")

draw_enabled = True
is_drawing = False

brush_size = 3  #grosime pensula

def set_draw_color(rgb_tuple):
    global draw_color
    draw_color = rgb_tuple

def select_palette_color(btn, rgb_tuple):
    global selected_palette_btn
    set_draw_color(rgb_tuple)

    # evidentiere buton selectat
    if selected_palette_btn is not None:
        selected_palette_btn.config(relief="raised", bd=1)
    btn.config(relief="sunken", bd=2)
    selected_palette_btn = btn

def set_brush(size):
    global brush_size
    brush_size = int(size)

def canvas_to_image_xy(cx, cy):
    # Converteste coordonatele de pe canvas in coordonate in imagine (tinand cont ca imaginea e centrata)
    if image_tk is None or image_processing.image is None:
        return None

    img_w, img_h = image_processing.image.size
    canvas_w = MAX_RENDER_SIZE[0] + 2
    canvas_h = MAX_RENDER_SIZE[1] + 2

    offset_x = (canvas_w - img_w) // 2
    offset_y = (canvas_h - img_h) // 2

    ix = cx - offset_x
    iy = cy - offset_y

    if ix < 0 or iy < 0 or ix >= img_w or iy >= img_h:
        return None

    return (ix, iy)

def draw_at(ix, iy):
    global image_tk

    # asigura un mod "desenabil"
    if image_processing.image.mode not in ("RGB", "RGBA"):
        image_processing.image = image_processing.image.convert("RGB")

    draw = ImageDraw.Draw(image_processing.image)

    r = brush_size
    draw.ellipse((ix - r, iy - r, ix + r, iy + r), fill=draw_color, outline=draw_color)

    # rerandare
    image_tk = ImageTk.PhotoImage(image_processing.image)
    render(image_tk)

def start_draw(event):
    global is_drawing
    if not draw_enabled:
        return

    p = canvas_to_image_xy(event.x, event.y)
    if p is None:
        return

    is_drawing = True
    draw_at(p[0], p[1])

def draw_move(event):
    global is_drawing
    if not draw_enabled or not is_drawing:
        return

    p = canvas_to_image_xy(event.x, event.y)
    if p is None:
        return

    draw_at(p[0], p[1])

def stop_draw(_event=None):
    global is_drawing
    is_drawing = False

window = tk.Tk()
window.title("Editor de imagini")
window.resizable(False, False)
image_tk = None

ui_font = tkFont.Font(family="Verdana", size=12)
button_font = tkFont.Font(family="Verdana", size=10)

BTN_W = 10
BTN_H = 1

top_bar = tk.Frame(window, bg="#286CA1")
top_bar.pack(anchor="nw", fill="x")

select_button = tk.Button(top_bar, text="Selectare",foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                           width=BTN_W, height=BTN_H, command=file_select)
select_button.pack(anchor="nw", side="left", padx=12, pady=8)

save_button = tk.Button(top_bar, text="Salvare", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                         width=BTN_W, height=BTN_H, command=file_save)
save_button.pack(anchor="nw", side="left", padx=15, pady=8)

left_bar = tk.Frame(window, bg="#286CA1")
left_bar.pack(side="left", fill="y")

image_area = tk.Frame(window, bg="white")
image_area.pack(side="left", expand="True")

filepath = tk.Label(image_area, font=ui_font, background="white", text="Selectati o image.")
filepath.pack(side="top")

canvas = tk.Canvas(image_area, width=MAX_RENDER_SIZE[0]+2, height=MAX_RENDER_SIZE[1]+2, bg="white")
canvas.create_rectangle(2, 2, MAX_RENDER_SIZE[0]+1, MAX_RENDER_SIZE[1]+1, outline="black")
canvas.pack(anchor="center")

img_data = tk.Label(image_area, text="", font=ui_font, bg="white")
img_data.pack(side="top")

#label coordonate pixel
coords_label = tk.Label(image_area, text="x: -  y: -", font=button_font, padx=2, pady=1, bg="white", fg="black", borderwidth=1)
coords_label.place(relx=1.0, rely=1.0, anchor="se", x=-4, y=-4)

#label culoare pixel
color_label = tk.Label(image_area, text="#------", font=button_font, padx=2, pady=1, bg="white", fg="black", borderwidth=1)
color_label.place(relx=0.0, rely=1.0, anchor="sw", x=4, y=-4)

canvas.bind("<Motion>", update_coords)
canvas.bind("<Leave>", clear_coords)

canvas.bind("<Button-1>", start_draw, add="+")
canvas.bind("<B1-Motion>", draw_move, add="+")
canvas.bind("<ButtonRelease-1>", stop_draw, add="+")

#butoanele de prelucrare
grey_button = tk.Button(left_bar, text="Greyscale", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                        width=BTN_W, height=BTN_H, command=lambda: processing('greyscale'))
grey_button.pack(anchor="n", side="top", padx=10, pady=5)

blur_button = tk.Button(left_bar, text="Blur", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                        width=BTN_W, height=BTN_H, command=lambda: processing('blur'))
blur_button.pack(anchor="n", side="top", padx=10, pady=5)

emboss_button = tk.Button(left_bar, text="Emboss", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                          width=BTN_W, height=BTN_H, command=lambda: processing('emboss'))
emboss_button.pack(anchor="n", side="top", padx=10, pady=5)

negativ_button = tk.Button(left_bar, text="Invert", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                          width=BTN_W, height=BTN_H, command=lambda: processing('negativ'))
negativ_button.pack(anchor="n", side="top", padx=10, pady=5)
spacer = tk.Frame(left_bar, height=20, bg="#286CA1") 
spacer.pack(side="top", fill="x")

#slideuri de prelucrare
contrast_slider = tk.Scale(left_bar, label="Contrast", from_=0, to=2, orient='horizontal', length=200, resolution=0.1, 
                           foreground="white", font=button_font, bg="#1E4E78")
contrast_slider.set(1)
contrast_slider.pack(anchor="n", side="top", padx=10, pady=0)

contrast_button = tk.Button(left_bar, text="Aplica contrast", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                            command=img_contrast)
contrast_button.pack(anchor="n", side="top", padx=10, pady=0)
spacer = tk.Frame(left_bar, height=10, bg="#286CA1") 
spacer.pack(side="top", fill="x")

brightness_slider = tk.Scale(left_bar, label="Brightness", from_=0, to=2, orient='horizontal', length=200, resolution=0.1, 
                           foreground="white", font=button_font, bg="#1E4E78")
brightness_slider.set(1)
brightness_slider.pack(anchor="n", side="top", padx=10, pady=0)

brightness_button = tk.Button(left_bar, text="Aplica brightness", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                            command=img_brightness)
brightness_button.pack(anchor="n", side="top", padx=10, pady=0)
spacer = tk.Frame(left_bar, height=10, bg="#286CA1") 
spacer.pack(side="top", fill="x")

sharpness_slider = tk.Scale(left_bar, label="Sharpness", from_=0, to=2, orient='horizontal', length=200, resolution=0.1, 
                           foreground="white", font=button_font, bg="#1E4E78")
sharpness_slider.set(1)
sharpness_slider.pack(anchor="n", side="top", padx=10, pady=0)

sharpness_button = tk.Button(left_bar, text="Aplica sharpness", foreground="white", font=button_font, bg="#1E4E78", highlightthickness=0, 
                            command=img_sharpness)
sharpness_button.pack(anchor="n", side="top", padx=10, pady=0)

#reglare dimensiune pensula
brush_title = tk.Label(left_bar, text="Brush size", fg="white", bg="#286CA1", font=button_font)
brush_title.pack(anchor="n", padx=10, pady=(20, 6))

brush_scale = tk.Scale(left_bar, from_=1, to=30, orient="horizontal", command=set_brush, bg="#286CA1", fg="white",
                       troughcolor="#1E4E78", highlightthickness=0)
brush_scale.set(brush_size)   

#paleta culori
palette_title = tk.Label(left_bar, text="Colors", fg="white", bg="#286CA1", font=button_font)
palette_title.pack(anchor="n", padx=10, pady=(20, 6))

palette_frame = tk.Frame(left_bar, bg="#286CA1")
palette_frame.pack(anchor="n", padx=10, pady=5)

palette_title.pack_forget()
palette_frame.pack_forget()

palette_frame.pack(side="bottom", padx=10, pady=10)
palette_title.pack(side="bottom", padx=10, pady=(0, 4))

brush_title.pack_forget()
brush_scale.pack_forget()

brush_scale.pack(side="bottom", padx=10, pady=(0, 10))
brush_title.pack(side="bottom", padx=10, pady=(10, 6))

# lista culori
palette_colors = [
    ("Black",  (0, 0, 0),       "#000000"),
    ("White",  (255, 255, 255), "#FFFFFF"),
    ("Red",    (255, 0, 0),     "#FF0000"),
    ("Green",  (0, 255, 0),     "#00FF00"),
    ("Blue",   (0, 0, 255),     "#0000FF"),
    ("Yellow", (255, 255, 0),   "#FFFF00"),
    ("Cyan",   (0, 255, 255),   "#00FFFF"),
    ("Magenta",(255, 0, 255),   "#FF00FF"),
    ("Orange", (255, 165, 0),   "#FFA500"),
    ("Purple", (128, 0, 128),   "#800080"),
    ("Brown",  (139, 69, 19),   "#8B4513"),
    ("Gray",   (128, 128, 128), "#808080"),
]

# creeaza butoane patrate in grid
cols = 6
for i, (name, rgb, hexcol) in enumerate(palette_colors):
    r = i // cols
    c = i % cols

    b = tk.Button(palette_frame, bg=hexcol, width=2, height=1, relief="raised", bd=1, highlightthickness=1)

    # selectare implicita (de ex. Red = index 2)
    btns = palette_frame.winfo_children()
    if len(btns) > 0:
        select_palette_color(btns[0], palette_colors[0][1])

    b.grid(row=r, column=c, padx=2, pady=2)
    b.config(command=lambda b=b, rgb=rgb: select_palette_color(b, rgb))

window.mainloop()