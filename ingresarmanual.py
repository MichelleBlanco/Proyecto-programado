import tkinter as tk
from tkinter import messagebox
import unicodedata
import subprocess

# Variables globales
matriz_1 = []
matriz_1_btn = []
matriz_2 = []  # Matriz para la segunda cara (Y-Z)
matriz_2_btn = []
definiciones = []
total_palabras = []
palabras_lista = []
diccionario_general = {}
diccionario_1 = []

def habilitar_controles():
    """Habilita los controles de la interfaz gráfica."""
    btn_agregar_palabra1.config(state="normal")
    btn_agregar_palabra_2.config(state="normal")
    btn_terminar.config(state="normal")

def crear_crucigrama():
    """Crea un crucigrama según el tamaño especificado en la entrada.
    
    Obtiene el tamaño de la matriz del campo de entrada, crea dos matrices
    de botones en la interfaz gráfica, y habilita los controles.
    
    Raises:
        ValueError: Si el tamaño no es un número entero.
    """
    # Obtener el tamaño de la matriz
    try:
        size = int(entrada_size.get())
    except ValueError:
        messagebox.showerror("Error", "Debe rellenar el espacio y debe ser un número entero.")
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


def lista(matriz_1, matriz_2, palabras, definicion, fila, columna, orientacion):
    """Agrega una palabra y su definición a una lista de palabras.

       Args:
           matriz_1 (list): La primera matriz (cara X-Y).
           matriz_2 (list): La segunda matriz (cara Y-Z).
           palabras (list): Lista de palabras.
           definicion (str): Definición de la palabra.
           fila (int): Fila donde se colocará la palabra.
           columna (int): Columna donde se colocará la palabra.
           orientacion (str): Orientación de la palabra ("H" para horizontal, "V" para vertical).

       Returns:
           None
       """
    if matriz_1:
        if orientacion == "H":
            pos_x = columna
            pos_y = fila
            pos_z = 0
            letra_direccion = "X"  
        elif orientacion == "V":
            pos_x = columna
            pos_y = fila
            pos_z = 0
            letra_direccion = "Y"  

    elif matriz_2: 
        if orientacion == "H":
            pos_x = 0
            pos_y = fila
            pos_z = columna
            letra_direccion = "X"  
        elif orientacion == "V":
            pos_x = 0
            pos_y = fila
            pos_z = columna
            letra_direccion = "Y"
    
    # Aquí define tus matrices y otras variables necesarias
    matriz_1 = matriz_1
    matriz_2 = matriz_2
    definicion = entrada_definicion.get()
    fila = entrada_fila.get()  # Define cómo obtienes esta posición
    columna = entrada_columna.get()  # Define cómo obtienes esta posición
    orientacion = letra_direccion  # Define la orientación (horizontal/vertical)

    # Obtener definición y palabra de las entradas
    definicion = entrada_definicion.get()
    palabra = entrada_palabra.get().upper()  # Asegurarse de que la palabra esté en mayúsculas
    
    palabra_con_tilde = entrada_palabra.get() and palabra # Obtiene la palabra desde el Entry
    palabra_procesada = quitar_tildes(palabra_con_tilde)
        
    # Crear un diccionario para la nueva palabra
    diccionario_palabra = {
        "Longitud palabra": len(palabra_procesada), 
        "Palabra": palabra_procesada,
        "Longitud definición": len(definicion),
        "Definición": definicion,
        "Posición x": pos_x,
        "Posición y": pos_y,
        "Posición z": pos_z,
        "Dirección": letra_direccion
    }

    # Agregar el diccionario de la nueva palabra a la lista
    palabras_lista.append(diccionario_palabra)

def verificar_matrices(palabra, definicion, orientacion, matriz, matriz_btn):
    """Verifica si una palabra se puede agregar a la matriz y la agrega si es posible.
    
    Args:
        palabra (str): La palabra a agregar.
        definicion (str): La definición de la palabra.
        orientacion (str): La orientación de la palabra ("H" para horizontal, "V" para vertical).
        matriz (list): La matriz en la que se intentará agregar la palabra.
        matriz_btn (list): La matriz de botones correspondiente a la matriz.

    Returns:
        None
    """  
    palabra = entrada_palabra.get().upper()
    definicion = entrada_definicion.get()
    orientacion = var_orientacion.get() 
    fila = entrada_fila.get()
    columna = entrada_columna.get()

    try:
        fila = int(entrada_fila.get())
        columna = int(entrada_columna.get())
    except ValueError:
        messagebox.showerror("Error", "La fila y columna deben ser números.")
        return
    
    if not palabra or not definicion:
        messagebox.showerror("Error", "Debe rellenar todos los espacios.")
        return

    # Verificar si alguna de las matrices tiene una palabra
    if any(any(celda != "" for celda in fila) for fila in matriz_1) or any(any(celda != "" for celda in fila) for fila in matriz_2):
        # Llamar a la función agregar_palabra
        agregar_palabra(palabra, definicion, orientacion, matriz, matriz_btn)
    
    else:
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
    try:   # Actualizar diccionario y sincronizar matrices
        total_palabras.append(palabra_procesada)
        sincronizar_columnas()

        lista(matriz_1, matriz_2, palabra_procesada, definicion, fila, columna, orientacion)

        # Agregar la definición
        definiciones.append(f"{len(definiciones) + 1}) {definicion}")
        lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")
    except:
        pass

