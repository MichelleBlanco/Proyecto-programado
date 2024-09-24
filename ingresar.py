
def ingresar_palabra():
    lista_palabras = []  # Lista para almacenar las palabras y definiciones
    lista_usar = [] 
    letras_divididas = []
    numero = 1  

    while True:
        palabra = input(f"Escriba la palabra #{numero} (o escribe 'T' para terminar): ")
        if palabra == 'T': 
            break
        elif palabra == "":
            print("No se ha ingresado ninguna palabra.")
            
        else:
            while True:
                definicion = input(f"Escriba la definición de '{palabra}': ")
                if definicion == "": 
                    print("Debe ingresar una definición")
                else:
                    lista_palabras.append([numero, palabra, definicion])
                    lista_usar.append([palabra])
                    
                    break  # Salimos del bucle solo si hay una definición válida
                    
            numero += 1  


    for sublista in lista_usar:
        palabra = sublista[0]  # Tomar la primera (y única) palabra de la sublista
        letras = list(palabra)  # Convertir la palabra en una lista de letras
        letras_divididas.append(letras)



    if lista_palabras:
        print("\nLista de palabras y definiciones:")
        for item in lista_palabras:
            print(f"{item[0]}. Palabra: {item[1]}, Definición: {item[2]}")
            
    else:
        print("No se ingresaron palabras.")

# Ejecutar la función
ingresar_palabra()

