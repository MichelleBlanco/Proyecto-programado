import tkinter as tk
from tkinter import messagebox
import unicodedata

# Variables globales
matriz_1 = []
matriz_1_btn = []
matriz_2 = []  # Matriz para la segunda cara (Y-Z)
matriz_2_btn = []
definiciones = []

def habilitar_controles():
    btn_agregar_palabra1.config(state="normal")
    btn_agregar_palabra_2.config(state="normal")
    btn_terminar.config(state="normal")

def crear_crucigrama():
    # Obtener el tamaño de la matriz
    try:
        size = int(entrada_size.get())
    except ValueError:
        messagebox.showerror("Error", "El tamaño debe ser un número entero.")
        return
    
    # Eliminar el campo de entrada y el botón para evitar cambios posteriores
    entrada_size.destroy()
    btn_crear.destroy()

    # Limpiar la cuadrícula anterior si existe
    for widget in frame_matriz_1.winfo_children():
        widget.destroy()
    for widget in frame_matriz_2.winfo_children():
        widget.destroy()
        
    matriz_1.clear()
    matriz_1_btn.clear()
    matriz_2.clear()
    matriz_2_btn.clear()
    definiciones.clear()
    
    # Crear la primera matriz (cara X-Y)
    for i in range(size):
        fila = [""] * size
        fila_btn = []
        for j in range(size):
            btn = tk.Button(frame_matriz_1, text="", width=4, height=2)
            btn.grid(row=i, column=j)
            fila_btn.append(btn)
        matriz_1.append(fila)
        matriz_1_btn.append(fila_btn)

    # Crear la segunda matriz (cara Y-Z)
    for i in range(size):
        fila = [""] * size
        fila_btn = []
        for j in range(size):
            btn = tk.Button(frame_matriz_2, text="", width=4, height=2)
            btn.grid(row=i, column=j)
            fila_btn.append(btn)
        matriz_2.append(fila)
        matriz_2_btn.append(fila_btn)

    # Habilitar controles después de definir el tamaño
    habilitar_controles()

def verificar_matrices(palabra, definicion, orientacion, matriz, matriz_btn):
    
    palabra = entrada_palabra.get().upper()
    definicion = entrada_definicion.get()
    orientacion = var_orientacion.get() 
    fila = entrada_fila.get()
    columna = entrada_columna.get()

    if not palabra or not definicion or not definicion or not fila or not columna:
        messagebox.showerror("Error", "Debe rellenar todos los espacios.")
        return

    # Verificar si alguna de las matrices tiene una palabra
    if any(any(celda != "" for celda in fila) for fila in matriz_1) or any(any(celda != "" for celda in fila) for fila in matriz_2):
        # Llamar a la función agregar_palabra
        agregar_palabra(palabra, definicion, orientacion, matriz, matriz_btn)
    
    else:
        # Supongamos que fila y columna son obtenidos de las entradas
        fila = int(entrada_fila.get())
        columna = int(entrada_columna.get())

        # Verificar si la palabra cabe en la posición seleccionada
        if orientacion == "H":
            if columna + len(palabra) > len(matriz[0]):
                messagebox.showerror("Error", "La palabra no cabe en la posición seleccionada.")
                return
        elif orientacion == "V":
            if fila + len(palabra) > len(matriz):
                messagebox.showerror("Error", "La palabra no cabe en la posición seleccionada.")
                return
        
        palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
        palabra_procesada = quitar_tildes(palabra_con_tilde)
        print(palabra_procesada)

        # Verificar si hay conflicto y buscar intersecciones
        for idx, letra in enumerate(palabra_procesada):
            if orientacion == "H":
                pos_actual = matriz[fila][columna + idx]
                if pos_actual != "" and pos_actual != letra:
                    messagebox.showerror("Error", f"Conflicto en la posición ({fila}, {columna + idx}).")
                    return
                
            elif orientacion == "V":
                pos_actual = matriz[fila + idx][columna]
                if pos_actual != "" and pos_actual != letra:
                    messagebox.showerror("Error", f"Conflicto en la posición ({fila + idx}, {columna}).")
                    return
            
        # Colocar la palabra en la matriz
        for idx, letra in enumerate(palabra_procesada):
            if orientacion == "H":
                matriz[fila][columna + idx] = letra
                matriz_btn[fila][columna + idx]["text"] = letra
            elif orientacion == "V":
                matriz[fila + idx][columna] = letra
                matriz_btn[fila + idx][columna]["text"] = letra
        sincronizar_columnas()

        # Agregar la definición
        definiciones.append(f"{len(definiciones) + 1}) {definicion}")
        lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")

