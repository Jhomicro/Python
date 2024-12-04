def regresiva(numer):
    for i in range (numer, 0,-1):
        print(i)

try:
    ingresado=int(input("Ingrese un número para hacer la cuenta regresiva: "))
    regresiva(ingresado)
except ValueError:
    print("Por favor ingrese un número entero valido")
    