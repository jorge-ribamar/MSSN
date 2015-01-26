# !/usr/bin/python 
# -*- coding: iso-8859-15 -*- 
"""
Created on Sat Jan 25 12:36:21 2014

@author: Jorge
"""

import pygame
import numpy as np
from params import EMPTY_COLOR, writeText

    
def linMapping(value, ylim, graphHeight):
    return value * (graphHeight / ylim)


class GraphicManager:
    def __init__(self, screen, origin, width, height, nPontos, waitingTimes):
        self.screen = screen        
        self.origin = origin
        self.width = width
        self.height = height
        self.nPontos = nPontos
        self.waitingTimes = waitingTimes
        self.counter = 0
        self.backColor = (255,255,255)
        self.graphics = {}
        self.nGraphs = 1
        
    def addGraphic(self, origin, width, height, lineColor, title, inicialValue):
        self.graphics[self.nGraphs]=Graphic(self.screen, origin, width, height, self.nPontos, self.waitingTimes, lineColor, title, inicialValue)
        self.nGraphs+=1
        
    def addLine(self,value, graph, color):
        self.graphics[graph].addLine(value, color)    
        
    def addPoint(self,values):
        if self.counter==0:             
            for i in self.graphics:
                self.graphics[i].addPoint(values[i-1])
        self.counter =(self.counter + 1)%self.waitingTimes
    
    def addColor(self,color, graph):
        self.graphics[graph].addColor(color)
        
    def draw(self):
        pygame.draw.rect(self.screen, self.backColor, 
                         (self.origin[0], self.origin[1], self.width, self.height))
        for g in self.graphics.values():
            g.draw()
            
    def setLegend(self,graph ,pos, dim, labels):
        self.graphics[graph].setLegend(pos, dim, labels)

class Graphic:
    def  __init__(self, screen, origin, width, height, nPontos, waitingTimes, titleColor, title, inicialValue):
        self.screen = screen        
        self.origin = origin
        self.width = width
        self.height = height
        self.wText=10
        self.hTitle=20
        self.nPontos = nPontos
        self.yAxis = list()
        self.yAxis.append(np.ones(nPontos)*inicialValue)
        self.xAxis = np.arange(nPontos)*(width-self.wText)/nPontos
        self.titleColor=titleColor
        self.ylim = 20
        self.title = title
        self.nLines=1
        self.colorList = list()
        self.colorList.append(titleColor)
        self.screenLegend = None
        self.legend=False
        self.legendPos = None
      
    def addPoint(self,value):
        for i in range(self.nLines):
            self.yAxis[i] = np.roll(self.yAxis[i], -1)
            self.yAxis[i][-1] = value[i]
        self.scaleAdjust()
        
    def addColor(self,color):
        self.colorList.append(color)
        
    def addLine(self,value, color):
        self.nLines+=1        
        self.yAxis.append(np.ones(self.nPontos)*value)
        self.addColor(color)
    
    def scaleAdjust(self):
        self.ylim = np.amax(self.yAxis)
        if self.ylim <=10:
            self.ylim=10
    
    def setLegend(self, pos, dim, labels):
        self.legend=True
        self.legendPos = pos
        self.screenLegend = pygame.Surface(dim)
        self.screenLegend.set_colorkey((0,0,0))
        self.screenLegend.set_alpha(200)
        pygame.draw.rect(self.screenLegend, (255,255,255), ((0, 0, dim[0],dim[1])))
        yPos = 10        
        for i in range(self.nLines):
            pygame.draw.circle(self.screenLegend, self.colorList[i], (10, yPos+8), 2,0)
            writeText(labels[i], (15, yPos), 10, self.colorList[i], self.screenLegend)
            yPos += 15
    
    def draw(self):
        if self.legend==True:
            self.screen.blit(self.screenLegend, self.legendPos)
        writeText(self.title,(self.origin[0]+5,self.origin[1]), 15, self.titleColor, self.screen)
        writeText("0",(self.origin[0]+5,self.origin[1]+self.height-5), 10, self.titleColor,self.screen)
        writeText(str(int(self.ylim/2)),(self.origin[0]+5,(self.origin[1]+self.height+self.origin[1]+self.hTitle)/2), 10, self.titleColor,self.screen)
        writeText(str(int(self.ylim)),(self.origin[0]+5,self.origin[1]+self.hTitle), 10, self.titleColor,self.screen)
        for l in range (self.nLines):       
            for i in range(self.nPontos-1):       
                pygame.draw.line(self.screen, self.colorList[l], (self.origin[0]+self.wText+self.xAxis[i], self.origin[1]+self.height-linMapping(self.yAxis[l][i], self.ylim, self.height-self.hTitle)),
                                 (self.origin[0]+self.wText+self.xAxis[i+1], self.origin[1]+self.height-linMapping(self.yAxis[l][i+1], self.ylim, self.height-self.hTitle)))

if __name__ == "__main__": 

    import pygame, sys
    from pygame.locals import *
    
    pygame.init()
    screen = pygame.display.set_mode((300,600))        
    g = GraphicManager(screen, (0,0),300, 600, 20, 1)
    g.addGraphic((20,20), 260 , 400 , (0,0,255), "População Total", 20)
    g.addLine(5, 1, (0,255,0))
    g.setLegend(1 ,(20, 440), (260, 100), ("Cordenada y", "Cordenada x"))
    
    while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYUP:
#                        self.onKeyUp(event.key,event.mod)
                        pass
                    if event.type == KEYDOWN:
#                        self.onKeyDown(event.unicode,event.key,event.mod)
                        pass
                    if event.type == MOUSEBUTTONUP:
                        pass
#                        self.onMouseButtonUp(event.pos,event.button)
                    if event.type == MOUSEBUTTONDOWN:
                        g.addPoint(np.array([np.array([event.pos[1], event.pos[0]])]))
                    if event.type == MOUSEMOTION:
                        pass
#                        self.onMouseMotion(event.pos,event.rel,event.buttons)
                g.screen.fill(EMPTY_COLOR)            
                g.draw() 
                pygame.display.update()        
