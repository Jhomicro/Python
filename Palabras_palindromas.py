#! Palabras palíndromas

def palindromo(texto):
    #!Convertir el texto en minusculas y quitar los espacios
    texto = texto.lower().replace(" ", "") 
    
    #!Retificar si el texto es igual al texto invertido
    return texto == texto[::-1]
palabra="reconocer"
frase="Anita lava la tina"
numero="1331"

if palindromo(palabra):
    print(f"{palabra} en un políndromas")
else:
    print(f"{palabra} no es políndromas")
if palindromo(frase):
    print(f"{frase} es políndromas")
else:
    print(f"{frase} no es políndromas")