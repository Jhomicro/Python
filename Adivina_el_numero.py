#Ejercicio 5: adivina un número
import random

aleatorio = random.randint(1,10)
num = 0

while num != aleatorio:
    num=int(input("ingresa un número: "))
    if aleatorio != num:
        print("Sigue intentando")
print(f"El número es {aleatorio}")
