# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import timeit
from gekko import GEKKO
import random

'''Iniciando contador de tiempo'''
tiempoInicio = timeit.default_timer()

''' Configurando o GEKKO'''
m = GEKKO(remote=False)  # Inicializando um modelo de GEKKO (Solución local)
m.options.IMODE = 3     # Modo correspondente a optimización
m.options.SOLVER = 1  # Tipo de solver (1=APOPT, 2=BPOPT, 3=IPOPT)
''' Fín de configuración  de GEKKO'''

''' Parámetros del modelo'''
N = 10  # número de líneas de cultivo
T = 24  # tiempo

# flujo por hora
Fmax = 30
Fsafe = 3

# necesidad de agua de cultivo
w = np.array([4.93, 5.47, 3.82, 5.11, 7.22, 4.44, 3.47, 4.93, 5.04, 2.59])
wn = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
''' Fim de parâmetros do modelo'''

''' Calculos para simulaciones'''
# variacion de la necesidad
variacion_necesidad = random.uniform(0, 5)
signo_variacion = random.randint(0, 1)
duracion_riego = 4

rn = m.Array(m.Var, [N], lb=0, ub=12)  # tiempo inicio
dn = m.Array(m.Var, [N], lb=0, ub=16)  # tiempo finalización

# Generamos hora de inicio y fín para cada cultivo
for i in range(N):
    rn[i] = random.randint(1, 12)
    dn[i] = rn[i] + duracion_riego

# Generamos la variación de la necesidad agua para cada cultivo en +- 0 a 5%
for i in range(N):
    if (signo_variacion == 1):
        wn[i] = w[i]+(w[i] * variacion_necesidad / 100)
    else:
        wn[i] = w[i]-(w[i] * variacion_necesidad / 100)
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
        if(np.asarray(fnt[i, j]) > 0):
            ffijo[i, j] = Fsafe  # Fsafe/2
        else:
            ffijo[i, j] = 0


# Flujo por linea
flineas = m.Array(m.Var, [N])
flineas_fijo = m.Array(m.Var, [N])
for k in range(N):
    flineas[k] = m.sum(np.asarray(fgrafico[k, :]))
    flineas_fijo[k] = m.sum(np.asarray(ffijo[k, :]))

print('###### Graficos ########### \n')
print('Matriz flujo de lineas óptimo : \n' + str(flineas))
print('Matriz flujo de lineas fijo: \n' + str(flineas_fijo))

# Flujo por hora
fhoras = m.Array(m.Var, [T], lb=0, ub=Fsafe)
fhoras_fijo = m.Array(m.Var, [T])

for j in range(T):
    fhoras[j] = m.sum(np.asarray(fgrafico[:, j]))
    fhoras_fijo[j] = m.sum(np.asarray(ffijo[:, j]))

print('###### Graficos ########### \n')
print('Matriz flujo horas óptimo: \n' + str(fhoras))
print('Matriz flujo horas fijo: \n' + str(fhoras_fijo))


x = np.arange(T)

plt.figure(figsize=(16, 8))
plt.title('Flujo de consumo de agua', fontdict={'fontsize': 20})
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (30, 30),
          'axes.labelsize': 'x-small',
          'axes.titlesize': 'small',
          'xtick.labelsize': 'x-small',
          'ytick.labelsize': 'x-small'}
plt.rcParams.update(params)

plt.subplot(1, 1, 1)
plt.plot(x, fgrafico[0, :], 'g-', label='Poroto')
plt.plot(x, fgrafico[1, :], 'b-', label='Arroz')
plt.plot(x, fgrafico[2, :], 'r-', label='Tomate')
plt.plot(x, fgrafico[3, :], 'k-', label='Maiz')
plt.plot(x, fgrafico[4, :], 'c-', label='Frijol')
plt.plot(x, fgrafico[5, :], 'm-', label='Cebolla')
plt.plot(x, fgrafico[6, :], '-', color='orange', label='Naranja')
plt.plot(x, fgrafico[7, :], '-', color='yellow', label='Platano')
plt.plot(x, fgrafico[8, :], '-', color='purple', label='Camote')
plt.plot(x, fgrafico[9, :], '-', color='indigo', label='Yuca')
plt.legend(fontsize=6)
plt.ylabel('Consumo agua(lt)', fontsize=8)
plt.xlabel('Periodo riego (horas)', fontsize=8)

'''
plt.subplot(3, 1, 2)
plt.plot(x, fhoras, '-', color='orange', label='Consumo total - flujo óptimo')
plt.plot(x, fhoras_fijo, '--*', color='royalblue',
         label='Consumo total - flujo fijo')
plt.legend(fontsize=7)
plt.ylabel('Consumo agua(lt)', fontsize=8)
plt.xlabel('Periodo riego (horas)', fontsize=8)


plt.subplot(3, 1, 3)
indice = np.arange(N)
ancho = 0.25
plt.bar(indice, w, width=ancho, color='seagreen',
        label='Cantidad de agua deseada')
plt.bar(indice+ancho, [flineas[0], flineas[1], flineas[2], flineas[3], flineas[4], flineas[5], flineas[6], flineas[7], flineas[8], 0], width=ancho, color='orange',
        label='Cantidad de agua con flujo óptimo')
plt.bar(indice+ancho+ancho,
        flineas_fijo, width=ancho, color='royalblue', label='Cantidad de agua con flujo fijo')
plt.xticks(indice+ancho, ('Poroto', 'Arroz', 'Tomate', 'Maiz',
           'Frijol', 'Cebolla', 'Naranja', 'Platano', 'Camote', 'Yuca'))
plt.ylabel('Cantidad agua suministrada', fontsize=8)
plt.xlabel('Tipos de plantas', fontsize=8)
plt.legend(fontsize=7)
plt.subplots_adjust(left=0.15,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.5)

                    '''
plt.show()
