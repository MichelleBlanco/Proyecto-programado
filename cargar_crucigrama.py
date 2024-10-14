import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

nombre=[]

def listar_archivos():
    """Lista los archivos con extensión '.c3d' en el directorio actual.

    Args:
        No tiene argumentos.

    Returns:
        list: Una lista de nombres de archivos que terminan con '.c3d'.
    """
        
    # Listar archivos que terminan en .c3d en el directorio actual
    return [f for f in os.listdir() if f.endswith('.c3d')]

def jugar():
    """Valida el archivo de crucigrama ingresado por el usuario y muestra un mensaje de éxito o error. 
    Si el archivo existe en la lista de archivos, se procede con la lógica de iniciar el juego.
    
    Args:
        None

    Returns:
        None
    """
    nombre_archivo = entrada_nombre.get().strip()
    if nombre_archivo in archivos:
        # Si el archivo existe, proceder a la ventana de jugar (puedes cambiar esto por la lógica que necesites)
        # Aquí podrías importar y llamar a la función correspondiente para leer y jugar con el crucigrama
        nombre.append(nombre_archivo)
        messagebox.showinfo("Éxito", f"¡Vas a jugar con el archivo: {nombre_archivo}!")
        # Por ejemplo, aquí podrías llamar a la función de leer_jugar.py
        # leer_jugar(nombre_archivo)
        import hola
    else:
        # Si el archivo no existe, mostrar un mensaje de error
        messagebox.showerror("Error", "El archivo no existe. Por favor, ingresa un nombre válido.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Seleccionar Crucigrama")
ventana.geometry("1550x900")

# FONDO
image = Image.open("flor.png")
image = image.resize((1550, 900), Image.Resampling.LANCZOS)  # Cambiar a 800x800
bg_image = ImageTk.PhotoImage(image)

# Crear el Label para el fondo
bg_label = tk.Label(ventana, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Listar archivos .c3d
archivos = listar_archivos()

# Etiqueta para la lista de archivos
etiqueta_archivos = tk.Label(ventana, text="Archivos disponibles:")
etiqueta_archivos.pack(pady=10)

# Crear un marco para la lista de archivos
frame_lista = tk.Frame(ventana)
frame_lista.pack(pady=5)

# Crear un Listbox para mostrar los archivos
lista_archivos = tk.Listbox(frame_lista, width=50, height=10)
for archivo in archivos:
    lista_archivos.insert(tk.END, archivo)
lista_archivos.pack()

# Etiqueta para la entrada de texto
etiqueta_ingreso = tk.Label(ventana, text="Ingresa el nombre del archivo:")
etiqueta_ingreso.pack(pady=10)


# Entrada de texto
entrada_nombre = tk.Entry(ventana, width=30)
entrada_nombre.pack(pady=5)

# Botón para jugar
boton_jugar = tk.Button(ventana, text="Jugar", command=jugar)
boton_jugar.pack(pady=20)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
