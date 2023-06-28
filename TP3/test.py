import pandas as pd
import matplotlib.pyplot as plt

def golesToString(stringOfGoals):
    '''
    Recibe un stings que contiene información de los goles de un partido 

    Entrada: 
        - recibe un string de goles [string]
    Salida: 
        - devuelve: penalLocal [string], golLocal [string], golVisitante [string], penalVisitante [string]

    '''

    goals = []
    aux = ''

    print(stringOfGoals)
    for index,number in enumerate(stringOfGoals):

        if not number.isdigit(): continue #si no es un numero, salteamos todo y pasamos al siguiente caracter
        aux += number
        if index + 1 == len(stringOfGoals) or not stringOfGoals[index+1].isdigit(): #si el caracter siguiente al num, no es un numero, debemos agregar aux a en goals[]
            goals.append(int(aux))
            aux = ''
    
    if '(' in stringOfGoals: #Si el string tiene un paréntesis, quiere decir que hubo penales
        pass

    else: #Si no hay un ( en el string, quiere decir que no hubo penales, por lo que hay que agregar dos ceros a la lista de goles
        #sumamos dos ceros al principio y al final para conseguir formato de [0,1,2,0]
        goals.append(0) 
        goals.insert(0,0)
    print(goals)

    return goals[0],goals[1],goals[2],goals[3]

def crearDiccionario(df):
    '''
    recibe un Dataframe de pandas y crea un diccionario. Devuelve el diccionario creado con los nombres de los countryes como claves

    Entrada: 
        - Recibe el dataframe del archivo con todos los goles del partido [DataFrame]
    Salida: 
        - Devuelve el diccionario principal creado [dicc]

    '''

    dic = {}
    for countryName in df['home_team']: #Recorremos la columna home_team y obtenemos el index con enumerate

        #si el diccionario no esta creado, lo creamos
        if countryName not in dic:
            dic[countryName] = {'goals':0, 'points':[0], 'rank':0}

        #sumamos todos los goles que hizo el país estando de local
    return dic

def sumarGoles(dic,df):

    '''
    recibe el diccionario creado en crearDiccionario() y el dataframe usado en la funcion crearDiccionario() para crear el diccionario.
    Agrega la cantidad de goles que convirtió el equipo durante el partido, teniendo en cuenta los goles de penal
    No retorna nada

    Entrada: 
        - Recibe el diccionario principal creado [dicc] y el dataframe del archivo con todos los goles del partido [DataFrame]
    Salida: 
        - None

    '''

    for index,data in df[['home_team','away_team', 'score']].iterrows(): #iteramos por cada fila del dataFrame 

        local = data[0]
        visitante = data[1]

        penalLocal,golLocal,golVisitante,penalVisitante = golesToString(data[2]) #obtenemos los goles del partido

        #asignamos la cantidad de goles a cada equipo
        dic[local]['goals'] = dic[local]['goals'] + penalLocal + golLocal 
        dic[visitante]['goals'] = dic[visitante]['goals'] + golVisitante + penalVisitante    

def addRank(dic,df):
    '''
    recibe el diccionario creado en crearDiccionario() y el dataframe usado en la funcion crearDiccionario() para crear el diccionario.
    Agrega el puesto en el que termino el equipo en base a los ultimos dos partidos jugados en el mundial
    No devuelve nada

    Entrada: 
        - Recibe el diccionario principal creado [dicc] y el dataframe del archivo con todos los goles del partido [DataFrame]
    Salida: 
        - None

    '''

    puesto = 1
    for i in [-1,-2]:
        
        penalLocal,golLocal,golVisitante,penalVisitante = golesToString(df[['score']].iloc[i].to_string(header= False, index= False)) #Pedimos los goles de los ultimos dos partidos
        golesTotales = (golLocal + penalLocal) - (golVisitante + penalVisitante) #Sumamos la cantidad de goles totales realizados en el partido

        local = df[['home_team']].iloc[i,:].to_string(header= False, index= False) #obtenemos el country local
        visita = df[['away_team']].iloc[i,:].to_string(header= False, index= False) #obtenemos el country visitante

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

