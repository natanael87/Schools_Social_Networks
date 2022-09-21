# -*- coding: utf-8 -*-
"""
Created on Wed May 28 00:03:55 2014

@author: elias
"""

from cmath import *
from numpy import *

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
    k = complex(k)
    # Reflection formula
    if k.real < 0.5:
        return 1/gamma(k)
    else:
        k -= 1
        x = p[0]
        for i in range(1, g+2):
            x += p[i]/(k+i)
        t = k + g + 0.5
        return t**(-k-0.5) * exp(t)/(sqrt(2*pi)  * x)

#Constantes:
z=9.31481481481

#Función a integrar (Numerador)
def f(k):
    return k*(k-1)*z**k*i_gamma(k+1)    

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
int0100=simp(1.,100.,10000)*exp(-z)
#int141=simp(100.,148.,10000)*exp(-z)
#print i_gamma(148)

z2=exp(-z)*int01.real+int0100.real
#z2_1=exp(-z)*int01.real+int0100.real
print 'z2:',z2

#Función a integrar: (Denominador)
def pro(k):
    return k*z**k*i_gamma(k+1)

#Integración por método de Simpsom
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
z1=(int_pro.real)*exp(-z)
print z1

bc=z2/z1
print bc