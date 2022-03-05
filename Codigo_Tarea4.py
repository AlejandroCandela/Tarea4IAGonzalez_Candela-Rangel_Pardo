#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
from math import e
import matplotlib.pyplot as plt
import time
import sys


# In[ ]:


def ex_sinConectar(grafo):
    for elemento in list(grafo.keys()):
        if grafo[elemento] == {}:
            return True
    return False
            

def instancias_camino_corto_c(nodos, consumo, convexo):
    dic_nodos = {}
    ## Establecemos alguna funcion para seguir en el tema de consumo
    if consumo == 1:
        ## Si los valores exteriores son los mas pesados
        fun = lambda x: int((((1+5**.5)/2)**x-((1-5**.5)/2)**x)/5**.5)
    elif consumo == 2:
        ## Si los valores exteriores son los mas pesados
        fun = lambda x: 1/x if x>0 else 0
    elif consumo == 3:
        ## Si existen valores positivos y negativos
        fun = lambda x: x if x%2==0 else -x
    elif consumo == 4:
        ## Si los valores son constantes
        fun = lambda x: x/x

    ##Inicializamos todos los elementos de la lista vacios sin ninguna conexion
    for i in range(nodos):
        dic_nodos[str(i)] = {}
    
    if nodos == 2:
        ## Si tenemos solo dos elementos lo mas logico seria conectarlos entre si 
        dic_nodos['0']['1'] = (1,fun(2))
        dic_nodos['1']['0'] = (1,fun(2))
    if nodos == 3:
        ## En cuanto el poligono alcanza tres vertices formaremos un ciclo en forma de triangulo 
        dic_nodos['0']['1'] = (1,fun(3))
        dic_nodos['1']['2'] = (1,fun(3))
        dic_nodos['2']['0'] = (1,fun(3))
    if nodos > 3:
        ## Si tenemos mas de tres lados entonces empezaremos a contener poligonos de vertices mas chicos en vertices mas grandes
        con_lev = 3
        tot_conectado = 0
        ## Para lograr la convexion mas facil y hacerlo mas interesante necesitaremos hacer que las capas impares se muevan
        ## en contra de las manecillas del relog y los poligonos pares a favor con esta variable
        frente_atras = False 
        ## Marcamos el primer poligono de tres lados este sera el mas pequeño
        ## La distancia y el costo estan basadas en los lados del poligono
        dic_nodos['0']['1'] = (con_lev-2,fun(con_lev))
        dic_nodos['1']['2'] = (con_lev-2,fun(con_lev))
        dic_nodos['2']['0'] = (con_lev-2,fun(con_lev))
        ## Tengo entendido que para verificar si un grafo es inconexo pueden existir dos casos:
        ## 1.- Existe un vertice con un conjunto de referencia vacio
        ## 2.- Existe algun vertice que no es apuntado por ningun otro elemento
        ## En este caso este grafo solo considerara el segundo apartado para hacer un grafo no convexo
        while ex_sinConectar(dic_nodos):
            ## Para poder hacer este grafo tomaremos una metodologia muy curiosa (al menos para mi, nunca utilize grafos antes)
            ## Vamos a segmentar el ultimo poligono conectado dentro del grafo
            pri_elemento = list(dic_nodos.keys())[tot_conectado : tot_conectado + con_lev]
            ## ¿Contamos con los suficientes vertices para hacer un poligono de n+1 lados que el ultimo poligono conectado?
            if len(dic_nodos)>=tot_conectado+2*con_lev + 1:
                ##Si, entonces la tenemos facil consideramos el sentido del ciclo
                if frente_atras:
                    ## Impar: en contra favor de las manecillas del relog/frente
                    for llave in pri_elemento:
                        dic_nodos[str(int(llave) + con_lev)][str(int(llave)+ con_lev + 1)] = (con_lev-1,fun(con_lev))
                    dic_nodos[str(tot_conectado + 2*con_lev)][str(int(pri_elemento[0]) + con_lev)] = (con_lev-1,fun(con_lev))
                else:
                    ## Par: a favor de las manecillas del relog/atras
                    for llave in pri_elemento:
                        dic_nodos[str(int(llave)+ con_lev + 1)][str(int(llave) + con_lev)] = (con_lev-1,fun(con_lev))
                    dic_nodos[str(int(pri_elemento[0]) + con_lev)][str(tot_conectado + 2*con_lev)] = (con_lev-1,fun(con_lev))
                ## Ahora para que sea convexo necesitamos conectar las dos capas, la que acabamos de considerar y la anterior
                ## tomaremos la anterior como referencia para establecer las conexiones
                for llave in pri_elemento:
                    ## ¿Es el vertice de la capa mas chica par?
                    if int(llave)%2 == 0:
                        ## Si, Entonces estableceremos que la direccion de la conexion sera de dentro hacia afuera
                        dic_nodos[llave][str(int(llave) + con_lev)] =(1,1)
                    else:
                        ## No, Entonces estableceremos que la direccion de la conexion sera de afuera hacia adentro
                        dic_nodos[str(int(llave) + con_lev)][llave] =(1,1)
            else:
                ## No, contamos con los suficientes vertices entonces nos la tenemos que ingeniar un poco y considerar las
                ## necesidades que se nos indican
                ## Esta sera la unica forma de hacer un grafo no convexo si es que se inicia la ultima capa empieza con un
                ## vertice impar o termina con un vertice par al menos ese fue el patron que fui viendo
                ## En este caso segmentaremos los vertices sobrantes
                seg_elemento = list(dic_nodos.keys())[tot_conectado + con_lev:]
                ## Tenemos que proceder de forma especial en caso de que sea solo un elemento
                if len(seg_elemento) == 1:
                    ## Esto dependera si el elemento es par o impar y si debe ser convexo o no
                    if int(pri_elemento[0])%2==0:
                        ## Si es par estableceremos un ciclo convexo conectando de la primera capa a este vertice
                        ## y conectaremos con el siguiente vertice de la primera capa
                        dic_nodos[pri_elemento[0]][seg_segmento[0]] = (con_lev-1,fun(con_lev))
                        dic_nodos[seg_elemento[0]][pri_elemento[1]] = (con_lev-1,fun(con_lev))
                    else:
                        ## Si es impar podemos hacer un grafo no convexo segun nuestros criterios
                        ## Si no tiene que ser convexo entonces solo conectaremos de la segunda capa a la primera 
                        dic_nodos[seg_elemento[0]][pri_elemento[0]] = (con_lev-1,fun(con_lev))
                        if convexo == True:
                            ## Y si tiene que ser convexo entonces hacemos lo mismo que antes
                            dic_nodos[pri_elemento[1]][pri_elemento[0]] = (con_lev-1,fun(con_lev))
                ## Jutamos todos los vertices restantes de la ultima capa considerandolos como si fuera un poligono
                if frente_atras:
                    for i in range(len(seg_elemento)-1):
                        dic_nodos[seg_elemento[i]][seg_elemento[i+1]] = (con_lev-1,fun(con_lev))
                    ## Si el elemento tiene que ser convexo obligaremos al primero y al segundo a servir de salida y 
                    ## entrada respectivamente debido aque esto ayuda a formular un ciclo
                    if convexo == True:
                        dic_nodos[pri_elemento[0]][seg_elemento[0]] = (con_lev-1,fun(con_lev))
                        dic_nodos[seg_elemento[-1]][pri_elemento[len(seg_elemento)-1]] = (con_lev-1,fun(con_lev))
                else:
                    for i in range(len(seg_elemento)-1):
                        dic_nodos[seg_elemento[i+1]][seg_elemento[i]] = (con_lev-1,fun(con_lev))
                    ## Si el elemento tiene que ser convexo obligaremos al primero y al segundo a servir de entrada y 
                    ## salida respectivamente debido aque esto ayuda a formular un ciclo
                    if convexo == True:
                        dic_nodos[seg_elemento[0]][pri_elemento[0]] = (con_lev-1,fun(con_lev))
                        dic_nodos[pri_elemento[len(seg_elemento)-1]][seg_elemento[-1]] = (con_lev-1,fun(con_lev))
                ## Ahora aqui empezaremos a hacer las conexiones a los nodos 
                if len(seg_elemento)>=2:
                    ## En caso de que sea convexo tenremos que descartar los nodos ya conectados 
                    if convexo == True:
                        seg_elemento = seg_elemento[1:-1]
                    ## Y segimos el mismo criterio que antes para conectar los elementos 
                    for llave in seg_elemento:
                        if int(llave)-con_lev%2 == 0:
                            dic_nodos[str(int(llave)-con_lev)][llave] =(1,1)
                        else:
                            dic_nodos[llave][str(int(llave)-con_lev)] =(1,1)
            ## Para apuntar bien a las posiciones necesitaremos tomar en cuenta todos los elementos entonces como en los
            ## calculos solo tomamos encuenta las dos capas superiores necesitaremos una forma de agregar al posicionamiento
            ## las otras capas
            tot_conectado = con_lev + tot_conectado
            ## El lado del poligono siempre se eleva en uno
            con_lev = con_lev + 1
            ## Y cambiamos el sentido del giro
            frente_atras = not frente_atras
    return dic_nodos


