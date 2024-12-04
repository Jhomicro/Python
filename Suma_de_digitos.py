#Suma de digitos
def suma_d(num):
    suma=0
    for digito in str(num):
        suma+=int(digito)
    return sum
try:
    numero_ingresdado= int(input("Ingresa un digito para calcular la suma de digitos"))
    resultado=suma_d(numero_ingresdado)
    print(f"La suma de los digitos es {numero_ingresdado}")
except ValueError:
    print("Por favor agrega un número entero valido")