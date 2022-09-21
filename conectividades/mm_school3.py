# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 18:03:05 2014

@author: elias
"""

import numpy as np
import math as ma
import networkx as nx
import matplotlib.pyplot as plt

#factorial
def facto(n):
    if n==0:
        return 1
    else:
        return n*facto(n-1)


#Cargar la matriz de encuestas
a=np.loadtxt('esc3.txt',dtype=float)

s=6 #Número de salones

#Convertir datos a relaciones de amistad 
n=a[0].size

for i in xrange(n):
    for j in xrange(n):
        if a[i,j]==5.0 or a[i,j]==6.0 or a[i,j]==2.0:
            a[i,j]=0.0
        elif a[i,j]==3.0 or a[i,j]==4.0:
            a[i,j]=1.0
            
#####Análisis matricial
suma_col=a.sum(axis=1)
#Caminos de longitud 1
l1=a.sum()
z1=l1/n

#Caminos de longitud 2
a2=np.dot(a,a)
for i in xrange(n):
    a2[i,i]=0
    for j in xrange(n):
        if a2[i,j]>0:
            a2[i,j]=1
        if a[i,j]==1:
            a2[i,j]=0
l2=a2.sum()
z2=l2/n

#Umbral de persolación
bc=l1/l2

######Análisis estadístico:
#Se cuenta el número de veces que aparece cierta cantidad de enlaces
pk=np.zeros(n)
for i in xrange(n):
    cont=0
    for j in xrange(n):
        if suma_col[j]==i:
            cont +=1
    pk[i]=cont
#Distribución de probabilidad real de la red:
pk=pk/n

#Distribución de los segundos vecinos:
k=np.arange(n)
zetak=np.zeros(n)
for i in xrange(n):
    zetak[i]=k[i]*pk[i]
zetak=zetak/z1

dos=np.zeros(n)
for i in xrange(n):
    dos[i]=(k[i]-1)*zetak[i]
z2e=dos.sum()

####Análisis probabilśtico
#Se contruye la distribución de Poisson:
pkp=np.zeros(n)
j=0.0
for i in xrange(n):
    pkp[i]=ma.exp(-z1)*z1**i/(facto(j))
    j+=1.0

#Se calculan los segundos vecino usando la distribución de Poisson
arg=np.zeros(n)
j=0.0
for i in xrange(n):
    arg[i]=k[i]*ma.exp(-z1)*z1**i/(facto(j))
    j+=1.0
z1p=arg[:170].sum()

j=0.0
arg2=np.zeros(n)
for i in xrange(n):
    arg2[i]=(k[i]-1)*k[i]*ma.exp(-z1)*z1**i/(facto(j))
    j+=1.0
z2p=arg2[:170].sum()

#Se genera el grapho
A=np.matrix(a)
G=nx.from_numpy_matrix(A)

#Resultados
print 'Friendship network measurements',':','School 3'
print 'Order :',G.order()
print 'Size :',G.size()
print 'Assortativity: ', nx.degree_assortativity_coefficient(G)
print 'z1 = %d/%d = %f' %(l1,n,z1)
print 'z2 = %d/%d = %f' %(l2,n,z2)
print 'Percolation Threshold bc =', bc
print 'Segundos vecinos, análisis estadístico:', z2e
print 'z1 análisis probabilístico:', z1p
print 'z2 análisis probabilístico:', z2p
print nx.number_connected_components(G)
print

#Gráfica:
#plt.plot(k,pk,'co',k,pkp,'r')
#plt.axis([0,25,0,0.15])  
#plt.show()

#Intersección
a=1-bc*z1
b=-(n+bc)
c=n*bc
x_1=-b/(2*a)+ma.sqrt(b**2-4*a*c)/(2*a)
x_2=-b/(2*a)-ma.sqrt(b**2-4*a*c)/(2*a)
print 'b suponiendo s=419', x_2

b=np.linspace(0,.5,10000)
s=b+(b**2*bc*l1/n)/(bc-b)
figura2=plt.plot(b,s,'c')
plt.axhline(color='k',linestyle='steps--')
plt.axhline(y=n,color='k',linestyle='steps--')
plt.axis([bc-0.01,bc+0.001,-0.5,n+5])
#Línea de intersección:
plt.axvline(x=bc,color='r',linestyle='steps--')
plt.axvline(x=x_2,color='k',linestyle='steps--')
plt.xlabel('Fraction of connected nodes', size=15)
plt.ylabel('Component size average', size=15)
plt.text(0.229,400,r"$(0.230,419)$", fontsize=14, color="black")