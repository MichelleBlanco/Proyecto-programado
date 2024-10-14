import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import unicodedata
import subprocess

# Variables globales
matriz = []
matriz_btn = []
matriz_2 = []  # Matriz para la segunda cara (Y-Z)
matriz_2_btn = []
definiciones = []
palabras_agregadas = set()
definiciones_agregadas = set()
total_palabras = []
palabras_lista = []
diccionario_general = {}
diccionario_1 = []

# Función para habilitar controles
def habilitar_controles():
    """Habilita los campos de entrada y botones después de definir el tamaño de la matriz."""
    entrada_palabra.config(state="normal")
    entrada_definicion.config(state="normal")
    entrada_orientacion.config(state="normal")
    btn_agregar_palabra.config(state="normal")
    btn_terminar.config(state="normal")

def crear_crucigrama():
    """Crea un crucigrama con el tamaño especificado por el usuario.
    Obtiene el tamaño de la matriz a partir de la entrada del usuario, crea dos matrices 
    (cara X-Y y cara Y-Z) y habilita los controles necesarios para agregar palabras.
    
    Args: 
        None

    Returns:
        None
    """
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
    for widget in frame_matriz.winfo_children():
        widget.destroy()
    for widget in frame_matriz_2.winfo_children():
        widget.destroy()
        
    matriz.clear()
    matriz_btn.clear()
    matriz_2.clear()
    matriz_2_btn.clear()
    definiciones.clear()
    
    # Crear la primera matriz (cara X-Y)
    for i in range(size):
        fila = [""] * size
        fila_btn = []
        for j in range(size):
            btn = tk.Button(frame_matriz, text="", width=4, height=2)
            btn.grid(row=i, column=j)
            fila_btn.append(btn)
        matriz.append(fila)
        matriz_btn.append(fila_btn)

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

    frame_matriz.update_idletasks()
    frame_matriz_2.update_idletasks()

    # Habilitar controles después de definir el tamaño
    habilitar_controles()

def lista(matriz, matriz_2, palabras, definicion, fila, columna, orientacion):
    """Agrega una palabra a la lista de palabras con su definición y posición.

    Args:
        matriz (list): La matriz donde se desea agregar la palabra.
        matriz_2 (list): La segunda matriz para la cara Y-Z.
        palabras (list): La lista de palabras.
        definicion (str): La definición de la palabra.
        fila (int): La fila donde se colocará la palabra.
        columna (int): La columna donde se colocará la palabra.
        orientacion (str): La orientación de la palabra ("H" para horizontal, "V" para vertical).

    Returns:
        None
    """
    if matriz:
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
    matriz = matriz
    matriz_2 = matriz_2
    definicion = entrada_definicion.get()
    ###fila = entrada_fila.get()  # Define cómo obtienes esta posición
    ###columna = entrada_columna.get()  # Define cómo obtienes esta posición
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

# Función para verificar si una palabra cabe en la posición seleccionada
def puede_colocar_palabra(palabra, fila, columna, orientacion, matriz):
    """Verifica si una palabra cabe en la posición seleccionada de la matriz.
    
    Args:
        palabra (str): La palabra que se desea colocar.
        fila (int): La fila donde se intenta colocar la palabra.
        columna (int): La columna donde se intenta colocar la palabra.
        orientacion (str): La orientación de la palabra ("horizontal" o "vertical").
        matriz (list): La matriz donde se intenta colocar la palabra.
        
    Returns:
        bool: True si la palabra puede ser colocada, False en caso contrario.
    """
    longitud_palabra = len(palabra)
    if orientacion == 'horizontal':
        if columna + longitud_palabra > len(matriz[fila]):
            return False
    elif orientacion == 'vertical':
        if fila + longitud_palabra > len(matriz):
            return False
    return True

