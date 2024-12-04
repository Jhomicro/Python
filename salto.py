#Impresion par de elementos
def salto(valores):
    respuesta=[]
    for index, valor in enumerate(valores):
        if (index % 2) == 0:
            respuesta.append(valor)
    return respuesta

print(salto(["manzana","Bananas", "Melocoton", "Guayaba", "Fresa" ]))