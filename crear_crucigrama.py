import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


def crear_segunda_ventana():
    # Crear una nueva ventana secundaria
    segunda_ventana = tk.Toplevel()
    segunda_ventana.title("Crear crucigrama")
    segunda_ventana.geometry("1558x900")

    #FONDO
    image = Image.open("R.jpg")  
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(segunda_ventana, image=bg_image)
    bg_label.place(relwidth=1, relheight=1) 

    # Agregar un label a la ventana secundaria
    label = tk.Label(segunda_ventana, text="Ingrese un nombre para el crucigrama:", font=("Courier", 30),bg="lightblue", fg="black")
    label.pack(pady=20)

    entrada_nombre = tk.Entry(segunda_ventana, fg='grey')
    entrada_nombre.pack(pady=25)

    # Agregar un label a la ventana secundaria
    label = tk.Label(segunda_ventana, text="Ingrese una temática:", font=("Courier", 30),bg="lightblue", fg="black")
    label.pack(pady=35)

    entrada_tematica = tk.Entry(segunda_ventana, fg='grey')
    entrada_tematica.pack(pady=40)

    def continuar():
        while True:
            nombre = entrada_nombre.get()  # Obtener el nombre ingresado
            tematica = entrada_tematica.get()
            if nombre and tematica:  # Verificar que no esté vacío
                from ingresar import ingresar_palabra
                ingresar_palabra()
                with open(f"{nombre}.c3d","r") as archivo:
                    contenido = archivo.read()  # Lee el contenido o lo que necesites
                    print(contenido)
            else:
                messagebox.showinfo("Debe ingresar un nombre")
                crear_segunda_ventana()
            break 

    continuar_button = tk.Button(segunda_ventana, text="Continuar", command=continuar)
    continuar_button.pack(pady=10)  

    # Agregar un botón para cerrar la ventana secundaria
    close_button = tk.Button(segunda_ventana, text="Cerrar", command=segunda_ventana.destroy)
    close_button.pack(pady=10)
    segunda_ventana.mainloop()
