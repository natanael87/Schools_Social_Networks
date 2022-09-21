# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 17:57:27 2014

@author: elias
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 

def segundosv(a2,a1):
    for i in range(n):
        if a2[i,i]!=0.0:
                a2[i,i]=0.0
        for j in range(n):
            if a2[i,j]!=0.0:
                a2[i,j]=1.0
            if a1[i,j]==1.0:
                a2[i,j]=0.0


E=nx.read_adjlist('ene1CG.txt',nodetype=int)

a1=nx.to_numpy_matrix(E)

n=np.size(a1[0])

"""Caminos de longitud 1"""
l1=a1.sum()
"""Promedio de primeros vecinos"""
z1=l1/n
  
     
"""Caminos de longitud 2"""
a2=np.dot(a1,a1)
segundosv(a2,a1)
l2=a2.sum()

"""Promedio de segundos vecinos"""
z2=l2/n

#Umbral de percolación
bc =l1/l2

"""Aproximacion numerica umbral percolacion"""

def f(x):
    return x+(np.power(x,2)*np.power(z1,2))/(z1-x*z2)

from scipy.optimize import brentq 
sol1 = brentq(f, 0.3, 0.4)

from scipy.optimize import bisect
sol2 = bisect(f,0.3,0.4)

from scipy.optimize import ridder
sol3 = ridder(f,0.3,0.4)

from scipy.optimize import newton
sol4 = newton(f, 0.35)

print 'Friendship network measurements:','School 1'
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
print

#Resultados
print 'Paths length 1:',l1,',','z1:',z1
print 'Paths length 2:',l2,',','z2:',z2
print 'Percolation threshold bc:',z1/z2
print 'Número de nodos', n

#Gráficas
b=np.linspace(0,0.4,1000)
s=b+(np.power(b,2)*np.power(z1,2))/(z1-b*z2)
P=[x_2, p_2]
y=[(z1/z2)*n, n]

plt.subplot(3,1,1)
plt.axhline(y=(z1/z2)*n,color='black',linestyle='steps--')
plt.axhline(y=n,color='red',linestyle='steps-.')
plt.axvline(x=z1/z2,color='black',linestyle='steps--')
plt.axvline(x=x_2,color='black',linestyle='steps--')
plt.text(x_2-.008,(z1/z2)*n+1,r"$P$", fontsize=14, color="black")
plt.text(p_2+.001, n+1,r"$Q$", fontsize=14, color="black")
plt.text(0.0018,n+5,r"$82$", fontsize=14, color="black")
plt.text(0.0018,(z1/z2)*n+4,r"$29.62$", fontsize=14, color="black")
plt.text(0.38,100,'a', fontsize=14, color="black")
plt.axis([0,0.4, -50, n+50])
plt.tick_params(axis='both', which='major', labelsize=10)
plt.plot(b,s, P,y, 'go')