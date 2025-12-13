canvas.bind("<Button-1>", start_draw, add="+")
canvas.bind("<B1-Motion>", draw_move, add="+")
canvas.bind("<ButtonRelease-1>", stop_draw, add="+")