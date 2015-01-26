# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:57:35 2014

@author: Jorge
"""

from pygameApp import PygameApp
from params import EMPTY_COLOR, ANIMALS_IMAGE_FILES, INITIAL_NUM_PREYS, INITIAL_NUM_PREDATORS, writeText
import pygame
from pygame.locals import *




class Menu(PygameApp):
    def setup(self):     
        self.selected = 'rabbit'
        self.backGround = pygame.image.load('images/menu.png')
        self.backGround = pygame.transform.scale(self.backGround,(520,520))  
    def draw(self):
        self.screen.fill(EMPTY_COLOR)
        pygame.draw.rect(self.screen, (255,255,255), (20,20, self.width-40, self.height-40 ),0)
        pygame.draw.rect(self.screen, EMPTY_COLOR, (35,35, self.width-70, self.height-70 ),0)
        self.screen.blit(self.backGround,(40,40))
        baseCoor = (int(self.width/1.8),250)
        pygame.draw.rect(self.screen, (255,255,255), (40+520+10,40, 490, 520 ),0)
        writeText("Choose the initial number of:", (baseCoor[0]-30,baseCoor[1]-75), 32, (0,0,0), self.screen)
        writeText("Press Tab to navigate", (890,500), 15, (0,0,0,), self.screen)
        writeText("Press Enter to play", (890,500+20), 15, (0,0,0,), self.screen )
        for animal in ANIMALS_IMAGE_FILES.keys():
            if animal != self.selected:
                color = (227,171,8)
            else:
                color = (57,105,233)
            name = animal.title()
            writeText(name, baseCoor, 32, color, self.screen)
            pygame.draw.rect(self.screen, color, (baseCoor[0]+110,baseCoor[1], 100, 50 ),3)  
            writeText(ANIMALS_IMAGE_FILES[animal], (baseCoor[0]+110+20,baseCoor[1]), 32, color , self.screen)
            baseCoor = (baseCoor[0],baseCoor[1]+75)
            
        
    def nextSelected(self, inverse = False):
        if inverse==True:
            if self.selected == "wolf":
                self.selected = 'rabbit'
            elif self.selected == 'cow':
                self.selected = 'wolf'
            elif self.selected == 'bear':
                self.selected = "cow"
            elif self.selected == "rabbit":
                self.selected = "bear"
        else:
            if self.selected == "rabbit":
                self.selected = 'wolf'
            elif self.selected == 'wolf':
                self.selected = 'cow'
            elif self.selected == 'cow':
                self.selected = "bear"
            elif self.selected == "bear":
                self.selected = "rabbit"
        ANIMALS_IMAGE_FILES[self.selected] = ''
    
    def onKeyDown(self,unicode,key,mod):    
        if key == K_RETURN or key == K_KP_ENTER:
            self.running = False
        elif key == K_TAB:
            self.nextSelected()
        elif (key<= K_9 and key>= K_0) or (key>= K_KP0 and key<= K_KP9):
            if (key<= K_9 and key>= K_0):
                ANIMALS_IMAGE_FILES[self.selected] += pygame.key.name(key)
            else:
                ANIMALS_IMAGE_FILES[self.selected] += pygame.key.name(key)[1:2]
            if  int(ANIMALS_IMAGE_FILES[self.selected])>20:
                ANIMALS_IMAGE_FILES[self.selected] = "20"
        elif key == K_BACKSPACE:
            ANIMALS_IMAGE_FILES[self.selected] = ANIMALS_IMAGE_FILES[self.selected][0:-1]
        elif key == K_UP:
            self.nextSelected(True)
        elif key ==K_DOWN:
            self.nextSelected()
    
    def close(self):
        for animal in ANIMALS_IMAGE_FILES.keys():
            if ANIMALS_IMAGE_FILES[animal]=='':
                ANIMALS_IMAGE_FILES[animal]='0'
       
    def onKeyUp(self,key,mod):
        pass   
    
    def onMouseMotion(self,pos,rel,buttons):
        pass       
    
    def onMouseButtonDown(self,pos,button):
        pass

if __name__ == "__main__" :    
    Menu(1100,600,'Prey & Predators').run()