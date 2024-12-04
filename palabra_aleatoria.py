import random

consonantes ="aeioubcdfghjklmnñpqrstvwxyz"
palabra=""

for i in range(10):
    palabra=input("Ingresa la palabra: ")
    if palabra != consonantes:
        print(f"{i}: Sigue intentando")
print("¡Horabuena!")
