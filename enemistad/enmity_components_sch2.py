# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 11:39:17 2014

@author: elias
"""

import numpy as np
import networkx as nx
import math as ma
import matplotlib.pyplot as plt 

"""Cargar la matriz de encuestas de la Escuela 1"""
a=np.loadtxt('esc2.txt',dtype=float)

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

####Análisis probabilśtico 
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


"""Se genera el grafo de la red """
A=np.matrix(a)
G=nx.from_numpy_matrix(A)
print 'Enmity network measurements',':','School 2'

#Se calculan las componentes
l=nx.connected_components(G)
print '-Número de componentes: ', nx.number_connected_components(G)
if nx.number_connected_components(G)!=1:
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
    s_pro=ini/nx.number_connected_components(G)
    print 'Tamaño de la comunidad mayor:', np.ma.max(tam)
    print 'Tamaño relativo del cluster máximo:', Phi
    print 'Tamaño promedio de componente: ', s_pro
else:
    Phi=0
    print '-La red sólo tiene una componente'

#Intersección
bc= l1/l2   
    
a=1-bc*z1
b=-(n+bc)
c=n*bc
x_1=-b/(2*a)+ma.sqrt(b**2-4*a*c)/(2*a)
x_2=-b/(2*a)-ma.sqrt(b**2-4*a*c)/(2*a)

print 'Order:',G.order()
print 'Size:',G.size()
print 'Paths length 1:',l1,',','z1:',z1
print 'Paths length 2:',l2,',','z2:',z2
print 'Percolation threshold bc:',z1/z2
print 'Density:',nx.density(G)
print 'Clustering:',nx.average_clustering(G)
print 'Assortativity', nx.degree_assortativity_coefficient(G)
print 'b con s=%f: %f' %(s_pro, x_2 )
print
print 'z1 análisis probabilístico:', z1p
print 'z2 análisis probabilístico:', z2p

H0=nx.connected_component_subgraphs(G)[0]
graphs=list(nx.connected_component_subgraphs(G))
U3=nx.disjoint_union_all(graphs[1:3])
U2=nx.disjoint_union_all(graphs[3:9])
U1=nx.disjoint_union_all(graphs[9:45])
U=nx.disjoint_union_all(graphs[1:9])


plt.figure(1)
plt.subplot(1,2,1)
nx.draw(H0)

plt.subplot(2,2,2)
nx.draw_random(U)

plt.subplot(2,2,4)
nx.draw_random(U1)

plt.figure(2)
nx.draw(G)
plt.show()