# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np
import timeit
from gekko import GEKKO
import random

'''Iniciando contador de tiempo'''
TiempoInicio = timeit.default_timer()

''' Configurando o GEKKO'''
m = GEKKO(remote=False)  # Inicializado um modelo de GEKKO (Solución local)
m.options.IMODE = 3     # Modo correspondente a optimización
m.options.SOLVER = 1  # Tipo de solver (1=APOPT, 2=BPOPT, 3=IPOPT)
''' Fin de configuración deGEKKO'''

''' Parámetros del modelo'''
N_lineas = 10
N_horas = 24
f_max = 30  # flujo máximo
f_safe = 3  # flujo seguro

# necesidad por dia
w = np.array([4.93, 5.47, 3.82, 5.11, 7.22, 4.44, 3.47, 4.93, 5.04, 2.59])
wn = np.array([4.93, 5.47, 3.82, 5.11, 7.22, 4.44, 3.47, 4.93, 5.04, 2.59])
# wn = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
rn = np.array([3, 2, 0, 5, 7, 1, 4, 12, 9, 6])
dn = np.array([7, 6, 4, 9, 11, 5, 8, 16, 13, 10])


# variaciónn de la necesidad
variacion_necesidad = random.uniform(0, 5)
signo_variacion = random.randint(0, 1)
duracion_riego = 4

# rn = m.Array(m.Var, [N_lineas], lb=1, ub=12)
# dn = m.Array(m.Var, [N_lineas], lb=1, ub=12)

# Generamos hora de inicio y fin de cada cultivo
'''for i in range(N_lineas):
    rn[i] = random.randint(1, 12)
    dn[i] = rn[i] + duracion_riego
'''

# Generamos la variacion de la necesidad de cada cultivo en +- 0 a 5%
'''for i in range(N_lineas):
    if (signo_variacion == 1):
        wn[i] = w[i]+(w[i] * variacion_necesidad / 100)
    else:
        wn[i] = w[i]-(w[i] * variacion_necesidad / 100)'''
''' Fin de parámetros do modelo'''

'''Variables de modelo'''
# Flujo deseado
flujo_nt = m.Array(m.Var, [N_lineas, N_horas], lb=0, ub=f_safe)

# Flujo intermedio
flujo_intermedio = m.Array(m.Var, [N_lineas], lb=0, ub=f_safe)

# Flujo Total
Total_flujo = m.Var(lb=0)
'''Fin de variables de modelo'''


'''Ecuaciones de modelo'''
# Flujo calculo
for i in range(N_lineas):
    flujo_intermedio[i] = m.Intermediate(
        m.sum([(flujo_nt[i, j] - wn[i]) ** 2 for j in range(rn[i], dn[i])]))

# Flujo total
Total_flujo = m.Intermediate(m.sum(flujo_intermedio))
'''Fin de ecuaciones de modelo'''


'''Restricciones del problema de optimización'''

for j in range(N_horas):
    # Flujo por hora de todas las líneas sea <= flujo máximo
    m.Equation(m.sum(flujo_nt[:, j]) <= f_max)


for i in range(N_lineas):
    # Flujo por línea de todas las horas sea = necesidad de agua
    m.Equation(m.sum(flujo_nt[i, :]) <= wn[i])

'''Fin de restricciones del problema de optimización'''

'''Función Objetivo'''
m.Obj(Total_flujo)

'''Resolviendo el problema de optimización'''
m.solve(disp=True)

'''Presentando los resultados en consola'''
print('Resultados')
print('Matriz de necesidad : \n' + str(wn))
print('Matriz de flujo deseado: \n' + str(flujo_nt))
# print('Flujo intermedio calculo = ' + str(flujo_intermedio))
print('Flujo total = ' + str(Total_flujo.value))

''' Finalizando contador de tiempo '''
TiempoFim = timeit.default_timer()
print('Tiempo de ejecución: %f' % (TiempoFim - TiempoInicio))


''' Calculos para gráficos ....'''

fgrafico = m.Array(m.Var, [N_lineas, N_horas], lb=0, ub=f_safe)
flujo_fijo = m.Array(m.Var, [N_lineas, N_horas], lb=0, ub=f_safe)
for i in range(N_lineas):
    for j in range(N_horas):
        fgrafico[i, j] = np.asarray(flujo_nt[i, j])
        if(np.asarray(flujo_nt[i, j]) > 0):
            flujo_fijo[i, j] = f_safe/2
        else:
            flujo_fijo[i, j] = 0


