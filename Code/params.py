# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 15:20:48 2013

@author: Administrador
"""
from numpy import array
import pygame

GRID_SIZE = (40,20)
EMPTY_COLOR = [220,170,90]
# State 0 represents EATEN_STATE
#IMAGE_FILES = ['herb']

GRAPHICS_W = 300

IMAGE_FILES = ['','herb','mushroom','corn','cactus','roof'] #states [1,6] depois adiciona-se 'agua'


INITIAL_PREY_ENERGY = 20
ENERGY_TO_REPRODUCE_PREY = 40
ENERGY_UNGRY_PREY = 10

INITIAL_PREDATOR_ENERGY = 20
ENERGY_TO_REPRODUCE_PREDATOR = 40
ENERGY_UNGRY_PREDATOR = 10

INITIAL_WOLF_ENERGY = 20
ENERGY_TO_REPRODUCE_WOLF = 40
ENERGY_UNGRY_WOLF = 10

INITIAL_BEAR_ENERGY = 20
ENERGY_TO_REPRODUCE_BEAR = 40
ENERGY_UNGRY_BEAR = 10

INITIAL_RABBIT_ENERGY = 20
ENERGY_TO_REPRODUCE_RABBIT = 40
ENERGY_UNGRY_RABBIT = 10

INITIAL_COW_ENERGY = 20
ENERGY_TO_REPRODUCE_COW = 40
ENERGY_UNGRY_COW = 10


FOOD_SEARCH_NEIGH = array([(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,1),(1,-1),(1,1),
                           (-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2), (-1,-2),(-1,2),
                           (0,-2),(0,2),(1,-2),(1,2),(2,-2),(2,-1),(2,0),(2,1),(2,2)])



#ENERGY_FROM_FOOD = {0:0,1:3}
ENERGY_FROM_FOOD = {0:0,1:0,2:4,3:6,4:10,5:0,6:0,7:0}
#TIME_TO_REGROW = {1:10}
TIME_TO_REGROW = {2:5,3:8,4:10}

INITIAL_NUM_PREYS = 10
PREY_SIZE = 25

INITIAL_NUM_PREDATORS = 8
PREDATOR_SIZE = 25

ANIMALS_IMAGE_FILES = { 'bear':str(INITIAL_NUM_PREDATORS/2),'wolf':str(INITIAL_NUM_PREDATORS-INITIAL_NUM_PREDATORS/2), 'cow':str(INITIAL_NUM_PREYS-INITIAL_NUM_PREYS/2),'rabbit':str(INITIAL_NUM_PREYS/2)}

countAnimals = {"rabbit":'0', "wolf":'0', "bear":'0', "cow":'0', '':'0' }  

def writeText(text, pos, size, color, screen):
    myfont = pygame.font.SysFont("Comic Sans MS", size)
    label = myfont.render(text, 1, color)
    screen.blit(label, pos)