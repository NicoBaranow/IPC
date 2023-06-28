import random 

cash = 1000 # declaracion del monto de dinero inicial
firstOption = None #declaracion de variable para elegir el primer menu de opciones de apuestas
secondOption = None #declaracion de variable para elegir el segundo menu de opciones de apuestas

#################### Columnas disponibles en la ruleta ###################

column1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
column2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
column3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

#################### Declaracion de variables ###################

amountToBet = 0
bettedToEven = 0
bettedToOdd = 0
bettedTo1Row = 0
bettedTo2Row = 0
bettedTo3Row = 0
bettedToNumber = 0
chosenNumber = None
keepPlaying = None 
randomNumber = None
ganancias = None

#################### Option messages ###################

chooseWhatToBet = '\n1. Par o Impar\n2. Columnas\n3. Número\n\n'
chooseOddOrEven = '\n¿Desea apostar a Par o Impar?\n1. Par\n2. Impar\n'
chooseColumn = '\n¿Desea apostar a la columna del 1, columna del 2 o columna del 3?\n1. Columna 1\n2. Columna 2\n3. Columna 3\n\n'
chooseNumber = '\n¿A qué número desea apostar?\n'
keepPlayingMessage = '\nDesea seguir apostando?\n1. Si\n0. No\n'

#################### Error handling messages ###################

wrongOption = '\nError, la opción ingresada es incorrecta. Vuelva a ingresar un valor\n'
wrongBalance = '\nError, no posee fondos para apostar este monto o es una cantidad erronea. Vuelva a introducir un monto\n'
wrongDataType = '\nError, el numero a ingresar debe ser un entero. Vuelva a ingresar un valor\n'


print(f"\n\n################## Bienvenido a la Ruleta ##################### \n\nUsted tiene {cash} para usar. ¿A qué desea apostar?\n") #Mensaje de bienvenida que se ejecuta 1 sola vez

#################### Functions definition ###################

#Definimos funcion para elegir entre los estilos de apuesta. Mientras que option no sea 1,2 o 3, estaremos dentro de este bucle While, pidiendole al usuario que ingrese un numero
#Implementamos try,except, para evitar errores al ingresar números con coma, que provocarían un cierre del programa por un ValueError al admitir solo enteros
#Una vez que option toma un valor entre 1,2 o 3, salimos del bucle while y la funcion devuelve el parámetro reasignado al input del usuario que servira para elegir par o impar; columnas o numero
def chooseBetStyle(option): 
    while option not in [1,2,3]: 
        try: 
            option = int(input(chooseWhatToBet)) 
            if option not in [1,2,3]: print(wrongOption) 
        except ValueError: 
            print(wrongDataType)
    return option 

#Definimos funcion para elegir entre par o impar. Igual a la funcion chooseBetStyle. 
def chooseEvenOrOdd(option):
    while option not in [1,2]: 
        try: 
            option = int(input(chooseOddOrEven)) 
            if option not in [1,2]: print(wrongOption) 
        except ValueError: 
            print(wrongDataType) 
    return option 

#Definimos funcion para elegir entre columnas 1, 2 o 3. Igual a la funcion chooseBetStyle. 
def chooseColumns(option):
    while option not in [1,2,3]: 
        try: 
            option = int(input(chooseColumn))
            if option not in [1,2]: print(wrongOption) 
        except ValueError: 
            print(wrongDataType) 
    return option

#Definimos funcion para elegir numero a apostar. Igual a la funcion chooseBetStyle. 
def chooseNumberToBet(option): 
    while option not in range(37):
        try: 
            option = int(input(chooseNumber)) 
            if option not in range(37): print(wrongOption)
        except ValueError:
            print(wrongDataType) 
    return option 

#Definimos funcion para elegir el monto a apostar. Igual a la funcion chooseBetStyle, pero devuelve una cantidad de dinero entera, > a 0 y < al dinero dispobible
def placeBet (amount): 
    print(f'\nUsted tiene {cash} para apostar.\n¿Cuánto desea apostar?') 
    while amount < 1 or amount > cash or not isinstance(amount, int):
        try:
            amount = int(input()) 
            if amount < 1 or amount > cash or not isinstance(amount, int): print(wrongBalance) 
        except ValueError: 
            print(wrongDataType)
    return amount

