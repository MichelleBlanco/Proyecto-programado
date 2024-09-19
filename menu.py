import tkinter as tk
from PIL import Image, ImageTk

def crear_crucigrama():
    import crear_crucigrama
    crear_crucigrama()

def cargar_crucigrama():
    import cargar_crucigrama
    cargar_crucigrama()

def salir_juego():
    ventana.destroy()

#CREACIÓN DE LA VENTANA
ventana = tk.Tk()
ventana.title("Generador de crucigramas 3D")
ventana.geometry("800x800")

#FONDO
image = Image.open("fondo.jpg")  
bg_image = ImageTk.PhotoImage(image)
bg_label = tk.Label(ventana, image=bg_image)
bg_label.place(relwidth=1, relheight=1) 

#TÍTULO
title_label = tk.Label(ventana, text="Generador de crucigramas 3D", font=("Courier", 30),bg="lightblue", fg="black")
title_label.pack(pady=130)

#BOTONES
create_button = tk.Button(ventana, text="Crear Crucigrama", width=18, command=crear_crucigrama, font=("Courier", 14), bg="lightblue")
create_button.pack(pady=30)

load_button = tk.Button(ventana, text="Cargar Crucigrama", width=18, command=cargar_crucigrama, font=("Courier", 14), bg="lightblue")
load_button.pack(pady=30)

exit_button = tk.Button(ventana, text="Salir", width=18, command=salir_juego, font=("Courier", 14), bg="lightblue")
exit_button.pack(pady=30)

ventana.mainloop()