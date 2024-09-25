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

    def continuar():
        while True:
            nombre = entrada_nombre.get()  # Obtener el nombre ingresado
            if nombre:  # Verificar que no esté vacío
                from ingresar import ingresar_palabra
                ingresar_palabra()
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

    # Agregar un botón para cerrar la ventana secundaria
    close_button = tk.Button(segunda_ventana, text="Cerrar", command=segunda_ventana.destroy)
    close_button.pack(pady=10)
    segunda_ventana.mainloop()
