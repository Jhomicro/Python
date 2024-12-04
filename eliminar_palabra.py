#!Se solicita eliminar una palabra que forme parte de una cadena de caracteres
#!Esta cadena de caracteres debe ser solicitada desde el teclado
#!La palabra a eliminar debe ser seleccionada desde teclado
subfrase=""

frase=input("Introduce una frase: ")
palabra=input("Introduce la palabra que se desea eliminar: ")

indice=frase.find(palabra)
subfrase= frase[0:indice] + frase[indice+len(palabra)+1: ]

print(subfrase)