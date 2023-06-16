import pandas as pd
import matplotlib.pyplot as plt

def golesToString(stringOfGoals):
    '''
    Recibe un stings que contiene información de los goles de un partido y 
    devuelve una tupla con los valores correspondientes
 
    '''
    goals = []

    for number in stringOfGoals:
        if number.isdigit(): 
            goals.append(int(number)) #apendeamos los numeros a la lista de goles
    
    if '(' in stringOfGoals: #Si el string tiene un paréntesis, quiere decir que hubo penales
        pass

    else: #Si el strign tiene longitud menor a 4, quiere decir que no hubo penales, por lo que hay que agregar dos ceros a la lista de goles
        #sumamos dos ceros al principio y al final para conseguir formato de [0,1,2,0]
        goals.append(0) 
        goals.insert(0,0)

    return goals[0],goals[1],goals[2],goals[3]

def crearDiccionario(df):
    dic = {}
    for countryName in df['home_team']: #Recorremos la columna home_team y obtenemos el index con enumerate

        #si el diccionario no esta creado, lo creamos
        if countryName not in dic:
            dic[countryName] = {'goals':0, 'points':[0], 'rank':0}

        #sumamos todos los goles que hizo el país estando de local
    return dic

def sumarGoles(dic,df): # home_team away_team

    for index,data in df[['home_team','away_team', 'score']].iterrows():

        local = data[0]
        visitante = data[1]

        penalLocal,golLocal,golVisitante,penalVisitante = golesToString(data[2])

        dic[local]['goals'] = dic[local]['goals'] + penalLocal + golLocal
        dic[visitante]['goals'] = dic[visitante]['goals'] + golVisitante + penalVisitante    

def addRank(dic,df):
    puesto = 1
    for i in [-1,-2]:
        
        penalLocal,golLocal,golVisitante,penalVisitante = golesToString(df[['score']].iloc[i].to_string(header= False, index= False))
        golesTotales = (golLocal + penalLocal) - (golVisitante + penalVisitante)

        local = df[['home_team']].iloc[i,:].to_string(header= False, index= False)
        visita = df[['away_team']].iloc[i,:].to_string(header= False, index= False)

        if golesTotales>0: #quiere decir que gana el equipo local
            dic[local]['rank'] = puesto #le asignamos el primer puesto
            puesto += 1
            dic[visita]['rank'] = puesto #le asignamos el segundo puesto
            puesto += 1 #le sumamos una vez mas el valor para que el siguiente equipo que salga tercero tenga su ranking correspondeinte

        else:
            dic[visita]['rank'] = puesto #le asignamos el primer puesto
            puesto += 1
            dic[local]['rank'] = puesto #le asignamos el segundo puesto
            puesto += 1 #le sumamos una vez mas el valor para que el siguiente equipo que salga tercero tenga su ranking correspondeinte

    return dic

def faseDeGrupos(dic,df):
    for index,data in df[['home_team','away_team']].iterrows():

        penalLocal,golLocal,golVisitante,penalVisitante = golesToString(df['score'].values[index]) #obtenemos los goles de la ilera de datos
        golesTotales = (golLocal + penalLocal) - (golVisitante + penalVisitante) #obtenemos los goles totales del partido
    
        paisLocal = data[0]
        paisVisita = data[1]

        #dependiendo de quien gane, le appendeamos 3, 1 o 0 puntos
        if len(dic[paisLocal]['points'])<4:
            if golesTotales>0: #gana local
                dic[paisLocal]['points'].append(dic[paisLocal]['points'][-1]+3)
            if golesTotales ==0: #empatan
                dic[paisLocal]['points'].append(dic[paisLocal]['points'][-1]+1)
            if golesTotales<0: #pierden
                dic[paisLocal]['points'].append(dic[paisLocal]['points'][-1])

        if len(dic[paisVisita]['points'])<4:
            if golesTotales<0: #gana visita
                dic[paisVisita]['points'].append(dic[paisVisita]['points'][-1]+3)
            if golesTotales ==0: #empatan
                dic[paisVisita]['points'].append(dic[paisVisita]['points'][-1]+1)
            if golesTotales>0: #pierden
                dic[paisVisita]['points'].append(dic[paisVisita]['points'][-1])

def addGroupToDicc(dic,df):
    '''
    Agrega a cada diccionario de fileToDicc, el grupo al que pertenece al pais. Recibe 
    como parametro el nombre de un archivo que contenga la información de los grupos y
    el diccionario de fileToDicc.
    
    '''
    #iteramos sobre cada fila del dataframe, limitando a team y group
    for index,data in df[['team','group']].iterrows():
        #asignamos el valor de cada grupo al pais correspondiente. data[0] = nombre de pais; data[1] = num de grupo
        dic[data[0]]['group'] = data[1]

def fileToDicc(dataRoute, groupsRoute):
    '''
    Recibe el nombre de un archivo y devuelve un diccionario con paises como clave y otros
    diccionarios como valor.

    teams = {'equipox': { 'goals': x, 'points': [p0, p1, p2, p3], 'rank':x }, 
            'equipoy': { 'goals': y, 'points': [p0, p1, p2, p3], 'rank':0 }}
    '''
    dic = {}
    fileDF = pd.read_csv(dataRoute, encoding='utf8') 
    groupsDF = pd.read_csv(groupsRoute, encoding='utf8')

    dic = crearDiccionario(fileDF)
    addRank(dic,fileDF)
    sumarGoles(dic,fileDF)
    faseDeGrupos(dic,fileDF)
    addGroupToDicc(dic,groupsDF)

    return dic

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
    country, data = zip(*sortedlist)
    
    return list(country), list(data)

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


diccionarioPaises = fileToDicc('IPC\TPs-IPC\TP3\data.csv','IPC\TPs-IPC\TP3\group_stats.csv')
