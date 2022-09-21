# -*- coding: utf-8 -*-
"""
Created on Mon May 26 19:14:50 2014

@author: elias
"""

from numpy import exp,log

z=9.31481481481
gamma=0.577215664901
maxIt=1500

n=10

#factorial
def facto(n):
    if n == 0:
        return 1.0
    else:
        return n * facto(n-1)
        
#La constante alpha
s1=0.0
for i in xrange(1,n+1):
    s1+=1.0/i
alp=s1-gamma
print 'alpha:',alp

#función Integral de 0 a 1
def int01(m):
    t = facto(m)/(alp-log(z))**(m+1)
    for i in range(m+1):
        t -= z*exp(-alp)*facto(m) / (facto(i)*(alp-log(z))**(m+1-i))
    return t 
    
print int01(10)
print
m=10
t = facto(m)/(alp-log(z))**(m+1)
print t
for i in range(m+1):
    t -= facto(m)*z*exp(-alp) / (facto(i)*(alp-log(z))**(m+1-i))
    print i,m+1-i,':',z*exp(-alp)*facto(m) / (facto(i)*(alp-log(z))**(m+1-i)),  
    print t
    
print
print -t
print facto(m)/(alp-log(z))**(m+1)

print
print exp(-alp),log(z),alp-log(z)