# In[ ]:


def solucion(G, nodo, final,lista,con): ## Esta sera una solucion aleatoria
    while not(final in G[nodo].keys()): ## Hasta que no nos encontramos en un nodo que tiene el fin como vecino
                                        ## no paramos
        nodo_e = random.randint(0,len(G[nodo].keys())-1) ## Escogemos un vecino aleatorio
        con = con + G[nodo][list(G[nodo].keys())[nodo_e]][1] ## sumamos el coso del arista del nodo actual al
                                                             ## vecino random
        nodo = list(G[nodo].keys())[nodo_e] ## Colocamos el vencino aleatorio como el vecino actual
        lista.append(nodo)                  ## lo guardamos en el registro
    con = con + G[nodo][final][1]           ## Al finalizar agregamos el costo de la arista del nodo actual 
                                            ## al final
    lista.append(final)                     ## concatenamos el nodo final
    return lista, con                       ## regresamos los resultados


def solucion_p(G,f,rec):    ## Switch de la solucion aleatoria generada                   
    con = 0                                  ## Debemos reiniciar el contador debido a que no sabremos la 
                                             ## longuitud del camino
    lista = rec[:random.randint(1,len(rec))] ## Hacemos una variacion de la longuitud del camino recortando
                                             ## la lista
    for i in range(len(lista)-1):            ## Calculamos de nueva cuenta la longuitud del camino actual
        con = con + G[lista[i]][lista[i+1]][1]
    return solucion(G,lista[-1],f,lista,con) ## replantemos la solucion iniciando desde el ultimo nodo en 
                                             ## la lista hasta el final
    
