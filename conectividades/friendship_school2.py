# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 23:14:36 2014

@author: elias
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt 

"""Matriz de encuestas de la Escuela 1"""
a=np.loadtxt('esc2.txt',dtype=float)

n=a[0].size #Número de estudiantes =226


"""Matriz de adyacencia de la red de amistad""" 

for i in range(n):
    for j in range(n):
        if a[i,j]==5.0 or a[i,j]==6.0 or a[i,j]==2.0:
            a[i,j]=0.0
        elif a[i,j]==3.0 or a[i,j]==4.0:
            a[i,j]=1.0
 
       
"""Caminos de longitud 1"""
l1=a.sum()
"""Promedio de primeros vecinos"""
z1=l1/n
  
     
"""Caminos de longitud 2"""
a2=np.dot(a,a)
for i in range(n):
    if a2[i,i]!=0.0:
            a2[i,i]=0.0
    for j in range(n):
        if a2[i,j]!=0.0:
            a2[i,j]=1.0
        if a[i,j]==1.0:
            a2[i,j]=0.0
l2=a2.sum()
"""Promedio de segundos vecinos"""
z2=l2/n

#Umbral de percolación
bc=l1/l2


"""Grafo de la red y medidas de centralidad"""

A=np.matrix(a)
G=nx.from_numpy_matrix(A)
print 'Friendship network measurements:','School 2'
print 'Order:',G.order()
print 'Size:',G.size()
print 'Paths length 1:',l1,',','z1:',z1
print 'Paths length 2:',l2,',','z2:',z2
print 'Percolation threshold bc:',z1/z2
print 'Diameter:',nx.diameter(G)
print 'Density:',nx.density(G)
print 'Clustering:',nx.average_clustering(G)
print ''

"""Aproximacion numerica umbral percolacion"""

def f(x):
    return x+(np.power(x,2)*np.power(z1,2))/(z1-x*z2)

from scipy.optimize import brentq 
sol1 = brentq(f, 0.15, 0.25)

from scipy.optimize import bisect
sol2 = bisect(f,0.15,0.25)

from scipy.optimize import ridder
sol3 = ridder(f,0.15,0.25)

from scipy.optimize import newton
sol4 = newton(f, 0.2)

print 'Numerical methods to find a zero of a function:'
print '  Brent          Bisection         Ridder         Newton'
print sol1, sol2, sol3, sol4
print

#Intersección 1
a=1-bc*z1
b=-(bc*n+bc)
c=n*bc*bc
x_1=-b/(2*a)+np.sqrt(b**2-4*a*c)/(2*a)
x_2=-b/(2*a)-np.sqrt(b**2-4*a*c)/(2*a)
print 'b con s=%f: %f' %(n*bc, x_2)

#Intersección 2
a=1-bc*z1
b=-(n+bc)
c=n*bc
p_1=-b/(2*a)+np.sqrt(b**2-4*a*c)/(2*a)
p_2=-b/(2*a)-np.sqrt(b**2-4*a*c)/(2*a)
print 'b con s=%f: %f' %(n, p_2)

#Gráficas
b=np.linspace(0,0.25,1000)
s=b+(np.power(b,2)*np.power(z1,2))/(z1-b*z2)
P=[x_2, p_2]
y=[(z1/z2)*n, n]

plt.subplot(3,1,2)
plt.axhline(y=(z1/z2)*n,color='black',linestyle='steps--')
plt.axhline(y=n,color='red',linestyle='steps-.')
plt.axvline(x=z1/z2,color='black',linestyle='steps--')
plt.axvline(x=x_2,color='black',linestyle='steps--')
plt.text(x_2-.005,(z1/z2)*n+1,r"$P$", fontsize=14, color="black")
plt.text(p_2+.001, n+1,r"$Q$", fontsize=14, color="black")
plt.text(0.0018,n+5,r"$226$", fontsize=14, color="black")
plt.text(0.0018,(z1/z2)*n+4,r"$42.26$", fontsize=14, color="black")
plt.text(0.24,220,'b', fontsize=14, color="black")
plt.axis([0,0.25, -50, n+50])
plt.tick_params(axis='both', which='major', labelsize=12)
#plt.title('Robustness of the network', fontsize=12)
#plt.xlabel("Connected vertices $b$", fontsize=12)
plt.ylabel("$Tama\~no \ promedio \ de \ componente \ s$", fontsize=16)
plt.plot(b,s, P,y, 'go')