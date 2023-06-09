import pandas as pd
import matplotlib.pyplot as plt

def golesToString(stringOfGoals,homeOrAway):
    '''
    Recibe un stings que contiene información de los goles de un partido y 
    devuelve una tupla con los valores correspondientes
 
    '''
    goals = []

    for number in stringOfGoals:
        if number.isdigit(): 
            goals.append(int(number)) #apendeamos los numeros a la lista de goles
    
    if len(stringOfGoals)>=4: #Si el string tiene longitud de 4 o mas, quiere decir que hubo penales
        pass

    else: #Si el strign tiene longitud menor a 4, quiere decir que no hubo penales, por lo que hay que agregar dos ceros a la lista de goles
        #sumamos dos ceros al principio y al final para conseguir formato de [0,1,2,0]
        goals.append(0) 
        goals.insert(0,0)

    if homeOrAway == 'home': return goals[0]+goals[1] 
    if homeOrAway == 'away': return goals[2]+goals[3]

def fileToDicc(fileRoute):
    '''
    Recibe el nombre de un archivo y devuelve un diccionario con paises como clave y otros
    diccionarios como valor.

    teams = {'equipox': { 'goals': x, 'points': [p0, p1, p2, p3], 'rank':x }, 
            'equipoy': { 'goals': y, 'points': [p0, p1, p2, p3], 'rank':0 }}
    '''
    dic = {}
    fileDF = pd.read_csv(fileRoute, encoding='utf8') #Definimos el DataFrame
    
    for index,countryName in enumerate(fileDF['home_team']): #Recorremos la columna home_team y obtenemos el index con enumerate
        
        #si el diccionario no esta creado, lo creamos
        if countryName not in dic:
            dic[countryName] = {'goals':0, 'points':[0], 'rank':0}

        #agregamos el ranking segun como salieron en el mundial 2022
        if countryName == 'Argentina': dic[countryName]['rank'] = 1
        if countryName == 'France': dic[countryName]['rank'] = 2
        if countryName == 'Croatia': dic[countryName]['rank'] = 3
        if countryName == 'Morocco': dic[countryName]['rank'] = 4

        #sumamos todos los goles que hizo el país estando de local
        dic[countryName]['goals'] = dic[countryName]['goals'] + golesToString(fileDF['score'].values[index],'home')

    for index,countryName in enumerate(fileDF['away_team']): #Recorremos la columna away_team y obtenemos el index con enumerate
        
        #sumamos todos los goles que hizo el país estando de visitante
        dic[countryName]['goals'] = dic[countryName]['goals'] + golesToString(fileDF['score'].values[index],'away')
        
    for countryName in dic: #obtenemos todos los nombres de paises en el dicionario    
         for index,data in fileDF[['home_team','away_team']].iterrows(): 
            # Obtenemos un indice y una tupla: 63, (home_team: Argentina, away_team: France, Name: 63, dtype: object)
            
            #Si el pais esta en la fila entramos al bloque if
            if countryName in data[0] and len(dic[countryName]['points'])<4: #si el equipo es local
                golesTotales = golesToString(fileDF['score'].values[index],'home') - golesToString(fileDF['score'].values[index],'away')

                if golesTotales>0: #Gana el local, suma 3
                    dic[countryName]['points'].append(dic[countryName]['points'][-1] + 3 )

                if golesTotales == 0: #Empatan los equipos, suman 1
                    dic[countryName]['points'].append(dic[countryName]['points'][-1] + 1 )

                elif len(dic[countryName]['points'])<4: #Gana visita, suma 0
                    dic[countryName]['points'].append(dic[countryName]['points'][-1])

            if countryName in data[1] and len(dic[countryName]['points'])<4: #si el equipo es visitante 
                
                if golesTotales<0: #Gana visita, suma 3
                    dic[countryName]['points'].append(dic[countryName]['points'][-1] + 3 )

                if golesTotales == 0: #Empatan los equipos, suman 1
                    dic[countryName]['points'].append(dic[countryName]['points'][-1] + 1 )
              
                elif len(dic[countryName]['points'])<4: #Gana local, suma 0
                    dic[countryName]['points'].append(dic[countryName]['points'][-1])
    return dic       

def addGroupToDicc(fileRoute,dic):
    '''
    Agrega a cada diccionario de fileToDicc, el grupo al que pertenece al pais. Recibe 
    como parametro el nombre de un archivo que contenga la información de los grupos y
    el diccionario de fileToDicc.
    
    '''
    #Creamos el dataframe con la ruta
    fileDF = pd.read_csv(fileRoute, encoding='utf8')

    #iteramos sobre cada fila del dataframe, limitando a team y group
    for index,data in fileDF[['team','group']].iterrows():
        #asignamos el valor de cada grupo al pais correspondiente. data[0] = nombre de pais; data[1] = num de grupo
        dic[data[0]]['group'] = data[1]

def listasOrdenadas(dic,key,order = False):
    '''
    Toma el diccionario como parametro y un valor de ese diccionario. Se puede incorporar un tercer parámetro opcional:
    True: ordena en orden decreciente
    False: ordena en orden creciente

    Se devuelven dos listas. La primera posee todas las llaves del diccionario, 
    la segunda el valor que guarda cada sub-diccionario para la llave
    especificada. Ejemplo:

    A = ['Inglaterra', 'España', 'Alemania'] 
    B = [8, 10, 12] 

    '''
    listsSorted = [] #creamos una lista que tendra el formato [(pais,dato),(pais,dato)]
    
    for country in dic: #recorremos el diccionario para obtener los paises
        
        #appendeamos el nombre del pais y el dato que pasamos como parametro a la funcion tomandolo del dicc.
        listsSorted.append((country, dic[country][key])) 
    
    #una vez que tenemos la lista de tuplas, usamos la función sorted(). Le pasamos la lista de tuplas a ordenar
    #como primer parametro, y como segundo parametro una funcion lambda, que toma como parametro x, que corresponde
    #a la tupla, y x[1] es el parametro que usamos para ordenar las tuplas dentro de la lista. 
    #esta funcion devuelve una nueva lista de tuplas. El parametro reverse define el orden creciente o decreciente
    sortedlist = sorted(listsSorted,key=lambda x: x[1],reverse = order)

    #retornamos la nueva lista creada. La funcion zip(iterable) con un * por delante, tiene el efecto contrario
    # a la funcion zip(iterable). Esto quiere decir que se retorna una tupla de dos listas que pueden ser
    #desempaquetadas
    return zip(*sortedlist)

def graficadorDeBarras (dic):
    '''
    Recibe el diciconario y grafica con barras los goles totales de cada equipo en orden ascendente.
    Su gráfico debe tener los nombres rotados a 90°, el nombre del eje x, y el nombre del eje y.
    '''

    ejex,ejey = listasOrdenadas(dic,'goals') 
    print(ejex)
    print(ejey)
    plt.hist(ejex,ejey)
    plt.show()


# faseGrupos =  pd.read_csv('TP3\group_stats.csv', encoding='utf8')
# datosPartidos = pd.read_csv('TP3/data.csv', encoding='utf8')

# faseGrupos[['group','team']]
# print(datosPartidos[['match','home_team','away_team','score']].to_string())

diccionarioPaises = fileToDicc('TP3/data.csv')
addGroupToDicc('TP3\group_stats.csv',diccionarioPaises)
graficadorDeBarras(diccionarioPaises)