def faseDeGrupos(dic,df):
    '''
    recibe el diccionario creado en crearDiccionario() y el dataframe usado en la funcion crearDiccionario() para crear el diccionario.
    Agrega a cada diccionario una lista con los puntos ganados a lo largo de la fase de grupos
    No retorna nada

    Entrada: 
        - Recibe el diccionario principal creado [dicc] y el dataframe del archivo con todos los goles del partido [DataFrame]
    Salida: 
        - None

    '''

    for index,data in df[['home_team','away_team']].iterrows(): #recorremos cada fila del dataframe

        penalLocal,golLocal,golVisitante,penalVisitante = golesToString(df['score'].values[index]) #obtenemos los goles de la ilera de datos
        golesTotales = (golLocal + penalLocal) - (golVisitante + penalVisitante) #obtenemos los goles totales del partido
    
        countryLocal = data[0]
        countryVisita = data[1]

        #dependiendo de quien gane, le appendeamos 3, 1 o 0 puntos
        if len(dic[countryLocal]['points'])<4:
            if golesTotales>0: #gana local
                dic[countryLocal]['points'].append(dic[countryLocal]['points'][-1]+3)
            if golesTotales ==0: #empatan
                dic[countryLocal]['points'].append(dic[countryLocal]['points'][-1]+1)
            if golesTotales<0: #pierden
                dic[countryLocal]['points'].append(dic[countryLocal]['points'][-1])

        if len(dic[countryVisita]['points'])<4:
            if golesTotales<0: #gana visita
                dic[countryVisita]['points'].append(dic[countryVisita]['points'][-1]+3)
            if golesTotales ==0: #empatan
                dic[countryVisita]['points'].append(dic[countryVisita]['points'][-1]+1)
            if golesTotales>0: #pierden
                dic[countryVisita]['points'].append(dic[countryVisita]['points'][-1])

def addGroupToDicc(dic,df):
    '''
    Agrega a cada diccionario de fileToDicc, el grupo al que pertenece al country. Recibe 
    como parametro el nombre de un archivo que contenga la información de los grupos y
    el diccionario de fileToDicc.
    No retorna nada, solo agrega un campo a cada diccionario de country 

    Entrada: 
        - Recibe el diccionario principal creado [dicc] y el dataframe del archivo con todos los goles del partido [DataFrame]
    Salida: 
        - None
    
    '''
    #iteramos sobre cada fila del dataframe, limitando a team y group
    for index,data in df[['team','group']].iterrows():
        #asignamos el valor de cada grupo al country correspondiente. data[0] = nombre de country; data[1] = num de grupo
        dic[data[0]]['group'] = data[1]

