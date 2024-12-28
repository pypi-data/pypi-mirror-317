#Fire Bullet V: 1.Beta
#Developed by: A.AB
# libraries in use
from functools import reduce
from operator import *
from math import *
# math operators
def plus(a, b, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, l = 0, m = 0, n = 0, o = 0):
    num = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]
    plus = sum(num)
    return plus

def minus(a, b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, l = 0, m = 0, n = 0, o = 0):
    num = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]
    subt = reduce(sub, num)
    return subt


def multi(a, b = 1, c = 1, d = 1, e = 1, f = 1, g = 1, h = 1, i = 1, j = 1, k = 1, l = 1, m = 1, n = 1, o = 1):
    num = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]
    multi = reduce(mul, num)
    return multi

def divi(a, b = 1, c = 1, d = 1, e = 1, f = 1, g = 1, h = 1, i = 1, j = 1, k = 1, l = 1, m = 1, n = 1, o = 1):
    num = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]
    divi = reduce(truediv, num)
    return divi

# power, squareroot, sin, cos, tan
def power(a, b):
    power = a ** b
    return power

def squrt(a):
    sr = sqrt(a)
    return a

def sino(a):
    sino = sin(a)
    return sino

def cosi(a):
    cosi = cos(a)
    return cosi

def tanj(a):
    tanj = tan(a)
    return tanj

def cota(a):
    cota = 1 / tan(a)
    return cota

#perimeter, area and volume

#Perimeter of Shapes
def squ_per(a):
    #square perimeter
    p = a * 4
    return p

def rec_per(a, b):
    #rectangle perimeter
    p = (a + b) *2
    return p

def tri_per(a, b, c):
    #triangle perimeter
    p = a + b + c
    return p

def cir_per(r):
    #circle perimeter
    p = 2 * r * 3.14
    return p

def tra_per(a, b, c, d):
    #Trapezoid perimeter
    p = a + b + c + d
    return p

def rpen_per(a):
    #Regular Pentaagon
    p = a * 5
    return p

def ipen_per(a, b, c, d, e):
    #Irregular Pentagon
    p = a + b + c + d + e
    return p
#Perimeter of Other Shapes

def more_per(side,a="For regular shapes you need to ", b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0, i = 0, j = 0, k = 0, l = 0, m = 0, n = 0, o = 0, q = 0, r = 0, s = 0, t = 0, u = 0):
    #More Perimeter for Other shapes
    num = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, q, r, s, t, u]
    # y = input('is it a regular shape or irregular shape? ')
    if 0 < a:
        if sum(num[1 : 20]) <= 0:
            p = a * side
            return p
        elif not sum(num[1 : 20]) <= 0:
            p = sum(num)
            return p
       
#Area of Shapes

def squ_ar(a):
    #square area
    ar = a ** 2
    return ar

def rec_ar(a, b):
    #rectangle area
    ar = a * b
    return ar

def cir_ar(r):
    #circle area
    ar = 3.14 * (r ** 2)
    return ar

def tra_ar(a, b, h):
    #Trapezoid area
    ar = (a + b) * h * 0.5
    return ar

def tris_ar(a, b):
    #Triangles Area
    ar = a * b / 2
    return ar

# def pen_ar(a, b, c, d, e,):

# prisms volume
def cube_vol(a):
    #Cube volume
    v = a ** 3
    return v

def recube_vol(a, b, c):
    #Rectangular cube volume
    v = a * b * c
    return v

def cyl_vol(a, b, r):
    #Cylinder volume
    r_a = a * b
    c_a = 3.14 * (r ** 2)
    v = r_a * c_a
    return v

def triprism_vol(a='for triangle', b='triangle height', h='height of Shape'):
    ar = a * b / 2
    v = ar * h
    return v

def cone_vol(r, h):
    ar = 3.14 * (r ** 2)
    h /= 3
    v = ar * h
    return v

def tripyr_vol(a='base of triangle', b='the height of base', h='height of triangular pyramid'):
    ar = a * b / 2
    h /= 3
    v = ar * h
    return v

def squpyr_vol(a='side of square', h='height of whole shape'):
    ar = a ** 2
    h /= 3
    v = ar * h
    return v


def square(number):
    for i in range(number):
        s = i*i
        if s==number:
            return i
        