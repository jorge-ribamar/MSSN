# !/usr/bin/python 
# -*- coding: iso-8859-15 -*- 
"""
Created on Thu Oct 10 10:44:12 2013

@author: Administrador
"""

import pygame, sys
from pygame.locals import *

class PygameApp():
    def __init__(self,width=640,height=480,name='Test'):
        pygame.init()
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.fps = 50
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption(name)
        self.setup()
        self.running = True
        
    def setup(self):
        pass
    def draw(self):
        pass
    def onKeyUp(self,key,mod):
        pass
    def onKeyDown(self,unicode,key,mod):
        pass   
    def onMouseButtonUp(self,pos,button):
        pass
    def onMouseButtonDown(self,pos,button):
        pass
    def onMouseMotion(self,pos,rel,buttons):
        pass
    def close(self):
        pass

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    self.onKeyUp(event.key,event.mod)
                if event.type == KEYDOWN:
                    self.onKeyDown(event.unicode,event.key,event.mod)
                if event.type == MOUSEBUTTONUP:
                    self.onMouseButtonUp(event.pos,event.button)
                if event.type == MOUSEBUTTONDOWN:
                    self.onMouseButtonDown(event.pos,event.button)
                if event.type == MOUSEMOTION:
                    self.onMouseMotion(event.pos,event.rel,event.buttons)
            
            self.time_passed = self.clock.tick(self.fps)
            self.draw()
            pygame.display.update()
        self.close()

if __name__ == "__main__" :
    PygameApp().run()