import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


def crear_segunda_ventana():
    # Crear una nueva ventana secundaria
    segunda_ventana = tk.Toplevel()
    segunda_ventana.title("Crear crucigrama")
    segunda_ventana.geometry("1558x900")

    # Obtener el tamaño de la pantalla
    screen_width = segunda_ventana.winfo_screenwidth()
    screen_height = segunda_ventana.winfo_screenheight()
    # Ajustar el tamaño de la ventana al tamaño de la pantalla
    segunda_ventana.geometry(f"{screen_width}x{screen_height}")

    #FONDO
    image = Image.open("R.jpg")
    image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    # Crear el Label para el fondo
    bg_label = tk.Label(segunda_ventana, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  

    # Agregar un label a la ventana secundaria
    label = tk.Label(segunda_ventana, text="Ingrese un nombre para el crucigrama:", font=("Courier", 20),bg="white", fg="black")
    label.pack(pady=70)

    entrada_nombre = tk.Entry(segunda_ventana, fg='grey')
    entrada_nombre.pack(pady=20)

    # Agregar un label a la ventana secundaria
    label = tk.Label(segunda_ventana, text="Ingrese una temática:", font=("Courier", 20),bg="white", fg="black")
    label.pack(pady=30)

    entrada_tematica = tk.Entry(segunda_ventana, fg='grey')
    entrada_tematica.pack(pady=20)

    label = tk.Label(segunda_ventana, text="Digite la versión:", font=("Courier", 20),bg="white", fg="black")
    label.pack(pady=30)

    entrada_version = tk.Entry(segunda_ventana, fg='grey')
    entrada_version.pack(pady=20)

    def continuar():
        while True:
            nombre = entrada_nombre.get()  # Obtener el nombre ingresado
            tematica = entrada_tematica.get()
            version = entrada_version.get()
            if nombre and tematica and version:  # Verificar que no esté vacío
                diccionario_general= {"Versión":str(version),"nombre archivo":str(nombre), "Temática":str(tematica)}
                print(diccionario_general)
                try:
                    version = int(version)  # Intentar convertir a entero
                    from ingresar import ingresar_palabra
                    ingresar_palabra()
                except ValueError:  # Capturar si no es un número entero
                    messagebox.showinfo("Ingrese un número")
                    crear_segunda_ventana()
            else:
                messagebox.showinfo("Rellene los espacios")
                crear_segunda_ventana()
            break 

    continuar_button = tk.Button(segunda_ventana, text="Continuar", width=15, command=continuar, font=("Courier", 14), bg="white", fg="black")
    continuar_button.pack(pady=32)  

    # Agregar un botón para cerrar la ventana secundaria
    close_button = tk.Button(segunda_ventana, text="Cerrar", width=15, command=segunda_ventana.destroy, font=("Courier", 15), bg="white", fg="black")
    close_button.pack(pady=27)
    segunda_ventana.mainloop()
