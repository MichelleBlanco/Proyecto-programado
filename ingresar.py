import tkinter as tk
from tkinter import messagebox

def ingresar_palabra():
    lista_palabras = []  # Lista para almacenar las palabras y definiciones
    lista_usar = [] 
    letras_divididas = []
    numero = 1  

    # Crear una nueva ventana secundaria
    tercera_ventana = tk.Toplevel()
    tercera_ventana.title("Añadir palabras")
    tercera_ventana.geometry("1558x900") 

    while True:
        label = tk.Label(tercera_ventana, text= f"Ingrese la palabra #{numero}: ", font=("Courier", 30),bg="lightblue", fg="black")
        label.pack(pady=20)


        entrada_nombre = tk.Entry(tercera_ventana, fg='grey')
        entrada_nombre.pack(pady=25)
       
        #BOTONES
        create_button = tk.Button(tercera_ventana, text="Crear Crucigrama", width=18, command=salir, font=("Courier", 14), bg="lightblue")
        create_button.pack(pady=30)

        if label != "":
            while True:
                definicion = input(f"Escriba la definición de '{label}': ")
                if definicion == "": 
                    print("Debe ingresar una definición")
                else:
                    lista_palabras.append([numero, label, definicion])
                    lista_usar.append([label])
                     
                    break  # Salimos del bucle solo si hay una definición válida
            numero += 1
        
        else:
            label = tk.Label(tercera_ventana, text= f"Debe ingresar una palabra", font=("Courier", 30),bg="lightblue", fg="black")
            label.pack(pady=20)
            messagebox.showinfo("No se ha ingresado ninguna palabra.")
            

        for sublista in lista_usar:
            palabra = sublista[0]  # Tomar la primera (y única) palabra de la sublista
            letras = list(palabra)  # Convertir la palabra en una lista de letras
            letras_divididas.append(letras)
    
        if lista_palabras:
            print("\nLista de palabras y definiciones:")
            for item in lista_palabras:
                print(f"{item[0]}. Palabra: {item[1]}, Definición: {item[2]}")
                
        else:
            messagebox.showinfo("No se ingresaron palabras.")

# Ejecutar la función
        tercera_ventana.mainloop()

def salir():
    pass