def sincronizar_columnas():
    # Sincronizar de la última columna de X-Y a la primera columna de Z-Y
    for fila in range(len(matriz_1)):
        letra_xy = matriz_1[fila][-1]  # Última columna de X-Y
        letra_zy = matriz_2[fila][0]  # Primera columna de Z-Y
        
        # Copiar de X-Y a Z-Y si la letra existe y no hay conflicto
        if letra_xy != "" and (letra_zy == "" or letra_zy == letra_xy):
            matriz_2[fila][0] = letra_xy
            matriz_2_btn[fila][0]["text"] = letra_xy  # Actualizar el botón en Z-Y
        
        # Copiar de Z-Y a X-Y si la letra existe y no hay conflicto
        if letra_zy != "" and (letra_xy == "" or letra_xy == letra_zy):
            matriz_1[fila][-1] = letra_zy
            matriz_1_btn[fila][-1]["text"] = letra_zy  # Actualizar el botón en X-Y
            
def agregar_palabra(palabra, definicion, orientacion, matriz, matriz_btn):
    
    # Inicializa la variable interseccion_encontrada
    interseccion_encontrada = False

    # Supongamos que fila y columna son obtenidos de las entradas
    fila = int(entrada_fila.get())
    columna = int(entrada_columna.get())
    
    palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
    palabra_procesada = quitar_tildes(palabra_con_tilde)
    print(palabra_procesada)

    # Verificar si la palabra o la definición ya existen
    for defin in definiciones:
        if definicion in defin:
            messagebox.showerror("Error", "La definición ya existe.")
            return
    
    for idx_fila in matriz:
        if palabra in "".join(idx_fila):
            messagebox.showerror("Error", "La palabra ya existe en el crucigrama.")
            return
    
    # Verificar si la palabra cabe en la posición seleccionada
    if orientacion == "H":
        if columna + len(palabra_procesada) > len(matriz[0]):
            messagebox.showerror("Error", "La palabra no cabe en la posición seleccionada.")
            return
    elif orientacion == "V":
        if fila + len(palabra) > len(matriz):
            messagebox.showerror("Error", "La palabra no cabe en la posición seleccionada.")
            return# Aquí continúa tu lógica para agregar la palabra

    # Fase 1: Verificar intersecciones y conflictos sin modificar la matriz
    for idx, letra in enumerate(palabra_procesada):
        if orientacion == "H":
            pos_actual = matriz[fila][columna + idx]
            if pos_actual != "":  # Si hay algo en la posición
                if pos_actual == letra:  # Si es una intersección válida
                    interseccion_encontrada = True
                else:  # Conflicto: no es la misma letra
                    messagebox.showerror("Error", f"Conflicto en la posición ({fila}, {columna + idx}).")
                    return
        elif orientacion == "V":
            pos_actual = matriz[fila + idx][columna]
            if pos_actual != "":  # Si hay algo en la posición
                if pos_actual == letra:  # Si es una intersección válida
                    interseccion_encontrada = True
                else:  # Conflicto: no es la misma letra
                    messagebox.showerror("Error", f"Conflicto en la posición ({fila + idx}, {columna}).")
                    return

    # Si no se encontró ninguna intersección válida
    if not interseccion_encontrada:
        messagebox.showerror("Error", "No existe una intersección válida para la palabra.")
        return

    # Colocar la palabra en la matriz
    for idx, letra in enumerate(palabra_procesada):
        if orientacion == "H":
            matriz[fila][columna + idx] = letra
            matriz_btn[fila][columna + idx]["text"] = letra
        elif orientacion == "V":
            matriz[fila + idx][columna] = letra
            matriz_btn[fila + idx][columna]["text"] = letra
    sincronizar_columnas()
    
    # Agregar la definición
    definiciones.append(f"{len(definiciones) + 1}) {definicion}")
    lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")

