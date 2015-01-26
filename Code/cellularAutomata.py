# !/usr/bin/python 
# -*- coding: iso-8859-15 -*- 
"""
Created on Fri Nov 22 14:30:18 2013

@author: Administrador
"""

import pygame
from random import randint
from histogram import Histogram
from params import *

class CellularAutomata:
    def __init__(self,grid_size,screen):
        self.nStates = 0
        self.images = []
        self.ncols,self.nlines = grid_size
        self.screen = screen
        screen_w,screen_h = screen.get_size()
        screenCA_w = screen_w-GRAPHICS_W
        self.patch_w,self.patch_h = (screenCA_w/self.ncols,screen_h/self.nlines)
        self.patches = []
        for j in range(self.ncols):
            line = []
            for i in range(self.nlines):
                line.append(Patch((j,i),(self.patch_w,self.patch_h),self))
            self.patches.append(line)
        self.neighbors = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        for lineOfPatches in self.patches:
            for patch in lineOfPatches:
                patch.setNeighbors(self.neighbors)
    def addEatenState(self):
        surf = pygame.Surface((self.patch_w,self.patch_h))
        surf.fill(EMPTY_COLOR)
        self.images.append(surf)
        self.nStates += 1
    def addState(self,im_file):
        if im_file:
            surf = pygame.image.load('images/'+im_file+'.png').convert_alpha()
            surf = pygame.transform.scale(surf,(self.patch_w,self.patch_h))
            self.images.append(surf)
        else:
            surf = pygame.Surface((self.patch_w,self.patch_h))
            surf.fill(EMPTY_COLOR)
            self.images.append(surf)
        self.nStates += 1
    def setRandomStates(self):
        for lineOfPatches in self.patches:
            for patch in lineOfPatches:
                patch.state = randint(1,self.nStates-1)
                patch.targetState = patch.state
    def majorityRule(self):
        changed = []
        for lineOfPatches in self.patches:
            for patch in lineOfPatches:
                patch.setHistogram()
        for lineOfPatches in self.patches:
            for patch in lineOfPatches:
                changed.append(patch.update())
        return any(changed)
    def getPatch(self,x,y):
        col = int(x/self.patch_w) % self.ncols
        line = int(y/self.patch_h) % self.nlines
        return self.patches[col][line]
    def getPatchCoor (self,x,y):
        col = int(x/self.patch_w) % self.ncols
        line = int(y/self.patch_h) % self.nlines
        return (col,line)        
        
    def regenerate(self,dt):
        for lineOfPatches in self.patches:
            for patch in lineOfPatches:
                if patch.countdown > 0:
                    patch.countdown -= dt
                    if patch.countdown <= 0:
                        patch.state = patch.targetState
    def display(self):
        for lineOfPatches in self.patches:
            for patch in lineOfPatches:
                patch.display()

class Patch:
    def __init__(self,coord,size,cellularAutomata):
        self.pxcor,self.pycor = coord
        self.w,self.h = size
        self.state = 0
        self.targetState = 0
        self.countdown = 0
        self.ca = cellularAutomata
    def setNeighbors(self,neighbIndexes):
        self.neighbors = []
        nlines = self.ca.nlines
        ncols = self.ca.ncols
        for j,i in neighbIndexes:
            jj = (self.pxcor + j) % ncols
            ii = (self.pycor + i) % nlines
            self.neighbors.append(self.ca.patches[jj][ii])
    def setHistogram(self):
        ll = [p.state for p in self.neighbors]
        ll.append(self.state)
        self.hist = Histogram(ll)
    def update(self):
        mode = self.hist.getMode()
        changed = False
        if self.hist.d[self.state] < self.hist.d[mode]:
            self.state = mode
            self.targetState = mode
            changed = True
        return changed
    def getCenter(self):
        x = (self.pxcor + 0.5)*self.w
        y = (self.pycor + 0.5)*self.h
        return (x,y)
    def whichAnimalsAreOn(self,allAnimals, races):
        return [animal for animal in allAnimals 
                if (self.ca.getPatch(animal.location.x,animal.location.y) == self and animal.race in races)]

        
#    def whichPreysAreOn(self,allAnimals):
#        animalsOnPatch = [animal for animal in allAnimals 
#                if self.ca.getPatch(animal.location.x,animal.location.y) == self]
#        return [animal for animal in animalsOnPatch if animal.type == 'prey']
#    def whichPredatorsAreOn(self,allAnimals):
#        animalsOnPatch = [animal for animal in allAnimals 
#                if self.ca.getPatch(animal.location.x,animal.location.y) == self]
#        return [animal for animal in animalsOnPatch if animal.type == 'predator']   
#    def whichPreysAreOnByRace(self,allAnimals,race):
#        animalsOnPatch = [animal for animal in allAnimals 
#                if self.ca.getPatch(animal.location.x,animal.location.y) == self]
#        return [animal for animal in animalsOnPatch if (animal.type == 'prey' and animal.race==race)]
#    def whichPredatorsAreOnOnByRace(self,allAnimals,race):
#        animalsOnPatch = [animal for animal in allAnimals 
#                if self.ca.getPatch(animal.location.x,animal.location.y) == self]
#        return [animal for animal in animalsOnPatch if (animal.type == 'predator' and animal.race==race)]                  
    def display(self):
        self.ca.screen.blit(self.ca.images[self.state],(self.pxcor*self.w,self.pycor*self.h))


    