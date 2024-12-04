#Vacaciones

print("***************************\n" + "Bienvenido al menú de rappi\n" + "***************************\n")

nombre=input("Ingresa tu nombre: ")
id=(int(input("Ingresa tu número de identificación: ")))
print("Escoja la opción del departo que representes\n")
print("\t1. Atención al cliente\n\t2. Logistica\n\t3. Gerencia\n")
opc = int(input())

if opc == 1:
    print("Departamento de atención al cliente\n")
    clave=int(input("Ingrese la clave según su tiempo de antiguedad\n\t1. Con un año de servicio\n\t2. Con 2 a 6 años de servicio\n\t3. A partir de 7 años\n"))
    
    if clave == 1:
        print(nombre + " tienes 6 días de vacaciones")
    elif clave == 2:
        print(nombre + " tienes 14 días de vacaciones")
    elif clave == 3:
        print(nombre + " tienes 20 días de vacaciones")
    else:
        print(nombre + " no tienes derecho a vacaciones, siga trabajando bajo")
elif opc ==2:
    print("Departamento de logistica")
    clave=int(input("Ingrese la clave según su tiempo de antiguedad\n\t1. Con un año de servicio\n\t2. Con 2 a 6 años de servicio\n\t3. A partir de 7 años\n"))
    
    if clave == 1:
        print(nombre + " tienes 7 días de vacaciones")
    elif clave == 2:
        print(nombre + " tienes 15 días de vacaciones")
    elif clave == 3:
        print(nombre + " tienes 22 días de vacaciones")
    else:
        print(nombre + " no tienes derecho a vacaciones, siga trabajando bajo")
        
elif opc == 3:
    print("Departamento de gerencia")
    clave=int(input("Ingrese la clave según su tiempo de antiguedad\n\t1. Con un año de servicio\n\t2. Con 2 a 6 años de servicio\n\t3. A partir de 7 años\n"))
    
    if clave == 1:
        print(nombre + " tienes 10 días de vacaciones")
    elif clave == 2:
        print(nombre + " tienes 20 días de vacaciones")
    elif clave == 3:
        print(nombre + " tienes 30 días de vacaciones")
    else:
        print(nombre + " no tienes derecho a vacaciones, siga trabajando bajo")
else:
    print(nombre + " no se reconoce la opción seleccionada, por favor verifique nuevamente las opciones")