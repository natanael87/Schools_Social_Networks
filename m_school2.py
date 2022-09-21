# -*- coding: utf-8 -*-
"""
Created on Wed May 28 21:36:57 2014

@author: elias
"""

import numpy as np
from math import *
import networkx as nx
import matplotlib.pyplot as plt

#Cargar la matriz de encuestas
a=np.loadtxt('esc2.txt',dtype=float)

#Convertir datos a relaciones de amistad 
n=a[0].size
print n

for i in xrange(n):
    for j in xrange(n):
        if a[i,j]==5.0 or a[i,j]==6.0 or a[i,j]==2.0:
            a[i,j]=0.0
        elif a[i,j]==3.0 or a[i,j]==4.0:
            a[i,j]=1.0
            
################## Método 1
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

#Transición de fase
bc=l1/l2

################ Método 2
#Función Gamma:
# Coefficients used by the GNU Scientific Library
g = 7
p = array([0.99999999999980993, 676.5203681218851, -1259.1392167224028,
     771.32342877765313, -176.61502916214059, 12.507343278686905,
     -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7])

def gamma(z):
    #z = complex(z)
    # Reflection formula
    if z < 0.5:
        return pi / (sin(pi*z) * gamma(1-z))
    else:
        z -= 1
        x = p[0]
        for i in range(1, g+2):
            x += p[i]/(z+i)
        t = z + g + 0.5
        return sqrt(2*pi) * t**(z +0.5) * exp(-t) * x

    
#Uno sobre gamma
def i_gamma(k):
    #k = complex(k)
    # Reflection formula
    if k < 0.5:
        return 1/gamma(k)
    else:
        k -= 1
        x = p[0]
        for i in range(1, g+2):
            x += p[i]/(k+i)
        t = k + g + 0.5
        return t**(-k-0.5) * exp(t)/(sqrt(2*pi)  * x)

#Función a integrar (Numerador)
def f(k):
    return k*(k-1)*z1**k*i_gamma(k+1)    

#Método de simpsom
def simp(a,b,n):
    if n%2 != 0:
        n=n+1
        
    h=(b-a)/n
    sum_par=0.0
    sum_impar=0.0
    
    x_par=a    
    for i in range(n/2):
        x_par+=2*h
        sum_par+=f(x_par)
    x_impar=a+h
    for i in range(n/2):
        sum_impar+=f(x_impar)
        x_impar+=2*h
    
    area=(h/3)*(f(a)+f(b)+4*sum_par+2*sum_impar)
    return area

int01=simp(0.0,1.0,10000)
int0100=simp(1.,100.,10000)*exp(-z1)
#int141=simp(100.,148.,10000)*exp(-z)
#print i_gamma(148)

#Número proedio de segundos vecinos:
z2_int=exp(-z1)*int01+int0100
#z2_1=exp(-z)*int01.real+int0100.real

#Función a integrar: (Denominador)
def pro(k):
    return k*z1**k*i_gamma(k+1)

#Integración por método de Simpsom:
def simp2(a,b,n):
    if n%2 != 0:
        n=n+1
        
    h=(b-a)/n
    sum_par=0.0
    sum_impar=0.0
    
    x_par=a    
    for i in range(n/2):
        x_par+=2*h
        sum_par+=pro(x_par)
    x_impar=a+h
    for i in range(n/2):
        sum_impar+=pro(x_impar)
        x_impar+=2*h
    
    area=(h/3)*(pro(a)+pro(b)+4*sum_par+2*sum_impar)
    return area

int_pro=simp2(0.0,60,10000)
#Número promedio de primeros vecinos:
z1_int=(int_pro)*exp(-z1)

#Transición de fase:
bc_ap=z1_int/z2_int

#grapho
A=np.matrix(a)
G=nx.from_numpy_matrix(A)

#Resultados:
print 'Friendship network measurements',':','School 2'
print 'Order :',G.order()
print 'Size :',G.size()
print
print 'z1:', l1/n
print 'z2',z2
print 'bc:', bc
print
print 'z2 aproximado:',z2_int
print 'z1 aproximado:', z1_int
print 'bc aproximado:', bc_ap
print

#Intersección
a=1-bc*z1
b=-(n+bc)
c=n*bc
x_1=-b/(2*a)+sqrt(b**2-4*a*c)/(2*a)
x_2=-b/(2*a)-sqrt(b**2-4*a*c)/(2*a)
print x_1, x_2

#Gráfica:
b=np.linspace(0,.2,10000)
s=b+(b**2*bc*l1/n)/(bc-b)
figura2=plt.plot(b,s,'c')
plt.axhline(color='k',linestyle='steps--')
plt.axhline(y=n,color='k',linestyle='steps--')
plt.axis([bc-0.01,bc+0.001,-0.5,n+5])
#Línea de intersección:
plt.axvline(x=bc,color='r',linestyle='steps--')
plt.axvline(x=x_2,color='k',linestyle='steps--')
#plt.xlabel('b:fraccion de nodos conectados')
#plt.ylabel('s: Tamanio promedio de componente')