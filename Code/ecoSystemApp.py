# !/usr/bin/python 
# -*- coding: iso-8859-15 -*- 
"""
Created on Thu Oct 10 10:27:41 2013

@author: Administrador
"""

from pygameApp import PygameApp
from world import World
from params import *
from menu import Menu
from pygame.locals import *
from animal import Bear, Cow, Wolf, Rabbit
from vector2D import Vector2D

class EcoSystemApp(PygameApp):
    def setup(self):
        self.world = World(self.screen)
        dim = (GRAPHICS_W-20,80)
        self.screenLegend = pygame.Surface(dim)
        self.screenLegend.set_alpha(200)
        pygame.draw.rect(self.screenLegend, (255,255,255), ((0, 0, dim[0],dim[1])))
        writeText("Press Enter to return to Menu", (20,5), 15, (0,0,0), self.screenLegend)
        writeText("Add", (20,45), 10, (0,0,0), self.screenLegend)
        writeText("Remove", (20,60), 10, (0,0,0), self.screenLegend)
        writeText("Rabbit", (80,30), 10, (0,0,0), self.screenLegend)
        writeText("r", (80+10,45), 10, (0,0,0), self.screenLegend)
        writeText("x + r", (80+1,60), 10, (0,0,0), self.screenLegend)
        writeText("Cow", (135,30), 10, (0,0,0), self.screenLegend)
        writeText("x + c", (135-2,60), 10, (0,0,0), self.screenLegend)
        writeText("c", (135+7,45), 10, (0,0,0), self.screenLegend)
        writeText("Wolf", (175,30), 10, (0,0,0), self.screenLegend)
        writeText("w", (175+8,45), 10, (0,0,0), self.screenLegend)
        writeText("x + w", (175,60), 10, (0,0,0), self.screenLegend)
        writeText("Bear", (215,30), 10, (0,0,0), self.screenLegend)
        writeText("b", (215+10,45), 10, (0,0,0), self.screenLegend)
        writeText("x + b", (215+3,60), 10, (0,0,0), self.screenLegend)
    def draw(self):
        self.screen.fill(EMPTY_COLOR)
        self.world.update(self)
        self.world.display()
        self.screen.blit(self.screenLegend, (self.world.screenCA_w+10,self.height-85))
    def onKeyUp(self,key,mod):
        pass 
    def onKeyDown(self,unicode,key,mod):    
        Keys = pygame.key.get_pressed()        
        if Keys[K_RETURN] or Keys[K_KP_ENTER] or Keys[K_ESCAPE]:
            self.running = False
        if Keys[K_b] and Keys[K_x]:
            print "Remove Bear"
            self.world.remove_race("bear")
        elif Keys[K_r] and Keys[K_x]:
            print "Remove Rabbit"
            self.world.remove_race("rabbit")
        elif Keys[K_w] and Keys[K_x]:
            print "Remove Wolf"
            self.world.remove_race("wolf")
        elif Keys[K_c] and Keys[K_x]:
            print "Remove Cow"
            self.world.remove_race("cow")
        elif Keys[K_b]:
            (x,y) = pygame.mouse.get_pos()
            x=min(x, self.width-GRAPHICS_W)
            a = Bear(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(a)
        elif Keys[K_r]:
            (x,y) = pygame.mouse.get_pos()
            x=min(x, self.width-GRAPHICS_W)
            a = Rabbit(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(a)
        elif Keys[K_w]:
            (x,y) = pygame.mouse.get_pos()
            x=min(x, self.width-GRAPHICS_W)
            a = Wolf(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(a)
        elif Keys[K_c]:
            (x,y) = pygame.mouse.get_pos()
            x=min(x, self.width-GRAPHICS_W)
            a = Cow(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(a)
    def onMouseMotion(self,pos,rel,buttons):
        pass       
    def onMouseButtonDown(self,pos,button):
        pass


while True:
    menu = Menu(1100,600,'Prey & Predators')
    menu.run()
    ecoSystem = EcoSystemApp(1100,600,'Prey & Predators')
    ecoSystem.setup()
    ecoSystem.run()