def bet(alreadyBetted): # definimos funcion para modificar el dinero dispobible
    global cash # accedemos a la variable cash definida al principo del programa con la palabra reservada global, para asi poder modificarla dentro de la funcion
    global amountToBet # accedemos a la variable amountToBet definida al principo del programa con la palabra reservada global, para asi poder modificarla dentro de la funcion
    
    cash = cash - amountToBet #obtenemos el dinero dispobible restando el dinero actual con el dinero a apostar
    betted = amountToBet + alreadyBetted #definimos todo el dinero apostado
    print(f'\nHa apostado {amountToBet}. Le quedan {cash}') #informamos cuál fue el monto apostado
    amountToBet = 0 # reseteamos la cantidad a apostar, de lo contrario lo sumaríamos erroneamente cuando se repita 1 vez el código
    return betted #retornamos la cantidad total apostada

def askKeepPlaying(): #definimos funcion para preguntar al usuario si quiere seguir jugando
        option = None #creamos la variable local option para identificar la opcion del usuario
        while option not in [0,1]: #mientars que option no sea 1 o 2 estaremos dentro de este bucle while
            try: # implementamos try,except, para evitar errores al ingresar números con coma, que provocarían un cierre del programa
                option = int(input(keepPlayingMessage)) #pedimos al usuario que ingrese el valor correspondiente a si quiere seguir jugando o no
                if option not in [0,1]: print(wrongOption) # si option no es 1 o 2, imprimimos un mensaje de error
            except ValueError: #en caso de encontrarnos con un error del tipo 'ValueError' en el bloque try, enviaremos un mensaje de error al usuario
                print(wrongDataType)
        return option #una vez que el usuario ingresa una opcion correcta, se devuelve el valor de la opción


while True: 
    while True: 
        firstOption = chooseBetStyle(firstOption) #le asignamos a firstOption el valor de chooseBetStyle, que puede ser 1, 2 o 3

        if firstOption == 1: #si es 1 quiere decir que queremos apostar par o impar
            secondOption = chooseEvenOrOdd(secondOption) #le asignamos a secondOption el valor de chooseEvenOrOdd, que puede ser 1 o 2
            ####################  Apostar par  ###################
            if secondOption == 1: #si secondOption es 1, quiere decir que queremos apostar a un numero par                 
                amountToBet = placeBet(amountToBet) #asignamos amountToBet a PlaceBet(), que es la cantidad a apostar
                bettedToEven = bet(bettedToEven)  #asignamos la cantidad apostada a bettedToEven
            ###################  Apostar impar  ###################
            if secondOption == 2: #si secondOption es 2, quiere decir que queremos apostar a un numero impar              
                amountToBet = placeBet(amountToBet)#asignamos amountToBet a PlaceBet(), que es la cantidad a apostar
                bettedToOdd = bet(bettedToOdd)#asignamos la cantidad apostada bettedToOdd


###############################  Apostar columna ################################
        if firstOption == 2:  #si es 1 quiere decir que queremos apostar columna 1 2 o 3
            secondOption = chooseColumns(secondOption) #le asignamos a secondOption el valor de chooseColumns, que puede ser 1 2 o 3

############La metodologia para seleccionar opciones y cantidades apostadas es similar que con par o impar############
        
        ####################  Apostar columna 1  ###################
            if secondOption == 1: 
                amountToBet = placeBet(amountToBet)
                bettedTo1Row = bet(bettedTo1Row) 
        ####################  Apostar columna 2  ###################
            if secondOption == 2: 
                amountToBet = placeBet(amountToBet)
                bettedTo2Row = bet(bettedTo2Row) 
        ####################  Apostar columna 3  ###################
            if secondOption == 3:
                amountToBet = placeBet(amountToBet)
                bettedTo3Row = bet(bettedTo3Row)  

###############################  Apostar numero ################################

        if firstOption == 3 and chosenNumber == None: #Si la primera opcion es 3 quiere decir que queremos apostar a un numero, y si el numero no esta elegido anteriormente, entramos al if.
            chosenNumber = chooseNumberToBet(chosenNumber) #elegimos el numero al cual queremos apostar con la funcion chooseNumberToBet()
            amountToBet = placeBet(amountToBet) #asignamos amountToBet a PlaceBet(), que es la cantidad a apostar
            bettedToNumber = bet(bettedToNumber) #asignamos la cantidad apostada bettedToNumber

        elif firstOption == 3 and chosenNumber != None: # si queremos apostar a un numero pero este ya tiene un valor, no podremos volver a apostar a un numero
            print('Ya ha elegido un número')