# Flujo por linea
flineas = m.Array(m.Var, [N_lineas], lb=0, ub=f_safe)
flineas_fijo = m.Array(m.Var, [N_lineas])
for i in range(N_lineas):
    flineas[i] = m.sum(np.asarray(fgrafico[i, :]))
    flineas_fijo[i] = m.sum(np.asarray(flujo_fijo[i, :]))

print('----------------------------------------------------- \n\n')
print('Matriz flujo óptimo por líneas : \n' + str(flineas))
print('Matriz flujo fijo por líneas : \n' + str(flineas_fijo))

# Flujo por hora
fhoras = m.Array(m.Var, [N_horas], lb=0, ub=f_safe)
fhoras_fijo = m.Array(m.Var, [N_horas])

for j in range(N_horas):
    fhoras[j] = m.sum(np.asarray(fgrafico[:, j]))
    fhoras_fijo[j] = m.sum(np.asarray(flujo_fijo[:, j]))

print('----------------------------------------------------- \n\n')
print('Matriz flujo óptimo por horas : \n' + str(fhoras))
print('Matriz flujo fijo por horas  \n' + str(fhoras_fijo))


# [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
x = np.arange(N_horas)


plt.figure(figsize=(16, 8))
plt.title('Cantidad de agua suministrada',
          fontdict={'fontsize': 16})
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (30, 30),
          'axes.labelsize': 'small',
          'axes.titlesize': 'small',
          'xtick.labelsize': 'small',
          'ytick.labelsize': 'small'}
plt.rcParams.update(params)

plt.subplot(3, 1, 1)
plt.plot(x, fgrafico[0, :], 'g-', label='Poroto')
plt.plot(x, fgrafico[1, :], 'b-', label='Arroz')
plt.plot(x, fgrafico[2, :], 'r-', label='Tomate')
plt.plot(x, fgrafico[3, :], '-k', label='Maiz')
plt.plot(x, fgrafico[4, :], '-c', label='Frijol')
plt.plot(x, fgrafico[5, :], '-m', color='darkslategrey', label='Cebolla')
plt.plot(x, fgrafico[6, :], '-', color='orange', label='Naranja')
plt.plot(x, fgrafico[7, :], '-', color='yellow', label='Platano')
plt.plot(x, fgrafico[8, :], '-', color='purple', label='Camote')
plt.plot(x, fgrafico[9, :], '-', color='saddlebrown', label='Yuca')
plt.legend(fontsize=10)
yticks = np.arange(0, 2, 0.2)
xticks = np.arange(0, N_horas, 1)
plt.xticks(xticks)
plt.yticks(yticks)
plt.ylabel('Consumo agua(lt)', fontsize=8)
plt.xlabel('Periodo riego (horas)', fontsize=8)

plt.subplot(3, 1, 2)
# plt.plot(x, fhoras, '-', color='orange', label='Consumo total - flujo óptimo')
plt.plot(x, fhoras_fijo, '--*', color='royalblue',
         label='Consumo total - flujo fijo')
plt.legend(fontsize=7)
plt.ylabel('Consumo agua(lt)', fontsize=8)
plt.xlabel('Periodo riego (horas)', fontsize=8)
yticks = np.arange(0, 10, 1)
xticks = np.arange(0, N_horas, 1)
plt.xticks(xticks)
plt.yticks(yticks)


plt.subplot(3, 1, 3)
indice = np.arange(N_lineas)
ancho = 0.25
plt.bar(indice, wn, width=ancho, color='seagreen',
        label='Cantidad de agua deseada')
plt.bar(indice+ancho, [flineas[0], flineas[1], flineas[2], flineas[3], flineas[4], flineas[5], flineas[6], flineas[7], flineas[8], 2.59], width=ancho, color='orange',
        label='Cantidad de agua con flujo óptimo')
plt.bar(indice+ancho+ancho,
        flineas_fijo, width=ancho, color='royalblue', label='Cantidad de agua con flujo fijo(Fsafe/2)')
plt.xticks(indice+ancho, ('Poroto', 'Arroz', 'Tomate', 'Maiz',
           'Frijol', 'Cebolla', 'Naranja', 'Platano', 'Camote', 'Yuca'))
plt.ylabel('Cantidad agua suministrada', fontsize=8)
plt.xlabel('Tipos de plantas', fontsize=8)
plt.legend(fontsize=7)
yticks = np.arange(0, 10, 1)
plt.yticks(yticks)

plt.subplots_adjust(left=0.15,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.5)
plt.show()
