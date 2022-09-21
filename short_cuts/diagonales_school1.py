# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 15:20:57 2014

@author: elias
"""

import numpy as np
import networkx as nx
#import matplotlib.pyplot as plt

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
            
ns=18
#Análisis por comunidades
d=np.zeros((n,n))

zB=np.zeros(s)
z2B=np.zeros(s)

ent=(n-n%s)/s
resta=n
for i in range(s):
    l1c=0.0
    l2B=0.0
    resta=n-ent*(i+1)
    if resta>=ent:
        d[ent*i:ent*(i+1),ent*i:ent*(i+1)] =a[ent*i:ent*(i+1),ent*i:ent*(i+1)]
        d1=d[ent*i:ent*(i+1),ent*i:ent*(i+1)]
        l1c=d1.sum()
        zB[i]=l1c/ent
        d2=np.dot(d1,d1)
        for j in xrange(ns):
            d2[j,j]=0
            for k in xrange(ns):
                if d2[j,k]>0:
                    d2[j,k]=1
                if d1[j,k]==1:
                    d2[j,k]=0
        l2B=d2.sum()
        z2B[i]=l2B/ent
    else:
        d[ent*(s-1):n,ent*(s-1):n] = a[ent*(s-1):n,ent*(s-1):n]
        d1=d[ent*(s-1):n,ent*(s-1):n]
        l1c=d1.sum()
        zB[i]=l1c/ent
        d2=np.dot(d1,d1)
        for j in xrange(ns):
            d2[j,j]=0
            for k in xrange(ns):
                if d2[j,k]>0:
                    d2[j,k]=1
                if d1[j,k]==1:
                    d2[j,k]=0        
        l2B=d2.sum()
        z2B[i]=l2B/(n-ent*(s-1))

#Análisis de la matriz entera
ld1=d.sum()    

dcuad=np.dot(d,d)
for j in xrange(n):
    dcuad[j,j]=0
    for k in xrange(n):
        if dcuad[j,k]>0:
            dcuad[j,k]=1
        if d[j,k]==1:
            dcuad[j,k]=0
ld2=dcuad.sum()
print 
print zB
print z2B
print 'promedio de z1:', sum(zB)/s
print 'promedio de z2:', sum(z2B)/s
print
print 'z1 de la matriz entera', ld1/n
print 'z2 de la matriz entera', ld2/n