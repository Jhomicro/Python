#Calculadora de indice de masa corporal

def IMC(peso, altura):
    imc = peso / (altura**2)
    return imc

#? Solicitar las unidades
peso= float(input("Ingresa tu peso en kilogramos: "))
altura=float(input("Ingresa tu altura en metros: "))

#? Calcular tu IMC
imc= IMC(peso, altura)
imc= round(imc, 3)

#?Imprimir el calculo
print("Tu IMC es: ", imc)