import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def ingresar_palabra():
    # Crear una nueva ventana secundaria
    tercera_ventana = tk.Toplevel()
    tercera_ventana.title("Crear crucigrama")
    tercera_ventana.geometry("1558x900")

    # Obtener el tamaño de la pantalla
    screen_width = tercera_ventana.winfo_screenwidth()
    screen_height = tercera_ventana.winfo_screenheight()
    # Ajustar el tamaño de la ventana al tamaño de la pantalla
    tercera_ventana.geometry(f"{screen_width}x{screen_height}")

    #FONDO
    image = Image.open("R.jpg")
    image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    # Crear el Label para el fondo
    bg_label = tk.Label(tercera_ventana, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  

    label = tk.Label(tercera_ventana, text= "Defina el tamaño de la cuadricula, en el eje x, y, z: ", font=("Courier", 30),bg="lightblue", fg="black")
    label.pack(pady=20)

    eje_x = tk.Entry(tercera_ventana, fg='grey')
    eje_x.place(x=500, y=100)
    eje_y = tk.Entry(tercera_ventana, fg='grey')
    eje_y.place(x=700, y=100)
    eje_z = tk.Entry(tercera_ventana, fg='grey')
    eje_z.place(x=900, y=100)

    label = tk.Label(tercera_ventana, text= "Ingrese una palabra: ", font=("Courier", 30),bg="lightblue", fg="black")
    label.pack(pady=75)

    entrada_palabra = tk.Entry(tercera_ventana, fg='grey')
    entrada_palabra.pack(pady=25)
    
    label = tk.Label(tercera_ventana, text= "Ingrese la definición: ", font=("Courier", 30),bg="lightblue", fg="black")
    label.pack(pady=20)
    entrada_definicion = tk.Entry(tercera_ventana, fg='grey')
    entrada_definicion.pack(pady=25)
    

    #BOTONES
    jugar_button = tk.Button(tercera_ventana, text="Jugar", width=15, command=jugar, font=("Courier", 14), bg="white", fg="black")
    jugar_button.pack(pady=32)  
    
        # Agregar un botón para cerrar la ventana secundaria
    close_button = tk.Button(tercera_ventana, text="Cerrar", width=15, command=tercera_ventana.destroy, font=("Courier", 15), bg="white", fg="black")
    close_button.pack(pady=27)

    def jugar():
        while True:
            x = eje_x.get()  # Obtener el nombre ingresado
            y = eje_y.get()
            z = eje_z.get()
            palabra = entrada_palabra.get()  # Obtener el nombre ingresado
            definicion = entrada_definicion.get()
            if x and y and z and palabra and definicion:  # Verificar que no esté vacío
                #diccionario_general= {"Versión":str(version),"nombre archivo":str(nombre), "Temática":str(tematica)}
                #print(diccionario_general)
                try:
                    x = int(x)  # Intentar convertir a entero
                    y = int(y)
                    z = int(z)
                    from jugar import crear_cuarta_ventana
                    crear_cuarta_ventana()
                except ValueError:  # Capturar si no es un número entero
                    messagebox.showinfo("Ingrese un número")
                    ingresar_palabra()
            else:
                messagebox.showinfo("Rellene los espacios")
                ingresar_palabra()
            break 


# Ejecutar la función
    tercera_ventana.mainloop()

def salir():
    pass
