# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 10:26:17 2013

@author: Administrador
"""

class Histogram:
    def __init__(self,L):
        self.d = {}
        for x in L:
            if x in self.d:
                self.d[x] += 1
            else:
                self.d[x] = 1
    def getMode(self):
        maxval = max(self.d.values())
        for k,v in self.d.items():
            if v == maxval:
                return k
