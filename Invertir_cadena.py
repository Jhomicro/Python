
#?Desarrollar un programa que invierta una cadena de caracteres

fraseinvertida=""

frase=input("Ingrese una frase que quiere que se invierta")

for i in frase:
    fraseinvertida = i +fraseinvertida 
print(f"La palabra es {fraseinvertida}")
    