###############################  seguir jugando ################################
        if cash > 0: #si luego de apostar seguimos teniendo dinero, preguntamos al usuario si quiere seguir jugando
            keepPlaying = askKeepPlaying() #la funcion askKeepPlaying le pregunta al usuario si quere o no seguir jugando, y guarda su decicion en la variable keepPlaying
        
        if keepPlaying == 0: break #Si keepPlaying es 0, salimos del segundo While True, haciendo que se eliga un número al azar y se calculen las ganancias
        
        if cash == 0:# Si nos quedamos sin dinero luego de apostar, salimos del segundo While True para ver si obtuvimos alguna ganancia
            print('No tiene mas plata para apostar')
            break
    #en caso de que keepPlaying = 1, se repetirá el segundo whileTrue, hasta que el dinero sea 0 o keepPlaying == 0 
    #Limpiamos varibales a reutilizar
        firstOption = None
        secondOption = None
        amountToBet = 0
        keepPlaying = None

############################### Dejar de apostar ################################

    randomNumber = random.randint(0,36) #Una vez que salimos del segundo while True, elegimos un número al azar y lo guardamos en la variable randomNumber

    print(f'\nHa salido el {randomNumber}\n') #Imprimimos qué numero salió
    
    if randomNumber%2 == 0 and randomNumber != 0: #si el resto del numero es 0, quiere decir que es par y gane si le aposté. El cero no se toma como par en la ruleta
        if bettedToEven>0: print('Como usted apostó',bettedToEven,'al par ganó', bettedToEven*2)
        bettedToEven *=2 #multiplico por la ganancia de par o impar 
        bettedToOdd = 0 #les saco el valor almacenado a las variables no utilizadas

    if randomNumber == 0: # si sale el 0, lo apostado a par o impar debe ser 0 ya que no se toma en cuenta el 0 para esta apuesta
        bettedToEven = 0
        bettedToOdd = 0

    if randomNumber%2 == 1: 
        if bettedToOdd>0: print('Como usted apostó',bettedToOdd,'al impar ganó', bettedToOdd*2)
        bettedToOdd *=2
        bettedToEven = 0
    
    if randomNumber in column1:
        if bettedTo1Row>0:print('Como usted apostó',bettedTo1Row,'a la columna 1 ganó', bettedTo1Row*3)
        bettedTo1Row *= 3
        bettedTo2Row = 0 
        bettedTo3Row = 0 

    if randomNumber in column2:
        if bettedTo2Row>0:print('Como usted apostó',bettedTo2Row,'a la columna 2 ganó',bettedTo2Row*3)
        bettedTo2Row *= 3
        bettedTo1Row = 0 
        bettedTo3Row = 0 

    if randomNumber in column3:
        if bettedTo3Row>0:print('Como usted apostó',bettedTo3Row,'a la columna 3 ganó',bettedTo3Row*3)
        bettedTo3Row *= 3
        bettedTo2Row = 0 
        bettedTo1Row = 0 
    
    if randomNumber == chosenNumber:
        if bettedToNumber>0:print('Como usted apostó',bettedToNumber,'al', chosenNumber, 'ganó',bettedToNumber*36)
        bettedToNumber *=36
    else: 
        bettedToNumber = 0
        
    ganancias = bettedToEven+bettedToOdd+bettedTo1Row+bettedTo2Row+bettedTo3Row+bettedToNumber #La ganancia es la sumatoria de las apuestas multiplicadas por sus respectivos multiplicadores
    cash = ganancias + cash #cash hace referencia al dinero disponible para seguir apostando, que es la suma del dinero anterior y las ganancias 
    
    print(f'Sus ganancias son {ganancias}')

    print(f'Sus dinero restante es: {cash}')
    
    if cash < 1: #Si el dinero <= a 0, se saca al usuario del programa mediante un break que lo saca del primer while
        print('Se ha quedado sin fondos para seguir apostando')
        break

    keepPlaying = askKeepPlaying() # se le pregunta al usuario si quiere seguir jugando y se asigna el valor de retorno de la funcion askKeepPlaying() a keepPlaying 

    if keepPlaying == 0: # si el usuario decide no jugar mas, sale del primer while y se acaba el programa
        break   

    print('######## Nueva ronda de apuestas ########') #de lo contrario, se reinicia el programa
    #reasignamos las variables necesarias a 0
    amountToBet = 0
    bettedToEven = 0
    bettedToOdd = 0
    bettedTo1Row = 0
    bettedTo2Row = 0
    bettedTo3Row = 0
    bettedToNumber = 0
    chosenNumber = None
    keepPlaying = None
    randomNumber = None
    ganancias = None
    firstOption = 0
    secondOption = 0
    
#En caso de retirarse del casino, se informa con cuanto dinero
print(f'Usted se retira del casino con {cash}')
