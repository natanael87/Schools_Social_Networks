# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
import math as ma
import matplotlib.pyplot as plt 

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
#Método 1        
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

####Análisis probabilśtico 1
#Se contruye la distribución de Libre de Escala:
kmin=2
alpha=2.6
A=(alpha-1)/kmin

k=np.arange(n)
pkl=np.zeros(n)
for i in xrange(kmin):
    j=float(i)
    pkl[i]=ma.exp(-alpha*(j/kmin-1))
for i in xrange(kmin,n):
    i0=float(i)
    pkl[i]=(i0 /kmin)**(-alpha)
pkl=pkl*A
    
#Se calculan los primeros vecinos usando la distribución de Power Law:
arg=0.0
for i in xrange(n):
    arg+=k[i]*pkl[i]
z1p=arg

#Se calculan los segundos vecinos usando la distribución de Power Law:
arg2=0.0
for i in xrange(n):
    arg2+=(k[i]-1)*k[i]*pkl[i]
z2p=arg2

####Análisis probabilśtico 2
#Se contruye la distribución de Libre de Escala:
C=39.64
gamma=1.25

pkl2=np.zeros(n)
for i in xrange(1,n-1):
    pkl2[i]=i**(-gamma)
pkl2=pkl2*C
    
#Se calculan los primeros vecinos usando la distribución de Poisson
arg3=np.zeros(n)
for i in xrange(n):
    arg3[i]=k[i]*pkl2[i]
z1p2=arg3.sum()

#Se calculan los segundos vecinos usando la distribución de Poisson
arg4=np.zeros(n)
for i in xrange(n):
    arg4[i]=(k[i]-1)*k[i]*pkl2[i]
z2p2=arg4.sum()


"""Se genera el grafo de la red """
A=np.matrix(a)
G=nx.from_numpy_matrix(A)

#Se calculan las componentes
l=nx.connected_components(G)
if len(l)!=0:
    tam=np.zeros(len(l))
    print '-El tamaño de cada comunidad es:'     
    ini=0
    for i in range(len(l)):
        tam[i]=len(l[i])
        ini+=tam[i]
        print '[%d]: %d'%(i,len(l[i]))
        print 'Los nodos incluidos son:',l[i]
    print
    Phi=np.ma.max(tam)/n
    print 'Tamaño de la comunidad mayor:', np.ma.max(tam)
    print 'Tamaño relativo del cluster máximo:', Phi
else:
    Phi=0
    print '-No se encontraron componentes'

def f(x):
    return x+(np.power(x,2)*np.power(z1,2))/(z1-x*z2)

from scipy.optimize import brentq 
sol1 = brentq(f, 0.3, 0.45)

from scipy.optimize import bisect
sol2 = bisect(f,0.3,0.45)

from scipy.optimize import ridder
sol3 = ridder(f,0.3,0.45)

from scipy.optimize import newton
sol4 = newton(f, 0.3)

print 'Enmity network measurements',':','School 1'

print 'Numerical methods to find a zero of a function:'
print '  Brent          Bisection         Ridder         Newton'
print sol1, sol2, sol3, sol4
print

print nx.is_connected(G)
print nx.number_connected_components(G)
print nx.connected_components(G)
s_pro=89.0/nx.number_connected_components(G)
print 'Tamaño promedio de componente: ', s_pro
print

#Intersección 1
a=1-bc*z1
b=-(s_pro+bc)
c=s_pro*bc
x_1=-b/(2*a)+np.sqrt(b**2-4*a*c)/(2*a)
x_2=-b/(2*a)-np.sqrt(b**2-4*a*c)/(2*a)
print 'b con s=%f: %f' %(s_pro, x_2)

#Intersección 2
a=1-bc*z1
b=-(n*bc+bc)
c=bc*n*bc
p_1=-b/(2*a)+np.sqrt(b**2-4*a*c)/(2*a)
p_2=-b/(2*a)-np.sqrt(b**2-4*a*c)/(2*a)
print 'b con s=%f: %f' %(n*bc, p_2)

print 'Order:',G.order()
print 'Size:',G.size()
print 'Paths length 1:',l1,',','z1:',z1
print 'Paths length 2:',l2,',','z2:',z2
print 'Percolation threshold bc:',z1/z2
print 'Density:',nx.density(G)
print 'Clustering:',nx.average_clustering(G)
print
print 'z1 análisis probabilístico:', z1p
print 'z2 análisis probabilístico:', z2p
print
print 'z1 análisis probabilístico 2:', z1p2
print 'z2 análisis probabilístico 2:', z2p2

#Gráficas
b=np.linspace(0,0.4,1000)
s=b+(np.power(b,2)*np.power(z1,2))/(z1-b*z2)
P=[x_2, p_2]
y=[s_pro, n*bc]

plt.subplot(3,1,1)
plt.axhline(y=s_pro,color='black',linestyle='steps--')
plt.axhline(y=(z1/z2)*n,color='black',linestyle='steps-.')
plt.axvline(x=z1/z2,color='red',linestyle='steps--')
plt.axvline(x=x_2,color='black',linestyle='steps--')
plt.text(p_2+.002,(z1/z2)*n,r"$P$", fontsize=14, color="black")
plt.text(x_2+.001, s_pro+3,r"$Q$", fontsize=14, color="black")
plt.text(0.0018,s_pro+3,r"$4.45$", fontsize=14, color="black")
plt.text(0.0018,(z1/z2)*n+2,r"$38.26$", fontsize=14, color="black")
plt.text(0.37,130,'a', fontsize=14, color="black")
plt.axis([0,0.4, -50, n+50])
plt.tick_params(axis='both', which='major', labelsize=12)
#plt.title(r'$Umbral \ de \ percolaci\'on \ para \ la \ red \ de \ enemistad$', fontsize=20)
#plt.xlabel("Connected vertices $b$", fontsize=12)
#plt.ylabel("Mean size of component $s$", fontsize=12)
plt.plot(b,s, P, y, 'go')