def fileToDicc(dataRoute, groupsRoute):
    '''
    Recibe la ruta del archivo con todos los datos del partido y la ruta del archivo con los datos de la fase de grupo
    Crea el diccionario principal, agrega todos los campos necesarios
    Devuelve el diccionario final creado
    
    teams={'España':{'goals': 10, 'points':[0, 3, 4, 5], 'rank':0, 'group':a}, 
            'Alemania':{'goals': 12, 'points':[0, 1, 4, 4], 'rank':0, 'group':b}, 
            'Inglaterra':{'goals': 8, 'points':[0, 0, 0, 3], 'rank':0, 'group':c}}

    Entrada: 
        - Recibe el la ruta del archivo con todos los goles del partido [string] y la ruta del archivo con los datos de la fase de grupo [string]
    Salida: 
        - Devuelve el diccionario principal creado [dicc]

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

def ranking(dic,key,order = False):
    '''
    Toma el diccionario como parametro y un valor de ese diccionario. Se puede incorporar un tercer parámetro opcional:
    True: ordena en orden decreciente
    False: ordena en orden creciente

    Se devuelven dos listas. La primera posee todas las llaves del diccionario, 
    la segunda el valor que guarda cada sub-diccionario para la llave
    especificada. Ejemplo:

    A = ['Inglaterra', 'España', 'Alemania'] 
    B = [8, 10, 12] 

    Entrada: 
        - Recibe el diccionario principal [dic], valor segun el cual ordenar [string] y si se desea ordenar decreciente o creciente [booleano]
    Salida: 
        - None

    '''
    listsSorted = [] #creamos una lista que tendra el formato [(country,dato),(country,dato)]
    
    for country in dic: #recorremos el diccionario para obtener los countryes
        
        #appendeamos el nombre del country y el dato que pasamos como parametro a la funcion tomandolo del dicc.
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
    No devuelve nada, solo grafica y muestra

    Entrada: 
        - Recibe el diccionario principal [dic] 
    Salida: 
        - None
    '''
    ejeX, ejeY = ranking(dic,'goals')

    plt.figure(figsize =(14, 4))
    plt.bar(ejeX,ejeY)
    
    plt.yticks(range(0, ejeY[-1]+2,2)) #definimos el rango del eje y 
    plt.xticks(rotation = 90)
    plt.xlabel("Países")
    plt.ylabel("Goles totales")
    plt.title("Goles por país")

    plt.show()

def graficarGrupo(dic, grupo):
    
    '''
    Recibe el diccionario principal y el numero de grupo a graficar
    No devuelve nada, solo muestra el grafico

    Entrada: 
        - Recibe el diccionario principal [dic] y el numero de grupo a graficar [int]
    Salida: 
        - None
    '''

    countryes = []
    puntoscountryes = []

    for country in dic:
        if dic[country]['group'] == grupo:
            countryes.append(country)
            puntoscountryes.append(dic[country]['points'])

    plt.figure() #creamos la figura

    for country,puntaje in zip(countryes,puntoscountryes):   #juntamos los datos de countryes y puntos de country en fase de grupos 

        plt.plot(range(0,len(puntoscountryes[0])), puntaje , label = country, marker = 'o')
        plt.title(f' Grupo {grupo}') 
        plt.legend(loc = 'upper left') 

    plt.show()

def graficadorFaseGrupos(dic):
    '''
    Llama a la funcion de graficar la misma cantidad de grupos que existen, 8 para el mundial Qatar 2022
    Entrada: 
        - Recibe el diccionario principal [dic] 
    Salida: 
        - None
    '''
    cantGrupos = 0

    for key in dic:
        if dic[key]['group']>=cantGrupos: cantGrupos+=1 #Contamos la cantidad de grupos que hay

    for numGroup in range(1,cantGrupos):
        graficarGrupo(dic, numGroup) #llamamos a la funcion graficadora la cantidad de veces necesarias 

def save_dic(dic, fileName):
    ''' 
    Recibe el diccionario principal y el nombre del archivo que queremos asignarle al nuevo CSV
    Guarda la información almacenada en el diccionario principal.
    No retorna nada, solo guarda la informacion en el archivo CSV

    Entrada: 
        - Recibe el diccionario principal [dic] y el nombre del archivo que queremos asignarle al nuevo CSV [string]
    Salida: 
        - None

    '''
    
    with open(fileName, 'w') as archivo:
        
        columnas = 'team,goals,group,score1,score2,score3,rank\n'
        # escribimos la columna
        archivo.write(columnas)
        
        for country in dic:
            # definimos los valores a escribir en el archivo
            team = country
            goals = dic[country]['goals']
            group = dic[country]['group']
            score1 = dic[country]['points'][1]
            score2 = dic[country]['points'][2]
            score3 = dic[country]['points'][3]
            rank = score1 = dic[country]['rank']
            # escribimos los valores        
            linea = f'{team},{goals},{group},{score1},{score2},{score3},{rank}\n'
            archivo.write(linea)