def sincronizar_columnas():
    """Sincroniza las letras entre la última columna de la primera matriz y la primera columna de la segunda matriz.
    
    Args:
        None

    Returns:
        None
    """
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
    """Agrega una palabra a la matriz de crucigramas.

    Args:
        palabra (str): La palabra a agregar.
        definicion (str): La definición de la palabra.
        orientacion (str): La orientación de la palabra ("H" para horizontal, "V" para vertical).
        matriz (list): La matriz en la que se agregará la palabra.
        matriz_btn (list): La representación de botones de la matriz.

    Returns:
        None
    """
    # Inicializa la variable interseccion_encontrada
    interseccion_encontrada = False

    # Supongamos que fila y columna son obtenidos de las entradas
    fila = int(entrada_fila.get())
    columna = int(entrada_columna.get())
    
    palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
    palabra_procesada = quitar_tildes(palabra_con_tilde)
    

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
        if fila + len(palabra_procesada) > len(matriz):
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
    total_palabras.append(palabra_procesada)

    # Agregar la definición
    definiciones.append(f"{len(definiciones) + 1}) {definicion}")
    lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")
    lista(matriz_1, matriz_2, palabra_procesada, definicion, fila, columna, orientacion)

def quitar_tildes(palabra):
    """Elimina las tildes de una palabra.
    
    Args:
        palabra (str): La palabra de la cual se eliminarán las tildes.
    
    Returns:
        str: La palabra sin tildes.
    """
    # Eliminar tildes y otros diacríticos
    palabra_sin_tildes = ''.join((c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'))
    palabra_mayuscula = palabra_sin_tildes.upper()
    return palabra_mayuscula

from crear_crucigrama import diccionario_general
# Diccionario global
diccionario_general = {"palabras": diccionario_general }

def terminar(diccionario_1, palabras_lista):
    """Finaliza el proceso de creación del crucigrama y guarda la información.

    Args:
        diccionario_1 (dict): Diccionario que contiene la información del crucigrama.
        palabras_lista (list): Lista de palabras del crucigrama.

    Returns:
        None
    """
    numero_palabras = len(total_palabras)
    # Obtener dimensiones de la matriz
    tamaño_x = len(matriz_1)
    tamaño_y = len(matriz_1[0]) if matriz_1 else 0
    tamaño_z = len(matriz_2[0]) if matriz_2 else 0 
    version = entrada_version.get()
    # Crear un diccionario para la nueva palabra
    diccionario_1 = {
        "Versión": version,
        "Dimensión x": tamaño_x,
        "Dimensión y": tamaño_y,
        "Dimensión z": tamaño_z,
        "Número de palabras": numero_palabras,
    }
    diccionario_1 ["palabras"] = palabras_lista
    diccionario_general = diccionario_1 
    print(diccionario_general)
    root.destroy()    
    subprocess.run(["python", "menu.py"])
    guardar_crucigrama(diccionario_general)

from crear_crucigrama import nombre
num=nombre[0]
def guardar_crucigrama(diccionario_general):
    """Guarda el crucigrama en un archivo binario.

    Args:
        diccionario_general (dict): Diccionario que contiene la información del crucigrama.

    Returns:
        None
    """
    with open(f"{num}.c3d", "wb") as mi_archivo:
        mi_archivo.write(int(diccionario_general["Versión"]).to_bytes(1, byteorder="big", signed=False))
        mi_archivo.write(int(diccionario_general["Dimensión x"]).to_bytes(4,byteorder="big", signed=False))
        mi_archivo.write(int(diccionario_general["Dimensión y"]).to_bytes(4,byteorder="big", signed=False))
        mi_archivo.write(int(diccionario_general["Dimensión z"]).to_bytes(4,byteorder="big", signed=False))
        mi_archivo.write(int(diccionario_general["Número de palabras"]).to_bytes(4,byteorder="big", signed=False))

        # Para cada palabra en el crucigrama, escribir longitud, palabra, definición, posición y dirección
        for palabra in diccionario_general["palabras"]:
             # Codificar la palabra y definición en bytes
                palabra_codificada = palabra['Palabra'].encode('utf-8')
                definicion_codificada = palabra['Definición'].encode('utf-8')
                direccion_codificada = palabra['Dirección'].encode('utf-8')

                # Escribir la longitud de la palabra (1 byte)
                mi_archivo.write(len(palabra_codificada).to_bytes(1, byteorder="big", signed=False))

                # Escribir la palabra (n bytes, longitud de la palabra en bytes)
                mi_archivo.write(palabra_codificada)

                # Escribir la longitud de la definición (2 bytes)
                mi_archivo.write(len(definicion_codificada).to_bytes(2, byteorder="big", signed=False))

                # Escribir la definición (n bytes, longitud de la definición en bytes)
                mi_archivo.write(definicion_codificada)

                # Escribir la posición inicial en el espacio 3D: X, Y, Z (4 bytes cada una)
                mi_archivo.write(int(palabra['Posición x']).to_bytes(4, byteorder="big", signed=False))
                mi_archivo.write(int(palabra['Posición y']).to_bytes(4, byteorder="big", signed=False))
                mi_archivo.write(int(palabra['Posición z']).to_bytes(4, byteorder="big", signed=False))

                # Escribir la longitud de la dirección (1 byte)
                mi_archivo.write(len(direccion_codificada).to_bytes(1, byteorder="big", signed=False))

                # Escribir la dirección (n bytes, longitud de la dirección en bytes)
                mi_archivo.write(direccion_codificada)

        mi_archivo.close()


def alternar_vista():
    """Alterna entre las dos vistas de las matrices.

    Args:
        None

    Returns:
        None
    """
    if frame_matriz_1.winfo_viewable():
        frame_matriz_1.grid_remove()
        frame_matriz_2.grid(row=0, column=0)
    else:
        frame_matriz_2.grid_remove()
        frame_matriz_1.grid(row=0, column=0)

# Crear la ventana principal
root = tk.Tk()
root.title("Creador de Crucigrama")
root.geometry("1550x900")

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

tk.Label(frame_controles, text="Versión:").grid(row=1, column=0, sticky="w")
entrada_version = tk.Entry(frame_controles)
entrada_version.grid(row=1, column=1)

# Botón para crear la matriz
btn_crear = tk.Button(frame_controles, text="Crear Crucigrama", command=crear_crucigrama)
btn_crear.grid(row=0, column=2)

# Botón para alternar la vista (girar)
btn_girar = tk.Button(frame_controles, text="Girar", command=alternar_vista)
btn_girar.grid(row=1, column=2)

# Entrada para agregar palabra y definición
tk.Label(frame_controles, text="Palabra:").grid(row=2, column=0, sticky="w")
entrada_palabra = tk.Entry(frame_controles)
entrada_palabra.grid(row=2, column=1)

tk.Label(frame_controles, text="Definición:").grid(row=3, column=0, sticky="w")
entrada_definicion = tk.Entry(frame_controles)
entrada_definicion.grid(row=3, column=1)

tk.Label(frame_controles, text="Fila:").grid(row=4, column=0, sticky="w")
entrada_fila = tk.Entry(frame_controles)
entrada_fila.grid(row=4, column=1)

tk.Label(frame_controles, text="Columna:").grid(row=5, column=0, sticky="w")
entrada_columna = tk.Entry(frame_controles)
entrada_columna.grid(row=5, column=1)

# Orientación de la palabra
var_orientacion = tk.StringVar(value="H")
tk.Radiobutton(frame_controles, text="Horizontal", variable=var_orientacion, value="H").grid(row=7, column=0, sticky="w")
tk.Radiobutton(frame_controles, text="Vertical", variable=var_orientacion, value="V").grid(row=8, column=0, sticky="w")


# Botón para agregar palabra a la primera matriz
btn_agregar_palabra1 = tk.Button(frame_controles, text="Agregar Palabra Cara X-Y", command=lambda: verificar_matrices(entrada_palabra.get().upper(), 
                                                                        entrada_definicion.get(), 
                                                                        var_orientacion.get(), 
                                                                        matriz_1, 
                                                                        matriz_1_btn), state="disabled")
btn_agregar_palabra1.grid(row=7, column=1)

# Botón para agregar palabra a la segunda matriz
btn_agregar_palabra_2 = tk.Button(frame_controles, text="Agregar Palabra Cara Y-Z", command=lambda: verificar_matrices(entrada_palabra.get().upper(), 
                                                                          entrada_definicion.get(), 
                                                                          var_orientacion.get(), 
                                                                          matriz_2, 
                                                                          matriz_2_btn), state="disabled")
btn_agregar_palabra_2.grid(row=8, column=1)


# Botón para terminar el juego
btn_terminar = tk.Button(frame_controles, text="Terminar", command=lambda: terminar(diccionario_1, palabras_lista), state="disabled")
btn_terminar.grid(row=9, column=0, columnspan=2)

# Lista para mostrar las definiciones
lista_definiciones = tk.Listbox(frame_controles)
lista_definiciones.grid(row=10, column=0, columnspan=2)

root.mainloop()