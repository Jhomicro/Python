##Sección figonacci
num1, num2 = 0 , 1

while num2 <= 1597:
    print(num1 , num2, end=" ") #! En pantalla: 0 ,1 ,1...
    num1 += num2
    num2 += num1