def quitar_tildes(palabra):
    # Eliminar tildes y otros diacríticos
    palabra_sin_tildes = ''.join(
        (c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn')
    )
    palabra_mayuscula = palabra_sin_tildes.upper()
    return palabra_mayuscula

def terminar():
    # Mostrar las letras de la matriz
    for fila in matriz_1:
        for btn in fila:
            btn["text"] = ""  # Las letras quedan ocultas para resolver

    btn_terminar.config(state=tk.DISABLED)
#def terminar_crucigrama():
 #   total_palabras = len(palabras_agregadas)
  #  messagebox.showinfo("Total de Palabras", f"Total de palabras agregadas: {total_palabras}")

def alternar_vista():
    if frame_matriz_1.winfo_viewable():
        frame_matriz_1.grid_remove()
        frame_matriz_2.grid(row=0, column=0)
    else:
        frame_matriz_2.grid_remove()
        frame_matriz_1.grid(row=0, column=0)


# Crear la ventana principal
root = tk.Tk()
root.title("Creador de Crucigrama")

# Frame para la primera matriz (X-Y)
frame_matriz_1 = tk.Frame(root)
frame_matriz_1.grid(row=0, column=0, padx=10, pady=10)

# Frame para la segunda matriz (Y-Z)
frame_matriz_2 = tk.Frame(root)

# Panel de control
frame_controles = tk.Frame(root)
frame_controles.grid(row=0, column=1, padx=10, pady=10)

# Entrada para definir el tamaño de la matriz
tk.Label(frame_controles, text="Tamaño de la matriz:").grid(row=0, column=0, sticky="w")
entrada_size = tk.Entry(frame_controles)
entrada_size.grid(row=0, column=1)

# Botón para crear la matriz
btn_crear = tk.Button(frame_controles, text="Crear Crucigrama", command=crear_crucigrama)
btn_crear.grid(row=0, column=2)

# Botón para alternar la vista (girar)
btn_girar = tk.Button(frame_controles, text="Girar", command=alternar_vista)
btn_girar.grid(row=1, column=2)
# Entrada para agregar palabra y definición
tk.Label(frame_controles, text="Palabra:").grid(row=1, column=0, sticky="w")
entrada_palabra = tk.Entry(frame_controles)
entrada_palabra.grid(row=1, column=1)

tk.Label(frame_controles, text="Definición:").grid(row=2, column=0, sticky="w")
entrada_definicion = tk.Entry(frame_controles)
entrada_definicion.grid(row=2, column=1)

tk.Label(frame_controles, text="Fila:").grid(row=3, column=0, sticky="w")
entrada_fila = tk.Entry(frame_controles)
entrada_fila.grid(row=3, column=1)

tk.Label(frame_controles, text="Columna:").grid(row=4, column=0, sticky="w")
entrada_columna = tk.Entry(frame_controles)
entrada_columna.grid(row=4, column=1)

# Orientación de la palabra
var_orientacion = tk.StringVar(value="H")
tk.Radiobutton(frame_controles, text="Horizontal", variable=var_orientacion, value="H").grid(row=5, column=0, sticky="w")
tk.Radiobutton(frame_controles, text="Vertical", variable=var_orientacion, value="V").grid(row=6, column=0, sticky="w")


# Botón para agregar palabra a la primera matriz
btn_agregar_palabra1 = tk.Button(frame_controles, text="Agregar Palabra Cara X-Y", command=lambda: verificar_matrices(entrada_palabra.get().upper(), 
                                                                        entrada_definicion.get(), 
                                                                        var_orientacion.get(), 
                                                                        matriz_1, 
                                                                        matriz_1_btn), state="disabled")
btn_agregar_palabra1.grid(row=5, column=1)

# Botón para agregar palabra a la segunda matriz
btn_agregar_palabra_2 = tk.Button(frame_controles, text="Agregar Palabra Cara Y-Z", command=lambda: verificar_matrices(entrada_palabra.get().upper(), 
                                                                          entrada_definicion.get(), 
                                                                          var_orientacion.get(), 
                                                                          matriz_2, 
                                                                          matriz_2_btn), state="disabled")
btn_agregar_palabra_2.grid(row=6, column=1)


# Botón para terminar el juego
btn_terminar = tk.Button(frame_controles, text="Terminar", command=terminar, state="disabled")
btn_terminar.grid(row=8, column=0, columnspan=2)

# Lista para mostrar las definiciones
lista_definiciones = tk.Listbox(frame_controles)
lista_definiciones.grid(row=9, column=0, columnspan=2)

# Ejecutar la aplicación
root.mainloop()