def quitar_tildes(palabra):
    """Elimina las tildes y otros diacríticos de una palabra.
    
    Args:
        palabra (str): La palabra de la cual se eliminarán las tildes.
        
    Returns:
        str: La palabra sin tildes en mayúsculas.
    """
    # Eliminar tildes y otros diacríticos
    palabra_sin_tildes = ''.join((c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'))
    palabra_mayuscula = palabra_sin_tildes.upper()
    return palabra_mayuscula

def encontrar_interseccion(palabra, matriz, orientacion):
    """Encuentra las posiciones posibles donde una palabra puede intersectar con letras en la matriz.

    Args:
        palabra (str): La palabra que se desea colocar.
        matriz (list): La matriz donde se busca la intersección.
        orientacion (str): La orientación de la palabra ("H" para horizontal, "V" para vertical).
        
    Returns:
        list: Una lista de tuplas con las posiciones (fila, columna, orientación) donde se puede colocar la palabra.
    """
    posiciones_posibles = []
    longitud_palabra = len(palabra)

    # Recorrer la matriz en busca de posibles intersecciones (letras en común)
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            letra_en_matriz = matriz[fila][columna]
            
            # Intentar encontrar una letra común entre la palabra y la matriz
            for idx_palabra, letra in enumerate(palabra):
                if letra_en_matriz == letra:
                    # Si la letra en la matriz coincide con la letra en la palabra
                    # Intentar colocar horizontalmente (orientacion == "H")
                    if orientacion == "H":
                        inicio_columna = columna - idx_palabra
                        if inicio_columna >= 0 and inicio_columna + longitud_palabra <= len(matriz[0]):
                            # Verificar que todo el espacio esté disponible y coincida
                            puede_colocar = True
                            for i in range(longitud_palabra):
                                letra_actual = palabra[i]
                                if matriz[fila][inicio_columna + i] not in ("", letra_actual):
                                    puede_colocar = False
                                    break
                            if puede_colocar:
                                posiciones_posibles.append((fila, inicio_columna, 0))  # Z=0 para X-Y

                    # Intentar colocar verticalmente (orientacion == "V")
                    elif orientacion == "V":
                        inicio_fila = fila - idx_palabra
                        if inicio_fila >= 0 and inicio_fila + longitud_palabra <= len(matriz):
                            # Verificar que todo el espacio esté disponible y coincida
                            puede_colocar = True
                            for i in range(longitud_palabra):
                                letra_actual = palabra[i]
                                if matriz[inicio_fila + i][columna] not in ("", letra_actual):
                                    puede_colocar = False
                                    break
                            if puede_colocar:
                                posiciones_posibles.append((inicio_fila, columna, 0))  # Z=0 para X-Y

    # Si no se encontraron posiciones válidas, retornar una lista vacía
    return posiciones_posibles


# Función para colocar palabra con intersección
def colocar_palabra_interseccion(palabra, definicion, orientacion, matriz, matriz_btn):
    """Coloca una palabra en la matriz, verificando si puede intersecar con palabras ya existentes.

    Args:
        palabra (str): La palabra a colocar en la matriz.
        definicion (str): La definición de la palabra.
        orientacion (str): La orientación en la que se colocará la palabra ('H' para horizontal, 'V' para vertical).
        matriz (list): La matriz donde se colocará la palabra.
        matriz_btn (list): La matriz de botones correspondiente a la visualización de la matriz.

    Returns:
        bool: True si la palabra fue colocada correctamente, False en caso contrario.
    """
    if palabra in palabras_agregadas or definicion in definiciones_agregadas:
        messagebox.showerror("Error", "La palabra o la definición ya han sido agregadas.")
        return
    
    if not palabras_agregadas:
        fila = random.randint(0, len(matriz) - 1)
        columna = random.randint(0, len(matriz[0]) - 1)

        if orientacion == "H":
            if columna + len(palabra) > len(matriz[0]):
                columna = len(matriz[0]) - len(palabra)
        elif orientacion == "V":
            if fila + len(palabra) > len(matriz):
                fila = len(matriz) - len(palabra)

        if puede_colocar_palabra(palabra, fila, columna, orientacion, matriz):
            palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
            palabra_procesada = quitar_tildes(palabra_con_tilde)
            
            ##
            palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
            palabra_procesada = quitar_tildes(palabra_con_tilde)

            if palabra in palabras_agregadas or definicion in definiciones_agregadas:
                messagebox.showerror("Error", "La palabra o la definición ya han sido agregadas.")
                return False  # Retorna False si la palabra ya está

            # Inicializa la variable que indica si se colocó correctamente
            palabra_colocada_correctamente = False
            if puede_colocar_palabra(palabra, fila, columna, orientacion, matriz):
                for idx, letra in enumerate(palabra_procesada):
                    if orientacion == "H":
                        matriz[fila][columna + idx] = letra
                        matriz_btn[fila][columna + idx]["text"] = letra
                    elif orientacion == "V":
                        matriz[fila + idx][columna] = letra
                        matriz_btn[fila + idx][columna]["text"] = letra
            label_numero = tk.Label(matriz_btn[fila][columna], text=f"{len(definiciones) + 1}", font=("Arial", 6))
            label_numero.place(x=4, y=4)
            
            definiciones.append(f"{len(definiciones) + 1}) {definicion}")
            lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")
            palabras_agregadas.add(palabra_procesada)
            definiciones_agregadas.add(definicion)
            
            palabra_colocada_correctamente = True  # Marca que se colocó correctamente

            if not palabra_colocada_correctamente:
                messagebox.showerror("Error", "No se puede colocar la palabra en esa posición.")
            return palabra_colocada_correctamente  # Retorna si la palabra fue colocada correctamente

        else:
            messagebox.showerror("Error", "No se puede colocar la palabra en esa posición.")
    else:
        posiciones_posibles = encontrar_interseccion(palabra, matriz, orientacion)
        if not posiciones_posibles:
            messagebox.showinfo("Sin intersección", "No hay intersección válida para colocar la palabra.")
            return

        posiciones_filtradas = [(fila, columna, orientacion_interseccion) 
                                for fila, columna, orientacion_interseccion in posiciones_posibles 
                                if orientacion_interseccion == orientacion]
        
        if not posiciones_filtradas:
            messagebox.showinfo("Sin intersección", "No hay intersección válida con la orientación seleccionada.")
            return

        fila, columna, _ = random.choice(posiciones_filtradas)
        palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
        palabra_procesada = quitar_tildes(palabra_con_tilde)
        # Inicializa la variable que indica si se colocó correctamente
        palabra_colocada_correctamente = False
        if puede_colocar_palabra(palabra, fila, columna, orientacion, matriz):
            for idx, letra in enumerate(palabra_procesada):
                if orientacion == "H":
                    matriz[fila][columna + idx] = letra
                    matriz_btn[fila][columna + idx]["text"] = letra
                elif orientacion == "V":
                    matriz[fila + idx][columna] = letra
                    matriz_btn[fila + idx][columna] = letra

        definiciones.append(f"{len(definiciones) + 1}) {definicion}")
        lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")
        palabras_agregadas.add(palabra_procesada)
        definiciones_agregadas.add(definicion)
        sincronizar_matrices()
        palabra_colocada_correctamente = True  # Marca que se colocó correctamente
        if not palabra_colocada_correctamente:
            messagebox.showerror("Error", "No se puede colocar la palabra en esa posición.")
        return palabra_colocada_correctamente  # Retorna si la palabra fue colocada correctamente


# Función para verificar si una matriz está vacía
def matriz_esta_vacia(matriz):
    """Verifica si una matriz está vacía.

    Args:
        matriz (list): La matriz a verificar.

    Returns:
        bool: True si la matriz está vacía, False en caso contrario.
    """
    for fila in matriz:
        if any(letra != "" for letra in fila):
            return False
    return True

# Nueva función para agregar palabra a cualquiera de las matrices
def agregar_palabra():
    """Agrega una palabra a la matriz seleccionada, verificando intersecciones y validaciones necesarias.

    Args:
        None

    Returns:
        None
    """
    palabra = entrada_palabra.get().upper()
    definicion = entrada_definicion.get()
    orientacion = entrada_orientacion.get().upper()

    try:
        version = int(entrada_version.get())
    except ValueError:
        messagebox.showerror("Error", "La versión debe ser números.")
        return
    
    if not palabra or not definicion or not orientacion or not version:
        messagebox.showerror("Error", "Debe rellenar todos los espacios (palabra, definición y orientación).")
        return

    if orientacion not in ["V", "H"]:
        messagebox.showerror("Error", "La orientación debe ser 'V' o 'H'.")
        return
    
    palabra_procesada = quitar_tildes(palabra)
    if palabra_procesada in palabras_agregadas:
        messagebox.showerror("Error", "La palabra ya ha sido agregada.")
        return
    if definicion in definiciones_agregadas:
        messagebox.showerror("Error", "La definición ya ha sido agregada.")
        return

    posiciones_letras = []

     # Verificar si ambas matrices están vacías
    if matriz_esta_vacia(matriz) and matriz_esta_vacia(matriz_2):
        fila = random.randint(0, len(matriz) - 1)
        columna = random.randint(0, len(matriz[0]) - 1)
        if orientacion == "H" and columna + len(palabra) > len(matriz[0]):
            columna = len(matriz[0]) - len(palabra)
        elif orientacion == "V" and fila + len(palabra) > len(matriz):
            fila = len(matriz) - len(palabra)

       # Colocar la palabra en la matriz 1
        if puede_colocar_palabra(palabra, fila, columna, orientacion, matriz):
            for idx, letra in enumerate(palabra_procesada):
                if orientacion == "H":
                    matriz[fila][columna + idx] = letra
                    matriz_btn[fila][columna + idx]["text"] = letra
                    posiciones_letras.append((fila, columna + idx, 0))  # Coordenadas (X=fila, Y=columna+idx, Z=0)
                elif orientacion == "V":
                    matriz[fila + idx][columna] = letra
                    matriz_btn[fila + idx][columna]["text"] = letra
                    posiciones_letras.append((fila + idx, columna, 0))  # Coordenadas (X=fila+idx, Y=columna, Z=0)

            palabras_agregadas.add(palabra_procesada)
            # Imprimir la posición en la que se colocó la palabra
            pos_x = columna
            pos_y = fila
            pos_z = 0
            lista(matriz, matriz_2, palabra_procesada, definicion, fila, columna, orientacion)
            total_palabras.append(palabra_procesada)
            definiciones_agregadas.add(definicion)
            definiciones.append(f"{len(definiciones) + 1}) {definicion}")
            lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")
            sincronizar_matrices()
        else:
            messagebox.showerror("Error", "No se puede colocar la palabra en esa posición.")
    else:
        # Verificar si la palabra se puede agregar con intersección en ambas matrices
        posiciones_posibles_matriz1 = encontrar_interseccion(palabra, matriz, orientacion)
        posiciones_posibles_matriz2 = encontrar_interseccion(palabra, matriz_2, orientacion)

        # Combinar posiciones posibles
        posiciones_posibles = posiciones_posibles_matriz1 + posiciones_posibles_matriz2

        if posiciones_posibles:
            fila, columna, _ = random.choice(posiciones_posibles)
            matriz_objetivo = matriz if any(pos[0] == fila and pos[1] == columna for pos in posiciones_posibles_matriz1) else matriz_2
            matriz_btn_objetivo = matriz_btn if matriz_objetivo is matriz else matriz_2_btn
            z_valor = 0 if matriz_objetivo is matriz else 1  # Z=0 para X-Y, Z=1 para Y-Z
            
            palabra_con_tilde = entrada_palabra.get()  # Obtiene la palabra desde el Entry
            palabra_procesada = quitar_tildes(palabra_con_tilde)
            

            for idx, letra in enumerate(palabra_procesada):
                if orientacion == "H":
                    matriz_objetivo[fila][columna + idx] = letra
                    matriz_btn_objetivo[fila][columna + idx]["text"] = letra
                    posiciones_letras.append((fila, columna + idx, z_valor))  # Coordenadas (X=fila, Y=columna+idx, Z=z_valor)
                elif orientacion == "V":
                    matriz_objetivo[fila + idx][columna] = letra
                    matriz_btn_objetivo[fila + idx][columna]["text"] = letra
                    posiciones_letras.append((fila + idx, columna, z_valor))  # Coordenadas (X=fila+idx, Y=columna, Z=z_valor)

            pos_x = 0
            pos_y = fila
            pos_z = columna
            total_palabras.append(palabra_procesada)
            lista(matriz, matriz_2, palabra_procesada, definicion, fila, columna, orientacion)
            posiciones_letras.append(pos_x and pos_y and pos_z)
            palabras_agregadas.add(palabra_procesada)
            definiciones_agregadas.add(definicion)
            definiciones.append(f"{len(definiciones) + 1}) {definicion}")
            lista_definiciones.insert(tk.END, f"{len(definiciones)}. {definicion}")
            sincronizar_matrices()
        else:
            messagebox.showinfo("Sin intersección", "No hay intersección válida para colocar la palabra.")
    
 # Aquí se devuelve o se almacena la lista con las posiciones de las letras en la variable deseada
    return   # O almacénala en otra variable si lo prefieres

# Función para sincronizar ambas matrices
def sincronizar_matrices():
    """Sincroniza las letras entre dos matrices: 
    la última columna de la matriz X-Y y la primera columna de la matriz Z-Y.

    Args:
        matriz: La matriz X-Y que contiene las letras.
        matriz_2: La matriz Z-Y que contiene las letras.
        matriz_btn: Botones asociados a la matriz X-Y.
        matriz_2_btn: Botones asociados a la matriz Z-Y.

    Returns:
        None
    """
    # Sincronizar de la última columna de X-Y a la primera columna de Z-Y
    for fila in range(len(matriz)):
        letra_xy = matriz[fila][-1]  # Última columna de X-Y
        letra_zy = matriz_2[fila][0]  # Primera columna de Z-Y
        
        # Copiar de X-Y a Z-Y si la letra existe y no hay conflicto
        if letra_xy != "" and (letra_zy == "" or letra_zy == letra_xy):
            matriz_2[fila][0] = letra_xy
            matriz_2_btn[fila][0]["text"] = letra_xy  # Actualizar el botón en Z-Y
        
        # Copiar de Z-Y a X-Y si la letra existe y no hay conflicto
        if letra_zy != "" and (letra_xy == "" or letra_xy == letra_zy):
            matriz[fila][-1] = letra_zy
            matriz_btn[fila][-1]["text"] = letra_zy  # Actualizar el botón en X-Y
            
def terminar_crucigrama(diccionario_1, palabras_lista):
    """Finaliza la creación del crucigrama, obtiene las dimensiones y 
    guarda la información en un diccionario. 

    Args:
        diccionario_1 (dict): Un diccionario que almacenará la información del crucigrama.
        palabras_lista (list): Una lista de palabras que se han agregado al crucigrama.

    Returns:
        None
    """
    numero_palabras = len(total_palabras)
    # Obtener dimensiones de la matriz
    tamaño_x = len(matriz)
    tamaño_y = len(matriz[0]) if matriz else 0
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
    messagebox.showinfo("Total de Palabras", f"Total de palabras agregadas: {total_palabras}")
    guardar_crucigrama(diccionario_general)

from crear_crucigrama import nombre
num=nombre[0]
def guardar_crucigrama(diccionario_general):
    """Guarda el crucigrama en un archivo binario con extensión .c3d.

    Args:
        diccionario_general (dict): Un diccionario que contiene la información del crucigrama,
    incluidas palabras, definiciones y posiciones.

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

        # Cerrar el archivo
        mi_archivo.close()

def alternar_vista():
    """Alterna la vista entre dos marcos de matriz en la interfaz gráfica.
    Si el marco de la matriz actual es visible, lo oculta y muestra el otro marco.
    De lo contrario, oculta el segundo marco y muestra el marco actual.

    Args:
        None

    Returns:
        None
    """
    if frame_matriz.winfo_viewable():
        frame_matriz.grid_remove()
        frame_matriz_2.grid(row=0, column=0)
    else:
        frame_matriz_2.grid_remove()
        frame_matriz.grid(row=0, column=0)

# Crear la ventana principal
root = tk.Tk()
root.title("Creador y Jugador de Crucigrama 3D")
root.geometry("800x700")

# FONDO
image = Image.open("c.png")
image = image.resize((800, 800), Image.Resampling.LANCZOS)  # Cambiar a 800x800
bg_image = ImageTk.PhotoImage(image)

# Crear el Label para el fondo
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Frame para la primera matriz (X-Y)
frame_matriz = tk.Frame(root)
frame_matriz.grid(row=0, column=0, padx=10, pady=10)

# Frame para la segunda matriz (Y-Z)
frame_matriz_2 = tk.Frame(root)

# Panel de control
frame_controles = tk.Frame(root)
frame_controles.grid(row=0, column=1, padx=10, pady=10)

# Entrada para definir el tamaño de la matriz
tk.Label(root, text="Tamaño de la cuadrícula:").grid(row=2, column=2, sticky="w")
entrada_size = tk.Entry(root)
entrada_size.grid(row=2, column=7, columnspan=3)

# Botón para crear la matriz
btn_crear = tk.Button(root, text="Crear Crucigrama", command=crear_crucigrama, bg="green", fg="black")
btn_crear.grid(row=2, column=14, columnspan=3)

# Botón para alternar la vista (girar)
btn_girar = tk.Button(root, text="Girar", command=alternar_vista, bg="green", fg="black")
btn_girar.grid(row=5, column=10,  columnspan=3)

# Entrada para agregar palabra y definición
tk.Label(root, text="Palabra:").grid(row=4, column=2, sticky="w")
entrada_palabra = tk.Entry(root, state="disabled")
entrada_palabra.grid(row=4, column=7)

tk.Label(root, text="Definición:").grid(row=5, column=2, sticky="w")
entrada_definicion = tk.Entry(root, state="disabled")
entrada_definicion.grid(row=5, column=7)

# Entrada para definir la orientación
tk.Label(root, text="Orientación (V/H):").grid(row=6, column=2, sticky="w")
entrada_orientacion = tk.Entry(root, state="disabled")
entrada_orientacion.grid(row=6, column=7)

tk.Label(frame_controles, text="Versión:").grid(row=7, column=2, sticky="w")
entrada_version = tk.Entry(frame_controles)
entrada_version.grid(row=7, column=7)

# Función para agregar palabra con verificación de orientación
def agregar_palabra_con_orientacion(matriz_objetivo, matriz_btn_objetivo):
    palabra = entrada_palabra.get().upper()
    definicion = entrada_definicion.get()
    orientacion = entrada_orientacion.get().upper()

    if not palabra or not definicion or not orientacion:
        messagebox.showerror("Error", "Debe rellenar todos los espacios (palabra, definición y orientación).")
        return

    if orientacion not in ["V", "H"]:
        messagebox.showerror("Error", "La orientación debe ser 'V' o 'H'.")
        return

    # Colocar la palabra en la matriz
    colocar_palabra_interseccion(palabra, definicion, orientacion, matriz_objetivo, matriz_btn_objetivo)


# Botón para agregar palabra
btn_agregar_palabra = tk.Button(root, text="Agregar palabra", state="disabled", command=agregar_palabra, bg="green", fg="black")
btn_agregar_palabra.grid(row=8, column=10, columnspan=3)

# Lista de definiciones
lista_definiciones = tk.Listbox(root, height=10, width=40)
lista_definiciones.grid(row=10, column=2, columnspan=3)

# Botón para terminar
btn_terminar = tk.Button(root, text="Terminar", command=lambda:terminar_crucigrama(diccionario_1, palabras_lista), state="disabled", bg="green", fg="black")
btn_terminar.grid(row=12, column=10, columnspan=3)


# Iniciar el loop de la aplicación
root.mainloop()