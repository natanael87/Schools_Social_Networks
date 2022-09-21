# -*- coding: utf-8 -*-
"""
Created on Tue May 27 01:57:25 2014

@author: elias
"""

import math

z=9.31481481481
gamma=0.577215664901

n=10

#La constante alpha
s1=0.0
for i in xrange(1,n+1):
    s1+=1.0/i
alp=s1-gamma
print 'alpha:',alp

#función a integrar
def f(x,m):
    return x**m*(z*exp(-alp))**x
print f(0.1,10)  
#otra función
def f2(x):
    return 1/x
#método de simpsom
def simp(a,b,n):
    if n%2 != 0:
        n=n+1
    h=(b-a)/n
    sum_par=0.0
    sum_impar=0.0
    x_par=a
    for i in range(n/2):
        x_par+=2*h
        sum_par+=f(x_par,10)
    x_impar=a+h
    for i in range(n/2):
        sum_impar+=f(x_impar,10)
        x_impar+=2*h
    
    area=(h/3)*(f(a,10)+f(b,10)+4*sum_par+2*sum_impar)
    return area
print simp(0.0,1.0,15000)