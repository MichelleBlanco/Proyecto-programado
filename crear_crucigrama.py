import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import subprocess
from modo_juego import modo_jugar

diccionario_general={}
nombre=[]
def crear_segunda_ventana():
    """Crea una ventana secundaria para ingresar un nombre y una temática para el crucigrama, 
    y permite proceder con la creación del crucigrama o volver al menú principal.

    Args:
        None

    Returns:
        None
    """
    
    # Crear una nueva ventana secundaria  
    segunda_ventana = tk.Tk()
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

    def ejecutar_archivo():
        """Cierra la ventana secundaria y ejecuta el archivo 'menu.py' para regresar al menú principal.

        Args:
            None

        Returns:
            None
        """
        
        segunda_ventana.destroy()    
        subprocess.run(["python", "menu.py"])

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
    
    def continuar():
        """Verifica si el nombre del crucigrama y la temática han sido ingresados. Si ambos están presentes,
        los guarda en la lista 'nombre' y procede con la función 'modo_jugar()'. Si están vacíos, 
        muestra un mensaje pidiendo que se completen los campos.

        Args:
            None

        Returns:
            None
        """
        
        while True:
            nombre_1 = entrada_nombre.get()  # Obtener el nombre ingresado
            tematica = entrada_tematica.get()
            if nombre_1 and tematica:  # Verificar que no esté vacío
                nombre.append(nombre_1)
                segunda_ventana.destroy()
                modo_jugar()
            else:
                messagebox.showinfo("Rellene los espacios")
            break 

    continuar_button = tk.Button(segunda_ventana, text="Continuar", width=15, command=continuar, font=("Courier", 14), bg="white", fg="black")
    continuar_button.pack(pady=32)     

    # Agregar un botón para cerrar la ventana secundaria
    close_button = tk.Button(segunda_ventana, text="Volver", width=15, command=ejecutar_archivo, font=("Courier", 15), bg="white", fg="black")
    close_button.pack(pady=27)

    segunda_ventana.mainloop()