def recocido_sim_corto(G, v, f, tem, enf):
    recorrido_sal, costo_sal = solucion(G,v,f,[v],0) ## Realizamos una solucion inicial
    while tem>0:                                    ## Detenemos el ciclo hasta parar la temperatura
        recorrido_p, costo_p = solucion_p(G,f,recorrido_sal) ## Realizamos una solucion probicional 
        if costo_sal > costo_p:                              ## Es la solucion probicional mejor que la actual
            recorrido_sal, costo_sal = recorrido_p, costo_p  ## Si, asignamos la solucion probicionala la actual
        else: 
            if e**((costo_sal-costo_p)/tem) > random.random():  ## No, decidimos si tomar la solucion con la prbabilidad 
            ## ^-------------------------------------------------- en base a esta funcion
                recorrido_sal, costo_sal = recorrido_p, costo_p ## Si toca entonces cambiamos la solucion
        tem = tem-enf                                           ## Disminuimos la temperatira en cada iteracion
    return recorrido_sal, costo_sal

lista_rec = []
lista_cos = []
G = instancias_camino_corto_c(18,2,True)
for i in range(400):
    rec, costo = recocido_sim_corto(G,'0','17',1400,1)
    lista_cos.append(costo)
## para graficar
plt.style.use('seaborn-whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(lista_cos,bins= range(0,50))
plt.show()


# In[ ]:


registro = []
for i in range(0,1000):    
    G = instancias_camino_corto_c(18,2,True)
    lista1, con1 = solucion(G,'0','17',['0'],0)
    lista2, con2 = solucion_p(G,'17',lista1)
    if con1 > con2:
        registro.append(1)
    elif con1==con2:
        registro.append(.5)
    else:
        registro.append(0)
plt.style.use('seaborn-whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(registro)
plt.show()


# In[ ]:


lista_caminos = []
lista_costos = []
con = 0
for i in range(0,1000):
    G = instancias_camino_corto_c(18,1,True)
    x, y = solucion(G,'0','17',['0'],0)
    lista_caminos.append(x)
    lista_costos.append(y)
plt.style.use('seaborn-whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(lista_costos,bins= range(10,400))
print(min(lista_costos))
plt.show()


# In[ ]:


lista_caminos = []
lista_costos = []
for i in range(0,1000):
    G = instancias_camino_corto_c(18,1,True)
    x, y = solucion(G,'0','17',['0'],0)
    lista_caminos.append(len(x))
    lista_costos.append(y)
plt.style.use('seaborn-whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')
fig,ax = plt.subplots()
ax.set_xlabel('Longuitud de camino')
ax.set_ylabel('Costo del camino')
ax = plt.scatter(x = lista_caminos, y = lista_costos)


# In[ ]:


def tiempo_mejor(reps, func, *pargs, **kagrs):
    repslist = list(range(reps))
    best = 2 ** 32 
    for i in repslist:
        start = time.perf_counter()
        ret = func(*pargs,**kagrs)
        elapsed = time.perf_counter() - start
        if elapsed < best: 
            best = elapsed
    return elapsed, ret 

def recocido_simulado(G,it):
    return recocido_sim_corto(G, '0', '101', it, 1)

tiem_RS = []
cos_RS = []
tiem_UCS = []
cos_UCS = []
G = instancias_camino_corto_c(102,1,True)
for y in range(30):
    tiempo1,res1 = tiempo_mejor(100, ucs,G,0,101)
    tiempo2,res2 = tiempo_mejor(100, recocido_simulado,G,y*30)
    tiem_RS.append(tiempo2)
    cos_RS.append(res2[1])
    tiem_UCS.append(tiempo1)
    cos_UCS.append(res1[1])
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(tiem_RS)
plt.show()
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(tiem_UCS)
plt.show()

