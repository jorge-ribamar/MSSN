# !/usr/bin/python 
# -*- coding: iso-8859-15 -*- 
"""
Created on Sun Dec 29 12:20:25 2013

@author: Administrador
"""

from cellularAutomata import CellularAutomata
from vector2D import Vector2D
from random import randint
from numpy import array, hstack
from animal import *
from params import *
from graphic import Graphic, GraphicManager

class World:
    def __init__(self,screen):
        self.terrain = CellularAutomata(GRID_SIZE,screen)
        self.w,self.h = screen.get_size()
        self.screenCA_w = self.w-GRAPHICS_W
        self.terrain.addEatenState()
        for f in IMAGE_FILES:
            self.terrain.addState(f)
        self.terrain.setRandomStates()
        changing = True
        while changing:
            changing = self.terrain.majorityRule()
        self.animals = {}
        self.id = 0
              
        for n in range(int(ANIMALS_IMAGE_FILES['cow'])):
            p = Cow(screen,Vector2D(randint(10,self.screenCA_w),randint(10,self.h-1)),self)
            p.id = self.id
            self.animals[self.id] = p
            self.id += 1
        countAnimals["cow"]=int(ANIMALS_IMAGE_FILES['cow'])

        for n in range(int(ANIMALS_IMAGE_FILES['rabbit'])):
             p = Rabbit(screen,Vector2D(randint(10,self.screenCA_w),randint(10,self.h-1)),self)
             p.id = self.id
             self.animals[self.id] = p
             self.id += 1
        countAnimals["rabbit"]=int(ANIMALS_IMAGE_FILES['rabbit'])
        for n in range(int(ANIMALS_IMAGE_FILES['wolf'])):
             p = Wolf(screen,Vector2D(randint(10,self.screenCA_w),randint(10,self.h-1)),self)
             p.id = self.id
             self.animals[self.id] = p
             self.id += 1
        countAnimals["wolf"]=int(ANIMALS_IMAGE_FILES['wolf'])
        for n in range(int(ANIMALS_IMAGE_FILES['bear'])):
            p = Bear(screen,Vector2D(randint(10,self.screenCA_w),randint(10,self.h-1)),self)
            p.id = self.id
            self.animals[self.id] = p
            self.id += 1
        countAnimals["bear"]=int(ANIMALS_IMAGE_FILES['bear'])
        
        self.graphManager = GraphicManager(screen, (self.screenCA_w+10,0+10), GRAPHICS_W-20, self.h-100, 100, 5)
        self.graphManager.addGraphic((self.screenCA_w+10,0+10), GRAPHICS_W-20, self.h-112, (0,0,255), 'População total', len(self.animals))    
        self.graphManager.addLine(countAnimals["rabbit"],1,(255,0,0))
        self.graphManager.addLine(countAnimals["cow"],1,(75,75,0))
        self.graphManager.addLine(countAnimals["wolf"],1,(255,75,0))
        self.graphManager.addLine(countAnimals["bear"],1,(0,255,0))
        self.graphManager.setLegend(1 , (self.screenCA_w-70 , 10), (60,95), ("Total","Rabbit", "Cow","Wolf","Bear"))
        #self.graphManager.setLegend(1 , (self.screenCA_w-70 , 10), (60,95), ("Total","Rabbit"))
        
    def add_animal(self,animal):
        animal.id = self.id
        self.animals[self.id] = animal
        self.id += 1
        countAnimals[animal.race]+=1
##        self.addGraphPoint(1)
    def remove_animal(self,animal):
        try:        
            del self.animals[animal.id]
            countAnimals[animal.race]-=1
        except KeyError:
            pass
##        self.addGraphPoint(1)
        
    def remove_race(self, race):
        for a in self.animals.values():
            if a.race == race:
                self.remove_animal(a)
        
    def update(self,app):
        dt = app.time_passed/1000.
        for p in self.animals.values():
            p.update(dt,self.terrain)
        self.terrain.regenerate(dt)
        self.addGraphPoint(1)
    def display(self):
        self.terrain.display()
        for p in self.animals.values():
            p.display()
        self.graphManager.draw()
        
    def addGraphPoint(self, graph):
        self.graphManager.addPoint(array([hstack([array([len(self.animals)]),array([countAnimals["rabbit"],countAnimals["cow"],countAnimals["wolf"],countAnimals["bear"]])])]))