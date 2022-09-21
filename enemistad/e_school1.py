# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 12:42:19 2014

@author: elias
"""

import numpy as np
import networkx as nx
import math as ma
import matplotlib.pyplot as plt 
import powerlaw as pw

xmin=2

def argumento(lista,i):
    return ma.log(lista[i]/(xmin-0.5))
    
def sumatoria(kmin,kmax, func, lista):
    suma=0.0
    for i in range(kmin,kmax+1):
        suma+=func(lista,i)
    return suma
    

"""Cargar la matriz de encuestas de la Escuela 1"""
a=np.loadtxt('esc1.txt',dtype=float)

n=a[0].size  #Número de estudiantes

"""Se construye la matriz de adyacencia""" 

for i in range(n):
    for j in range(n):
        if a[i,j]==6.0 or a[i,j]==5.0 or a[i,j]==4.0 or a[i,j]==3.0 or a[i,j]==1.0:
            a[i,j]=0.0
        elif a[i,j]==2.0:
            a[i,j]=1.0
####Método 1        
"""Caminos de longitud 1"""
l1=a.sum()
"""Promedio de primeros vecinos"""
z1=l1/n
"""Caminos de longitud 2"""
a2=np.dot(a,a)
for i in xrange(n):
    a2[i,i]=0
    for j in xrange(n):
        if a2[i,j]>0:
            a2[i,j]=1
l2=a2.sum()
"""Promedio de segundos vecinos"""
z2=l2/n

"""Transición de fase"""
bc=l1/l2

#Ajuste de Komogolov:
suma_col=a.sum(axis=1)
k=np.arange(n)
datak=np.zeros(n)
for i in xrange(n):
    cont=0
    for j in xrange(n):
        if suma_col[j]==i:
            cont +=1
    datak[i]=cont
#Distribución de probabilidad real de la red:
alpha=1+10/(sumatoria(1,10,argumento,datak))
print 'alpha', alpha

#Ajuste de ley de potencias:
ajuste = pw.Fit(datak)
print ajuste.power_law.alpha
print ajuste.power_law.xmin
R, p = ajuste.distribution_compare('power_law', 'lognormal')
print R
print p
#plt.plot(np.arange(11),datak[:11],'o', np.arange(11),datak[:11], 'r')