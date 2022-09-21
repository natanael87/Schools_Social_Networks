# -*- coding: utf-8 -*-
"""
Created on Mon May 26 15:19:18 2014

@author: elias
"""

from numpy import exp,log

z=9.31481481481
gamma=0.577215664901

#factorial
def facto(n):
    if n == 0:
        return 1.0
    else:
        return n * facto(n-1)

n=167
#Creo la matriz
cero=zeros((n,n))
for i in xrange(n):
    cero[i,0]=i+1
    cero[i,1]=1

#creo la columna principal
fila=matrix(cero[0,0:n]).transpose()

#creo la columna secundaria
dos=zeros((2*n-1,1))
    
#Realizo la primera multiplicación y la suma de diagonales:
#diagonal superior
for i in xrange(fila.size):
    suma=0.0
    for j in xrange(i+1):
        suma+=dot(fila,matrix(cero[1,:]))[j,i-j]
    dos[i,0]=suma
#diagonal inferior    
for i in xrange(cero[1,:].size-1):
    suma=0.0
    for j in xrange(cero[1,:].size-i-1):
        suma+=dot(fila,matrix(cero[1,:]))[j+i+1,n-1-j]
    dos[n+i,0]=suma

#Las multiplicaciones sucesivas..
for k in xrange(2,n):
    fila=matrix(cero[k,0:n])
    m=dot(matrix(dos[0:n]),fila)
    #diagonal superior
    for i in xrange(n):
        suma=0.0
        for j in xrange(i+1):
            suma+=m[j,i-j]
        dos[i,0]=suma
    #diagonal inferior    
    for i in xrange(n-1):
        suma=0.0
        for j in xrange(n-i-1):
            suma+=m[j+i+1,n-1-j]
        dos[n+i,0]=suma
    coef=(dos[0:n+3]/facto(n))
#print dos[0:n+1]
print coef
print

#Pro último la multiplicación extra:
extra=matrix([0,-1,1])
f=dot(coef,extra)
print f
#Y las sumas de las diagonales de la matriz resultante m x n
#diagonal superior
for i in xrange(extra.size):
    suma=0.0
    for j in xrange(i+1):
        suma+=f[j,i-j]
        coef[i,0]=suma
print
#diagonales intermedias
dif=n+1-extra.size
for i in xrange(dif):
    suma=0.0
    for j in xrange(extra.size):
        suma+=f[j+i+1,extra.size-1-j]
        coef[extra.size+i,0]=suma
#diagonal inferior  
dif2=extra.size-1
for i in xrange(dif2):
    suma=0.0
    for j in xrange(dif2-i):
        suma+=f[dif+j+i+1,extra.size-1-j]
        coef[n+1+i,0]=suma
print coef
print

#La constante alpha
s1=0.0
for i in xrange(1,n+1):
    s1+=1.0/i
alp=s1-gamma
print 'alpha:',alp

#creo la columna de exponenciales
#e=zeros((n+3,1))
result=0.0
for i in xrange(n+3):
    result+=exp(-z)*coef[i]*(-1)**(i+1)*facto(i)/(log(z)-alp)**(i+1)
print result