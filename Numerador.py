# -*- coding: utf-8 -*-
"""
Created on Tue May 27 23:55:15 2014

@author: elias
"""

from cmath import *

#Función Gamma:
# Coefficients used by the GNU Scientific Library
g = 7
p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
     771.32342877765313, -176.61502916214059, 12.507343278686905,
     -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]

def gamma(z):
    z = complex(z)
    # Reflection formula
    if z.real < 0.5:
        return pi / (sin(pi*z) * gamma(1-z))
    else:
        z -= 1
        x = p[0]
        for i in range(1, g+2):
            x += p[i]/(z+i)
        t = z + g + 0.5
        return sqrt(2*pi) * t**(z+0.5) * exp(-t) * x
#Constantes:
z=9.31481481481

#Función a integrar
def f(k):
    return k*(k-1)*z**k/gamma(k+1)        

#Mi test
#for i in range(1,11):
 #   k=i/10.0
  #  print k,f(k)
    
#for i in range(300,400):
 #   k=i/10.0
  #  print k,f(k)

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
int141=simp(100.,141.,10000)*exp(-z)
print int141

z2=exp(-z)*int01+int0100
z2_1=exp(-z)*int01+int0100+int141
print z2,z2_1
