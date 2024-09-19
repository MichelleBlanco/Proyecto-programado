import tkinter as tk

def draw_cube(canvas, width, height, depth):
    # Coordenadas del vértice superior frontal izquierdo del cubo
    x0, y0 = 100, 100

    # Vértices frontales
    x1, y1 = x0 + width, y0
    x2, y2 = x0 + width, y0 + height
    x3, y3 = x0, y0 + height

    # Vértices trasladados hacia atrás (para la perspectiva)
    x4, y4 = x0 + depth, y0 - depth
    x5, y5 = x1 + depth, y1 - depth
    x6, y6 = x2 + depth, y2 - depth

    # Dibujar las aristas del cubo
    # Caras visibles
    # Cara frontal
    canvas.create_line(x0, y0, x1, y1)
    canvas.create_line(x1, y1, x2, y2)
    canvas.create_line(x2, y2, x3, y3)
    canvas.create_line(x3, y3, x0, y0)

    # Cara derecha
    canvas.create_line(x1, y1, x5, y5)
    canvas.create_line(x2, y2, x6, y6)
    canvas.create_line(x5, y5, x6, y6)

    # Cara superior
    canvas.create_line(x0, y0, x4, y4)
    canvas.create_line(x1, y1, x5, y5)
    canvas.create_line(x4, y4, x5, y5)

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("Cubo 3D en Tkinter")

# Crear un lienzo para dibujar
canvas = tk.Canvas(root, width=400, height=400, bg='white')
canvas.pack()

# Dibujar el cubo en el lienzo con dimensiones personalizadas
cube_width = 100
cube_height = 100
cube_depth = 60
draw_cube(canvas, cube_width, cube_height, cube_depth)

# Iniciar el bucle principal de la ventana
root.mainloop()



