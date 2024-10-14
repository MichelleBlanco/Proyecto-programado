import tkinter as tk
from PIL import Image, ImageTk
from crear_crucigrama import crear_segunda_ventana


def crear_crucigrama():
    """Cierra la ventana principal y abre la segunda ventana para crear un crucigrama.
    
    Args:
        None

    Returns:
        None
    """
    ventana.destroy()
    crear_segunda_ventana() 
    
def cargar_crucigrama(): 
    """Cierra la ventana principal y carga el módulo para cargar un crucigrama existente.
    
    Args:
        None

    Returns:
        None
    """ 
    ventana.destroy()
    import cargar_crucigrama

def salir_juego():
    """Cierra la ventana principal y termina la aplicación.
    
    Args:
        None

    Returns:
        None
    """
    ventana.destroy()

#CREACIÓN DE LA VENTANA

ventana = tk.Tk()
ventana.title("Generador de crucigramas 3D")
ventana.geometry("1550x900")

# Obtener el tamaño de la pantalla
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()

# Ajustar el tamaño de la ventana al tamaño de la pantalla
ventana.geometry(f"{screen_width}x{screen_height}")

# Cargar la imagen y redimensionarla al tamaño de la pantalla
image = Image.open("fondo.jpg")
image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(image)

# Crear el Label para el fondo
bg_label = tk.Label(ventana, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

#TÍTULO
title_label = tk.Label(ventana, text="Generador de crucigramas 3D", font=("Courier", 30),bg="black", fg="white")
title_label.pack(pady=130)
#BOTONES
create_button = tk.Button(ventana, text="Crear Crucigrama", width=18, command=crear_crucigrama, font=("Courier", 14), bg="black", fg="white")
create_button.pack(pady=30)
load_button = tk.Button(ventana, text="Cargar Crucigrama", width=18, command=cargar_crucigrama, font=("Courier", 14), bg="black", fg="white")
load_button.pack(pady=30)
exit_button = tk.Button(ventana, text="Salir", width=18, command=salir_juego, font=("Courier", 14), bg="black", fg="white")
exit_button.pack(pady=30)

if __name__=="__main__":   
    ventana.mainloop()

exit_button = tk.Button(ventana, text="Salir", width=18, command=salir_juego, font=("Courier", 14), bg="lightblue")
exit_button.pack(pady=30)

ventana.mainloop()
