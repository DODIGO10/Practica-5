import random as rnd
import Interpolacion_Lineal as qr
import genera_nuevo as dg
#rnd.seed(5)

lista_tabu = {}
tiempo_tabu = 2
rangodeServicios = dg.data()
def crea_solucion_vecina(solucion, posicion):
    #crea una solucion temporal recibiendo como parametro la solucion
    # anterior crea una solucion y el indice en donde fue alterado se guarda para
    # posterior momento tabu
    vector = solucion[:] # crea una copia de la solucion recibida como parametro

    index = rnd.randint(0, len(vector)-1) #se selecciona un indice random entre 0
    # y la longitud maxima de la solucion - 1 es menos 1 porque los indices inician en 0
    while index in lista_tabu: # se va a iterar hasta que indice no se encuentre dentro de
        # la lista tabu
        index = rnd.randint(0, len(solucion) - 1) #se selecciona el indice que
        # ya se comprobo que no existe en la lista tabu

    nuevo_valor = rnd.randint(rangodeServicios[posicion][0],rangodeServicios[posicion][1]) # crea un nuevo valor dentro de los rangos xmin y
    # xmax que sera asignado al vector en la posicion index generado anteriormente
    vector[index] = nuevo_valor
    return vector, index

def calcula_fo(solucion):
    vo = sum([i**2 for i in solucion])
    return vo

def crea_solucion(n):
    v = [rnd.randint(xmin, xmax) for i in range(n)]
    return v

def perturbacion(solucion,posicion): #modificacion brusca de la solucion
    vector = solucion[:]
    index1 = rnd.randint(0, len(solucion) - 1)
    while index1 in lista_tabu:
        index1 = rnd.randint(0, len(solucion) - 1)

    index2 = index1  ####
    while index2 == index1 and index2 in lista_tabu:
        index2 = rnd.randint(0, len(solucion) - 1)

    nuevo_valor1 = rnd.randint(rangodeServicios[posicion][0],rangodeServicios[posicion][1])
    nuevo_valor2 = rnd.randint(rangodeServicios[posicion][0],rangodeServicios[posicion][1])

    vector[index1] = nuevo_valor1
    vector[index2] = nuevo_valor2

    return vector, index1, index2


if __name__ == "__main__":
    data = dg.lectura()
    llaves = rangodeServicios.keys()
    llaves = list(llaves)
    mejores_vos = [[]for i in range(len(llaves))]
    lc = 30
    for i in range(len(data)):
        lc = 30
        while lc > 0:
            print("Inicia algoritmo:")
            solucion_temporal = data[i]  #S0
            print("solucion temporal: ", solucion_temporal)
            best_solucion = solucion_temporal[:] #copia de los valores
            best_vo = calcula_fo(best_solucion) # calcula funcion objetivo de cada valor de best
            # solucion que en primera instancia es la solucion inicial
            print("solucion vo inicial: ", best_vo)

            max_it_ils = 1000  #iterated local search = ils
            current_ils = 0

            max_it_local = 10000
            current_local  = 0

            while current_ils < max_it_ils: #busqueda local iterada

                while current_local < max_it_local: #busqueda local
                    solucion_temporal, idx1 = crea_solucion_vecina(solucion_temporal,llaves[i])#se rescribe
                    # la solucion_temporal por la nueva generada
                    vo_temporal = calcula_fo(solucion_temporal)

                    if vo_temporal < best_vo: # si los vo que se generan con la nueva solucion
                        # es menor con la best vo, los vo_temporal sera el nuevo best_vo
                        best_vo = vo_temporal
                        best_solucion = solucion_temporal[:] # la nueva best solucion
                        # sera una copia de la solucion temporal esto para que no haya referencias de
                        # memoria y cuando se modifica la solucion temporal no exista un cambio en best_solucion
                        print("nueva best solucion: ", solucion_temporal, end="    ")
                        print("vo: ", vo_temporal)
                        lista_tabu[idx1] = tiempo_tabu + 1 #agrega el indice a la lista

                    #print("it", end="   ")
                    #print("solucion: ", solucion_temporal, end="    ")
                    #print("vo: ", vo_temporal)

                    # update tabu times
                    lista_tabu_temp = lista_tabu.copy() # se crea una copia de la lista
                    # tabu para poder actualizar sus valores
                    for key in lista_tabu.keys():
                        lista_tabu_temp[key] -= 1
                        if lista_tabu_temp[key] == 0:
                            del lista_tabu_temp[key]
                    lista_tabu = lista_tabu_temp
                    ###

                    current_local+=1

                solucion_temporal, idx1, idx2 = perturbacion(solucion_temporal,llaves[i])
                vo_temporal = calcula_fo(solucion_temporal)
                if vo_temporal < best_vo:
                    best_vo = vo_temporal
                    best_solucion = solucion_temporal[:]
                    print("nueva best solucion: ", solucion_temporal, end="    ")
                    print("vo: ", vo_temporal)
                    lista_tabu[idx1] = tiempo_tabu + 1 # agrega el indice a la lista
                    lista_tabu[idx2] = tiempo_tabu + 1  # agrega el indice a la lista

                #update tabu times
                lista_tabu_temp = lista_tabu.copy()
                for key in lista_tabu.keys():
                    lista_tabu_temp[key] -= 1
                    if lista_tabu_temp[key] == 0:
                        del lista_tabu_temp[key]
                lista_tabu = lista_tabu_temp
                ###

                current_ils +=1
            lc  -= 1
            mejores_vos[i].append(best_vo)
            print("mejor solucion: ", best_solucion)
            print("mejor vo: ", best_vo)
    print(mejores_vos)
    iqrs = {
        "Temperatura": 0,
        "Humedad": 0,
        "Ruido": 0,
        "Int_luminosa": 0
    }
    for i in range(len(mejores_vos)):
        listIqr = list(iqrs.keys())[i]
        iqr = qr.interpolacion_Lineal(mejores_vos[i])
        iqrs[listIqr] = iqr
    print(iqrs)
    dg.actualizar_csv(iqrs)
        #soft and hard constrainst