# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 20:56:57 2013

@author: Administrador
"""
from math import sqrt,atan2

class Vector2D:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def __neg__(self):
        v = Vector2D(-self.x,-self.y)
        return v
    def add(self,v):
        self.x += v.x
        self.y += v.y
    def sub(self,v):
        self.x -= v.x
        self.y -= v.y
    def mul(self,a):
        self.x *= a
        self.y *= a
    def mag(self):
        return sqrt(self.x**2+self.y**2)
    def normalize(self):
        mod = self.mag()
        self.mul(1./mod)
    def heading(self):
        return atan2(self.y,self.x)
    def copy(self):
        return Vector2D(self.x,self.y)
    def limit(self,maxVal):
        if self.mag() > maxVal:
            self.normalize()
            self.mul(maxVal)