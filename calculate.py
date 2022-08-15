# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import timeit
from gekko import GEKKO
import random

class Calculate:
    def __init__(self, cultivos, hora_inicio, hora_fin):
        self.__cultivos = cultivos
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
 
    def optimize(self):
        cultivos = self.__cultivos
        hora_inicio = self.__hora_inicio
        hora_fin = self.__hora_fin

        '''Iniciando contador de tiempo'''
        tiempoInicio = timeit.default_timer()

        ''' Configurando o GEKKO'''
        m = GEKKO(remote=False)  # Inicializando um modelo de GEKKO (Solución local)
        m.options.IMODE = 3     # Modo correspondente a optimización
        m.options.SOLVER = 1  # Tipo de solver (1=APOPT, 2=BPOPT, 3=IPOPT)
        ''' Fín de configuración  de GEKKO'''

        ''' Parámetros del modelo'''
        N =  len(cultivos) # número de líneas de cultivo
        T = 24  # tiempo

        # flujo por hora
        Fmax = 30
        Fsafe = 3

        # necesidad de agua de cultivo
        w = np.array()
        wn = np.array()
        for i in range(N):
            w[i] = cultivos[i][1]
            wn[i] = cultivos[i][1]

        ''' Fim de parâmetros do modelo'''

        ''' Calculos para simulaciones'''
        duracion_riego = 4
        
        rn = m.Array(m.Var, [N], lb=0, ub=hora_inicio)  # tiempo inicio
        dn = m.Array(m.Var, [N], lb=0, ub=hora_fin)  # tiempo finalización

        # Generamos hora de inicio y fín para cada cultivo
        for i in range(N):
            rn[i] = random.randint(1, 12)
            dn[i] = rn[i] + duracion_riego

        ''' Fín calculos simulaciones'''


        '''Variables del modelo'''
        # Flujo óptimo
        fnt = m.Array(m.Var, [N, T], lb=0, ub=Fsafe)

        # Flujo intermedio
        faux = m.Array(m.Var, [N], lb=0, ub=Fsafe)

        # Flujo Total
        F = m.Var(lb=0)
        '''Fín de variables del modelo'''

        '''Ecuaciones del modelo'''
        for i in range(N):
            faux[i] = m.Intermediate(
                m.sum([(fnt[i, j] - wn[i]) ** 2 for j in range(rn[i], dn[i])]))

        # Flujo total
        F = m.Intermediate(m.sum(faux))
        '''Fín de ecuaciones del modelo'''

        '''Restricciones del problema de optimización'''
        for j in range(T):
            # suma del flujo agua de todas las líneas por hora no debe superar Flujo max
            m.Equation(m.sum(fnt[:, j]) <= Fmax)

        for i in range(N):
            # suma del flujo de agua de horas riego por línea de cultivo Igua a necesidad
            m.Equation(m.sum(fnt[i, :]) == wn[i])
        '''Fím de restriciones'''

        '''Función Objetivo'''
        m.Obj(F)

        '''Resolviendo el problema de optimización'''
        m.solve(disp=True)

        '''Presentando los resultados en consola'''
        print('Resultados')
        print('Matriz de necesidad : \n' + str(wn))
        print('Matriz de flujo óptimo: \n' + str(fnt))
        print('Matriz de flujo auxiliar: \n' + str(faux))
        print('Flujo total = ' + str(F.value))

        ''' Finalizando contador de tiempo '''
        tiempoFin = timeit.default_timer()
        print('tiempo de ejecución: %f' % (tiempoFin - tiempoInicio))


        ''' Cálculos para graficos '''
        fgrafico = m.Array(m.Var, [N, T], lb=0, ub=Fsafe)
        ffijo = m.Array(m.Var, [N, T], lb=0, ub=Fsafe)
        for i in range(N):
            for j in range(T):
                fgrafico[i, j] = np.asarray(fnt[i, j])
                
        # Flujo por linea
        flineas = m.Array(m.Var, [N])
        flineas_fijo = m.Array(m.Var, [N])
        for k in range(N):
            flineas[k] = m.sum(np.asarray(fgrafico[k, :]))
            
        print('###### Graficos ########### \n')
        print('Matriz flujo de lineas óptimo : \n' + str(flineas))
        
        # Flujo por hora
        fhoras = m.Array(m.Var, [T], lb=0, ub=Fsafe)
        fhoras_fijo = m.Array(m.Var, [T])

        for j in range(T):
            fhoras[j] = m.sum(np.asarray(fgrafico[:, j]))
            fhoras_fijo[j] = m.sum(np.asarray(ffijo[:, j]))

        print('###### Graficos ########### \n')
        print('Matriz flujo horas óptimo: \n' + str(fhoras))
        print('Matriz flujo horas fijo: \n' + str(fhoras_fijo))
