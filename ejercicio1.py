
#! Contador de palabras

palabra=input("Ingrese la palabra que deseas contar: ")
palabra1= palabra.replace(" ", "")#!Quita los espacios en la función
longitud = len(palabra1)
print(f"La palabra tiene {longitud} caracteres")
