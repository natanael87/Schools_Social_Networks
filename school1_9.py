# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 14:26:32 2014

@author: elias
"""

import numpy as np
import math as ma
import networkx as nx
import matplotlib.pyplot as plt

#Distribución de probabilidad binomial
def comb(n,k):
    if n-k >=0 and k >= 0:
        return ma.factorial(n)/(ma.factorial(n-k)*ma.factorial(k))
        
def bi(n,p,k):
    return comb(n,k)*p**k*(1-p)**(n-k)
    


#Cargar la matriz de encuestas
a=np.loadtxt('esc1.txt',dtype=float)

s=6 #Número de salones

#Convertir datos a relaciones de amistad 
n=a[0].size

for i in xrange(n):
    for j in xrange(n):
        if a[i,j]==5.0 or a[i,j]==6.0 or a[i,j]==2.0:
            a[i,j]=0.0
        elif a[i,j]==3.0 or a[i,j]==4.0:
            a[i,j]=1.0

#
arch=a[:8,:8]
np.savetxt('/home/elias/PY/arch2.txt',a,fmt='%d')

ns=8        
print a[:ns, :ns]
print

#####Análisis matricial
a9=a[:ns, :ns]
g=nx.from_numpy_matrix(a9)
suma_col=a9.sum(axis=1)
#Caminos de longitud 1
l19=a9.sum()
z19=l19/ns

#Caminos de longitud 2
a92=np.dot(a9,a9)
for i in xrange(ns):
    a92[i,i]=0
    for j in xrange(ns):
        if a92[i,j]>0:
            a92[i,j]=1
        if a9[i,j]==1:
            a92[i,j]=0
l29=a92.sum()
z29=l29/ns
print a92
print
#
m2=np.dot(a9,a9)
z2m=(m2.sum()-l19)/l19
######Análisis estadístico:
#Se cuenta el número de veces que aparece cierta cantidad de enlaces
pk=np.zeros(ns)
for i in xrange(ns):
    cont=0
    for j in xrange(ns):
        if suma_col[j]==i:
            cont +=1
    pk[i]=cont
#Distribución de probabilidad real de la red:
pk9=pk/ns

#Distribución de los segundos vecinos:
k=np.arange(ns)
zetak=np.zeros(ns)
for i in xrange(ns):
    zetak[i]=k[i]*pk9[i]
zetak9=zetak/z19

dos=np.zeros(ns)
for i in xrange(ns):
    dos[i]=(k[i]-1)*zetak9[i]
z29a=dos.sum()

####Análisis probabilśtico
#Se contruye la distribución binomial
ps9=z19/(ns-1)
pkb=np.zeros(ns)
for i in xrange(ns):
    pkb[i]=bi(ns,ps9,i)
    
#Se calculan los primeros vecinos usando la distribución Binomial
arg=np.zeros(ns)
for i in xrange(ns):
    arg[i]=k[i]*bi(ns,ps9,i)
z19p=arg.sum()
   
arg2=np.zeros(ns)
for i in xrange(ns):
    arg2[i]=(k[i]-1)*k[i]*bi(ns,ps9,i)
z29p=arg2.sum()

#Gráfica:
print suma_col
print pk
print 'p(k):',pk9
print 'Distribución binomial:',pkb
print 'Cálculo matricial: z1 = %f/%f = %f' %(l19,ns,z19)
print 'Cálculo matricial: z2 = %f/%f = %f' %(l29,ns,z29)
print 'z2 estadísto', z29a
print 'z1 probabilístico', z19p
print 'z2 probabilístico', z29p
print 'z2 prueba', z2m
#nx.draw(g)
plt.plot(k,pk9,'co',k,pkb,'r')
plt.axis([0,ns,0,0.5])  
plt.show()