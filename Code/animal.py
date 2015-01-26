# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 09:16:15 2013

@author: Administrador
"""

import pygame
from vector2D import Vector2D
from math import degrees,pi,sin,cos
from random import uniform,choice
from cellularAutomata import *
from params import *
from numpy import arange, array

class Mover:
    def __init__(self,screen,location,velocity,mass):
        self.location = location
        self.velocity = velocity
        self.acceleration = Vector2D(0,0)
        self.mass = mass
        self.screen = screen
        self.maxSpeed = 90.
        self.maxForce = 120.
        self.boxWidth,self.boxHeight = (self.screen.get_size()[0]-GRAPHICS_W,self.screen.get_size()[1] )
    def applyForce(self,f):
        faux = f.copy()
        faux.limit(self.maxForce)
        faux.mul(1./self.mass)
        self.acceleration.add(faux)
    def move(self,dt):
        self.acceleration.mul(dt)
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.maxSpeed)
        v = self.velocity.copy()
        v.mul(dt)
        self.location.add(v)
        self.acceleration.mul(0)
    def seek(self,target):
        steeringForce = target.copy()
        steeringForce.sub(self.location)
        steeringForce.normalize()
        steeringForce.mul(self.maxSpeed)
        steeringForce.sub(self.velocity)
        steeringForce.limit(self.maxForce)
        return steeringForce
    def flee(self,target):
        f = self.seek(target)
        f.mul(-1.)
        return f
    def arriving(self,target):
        steeringForce = target.copy()
        steeringForce.sub(self.location)
        d = steeringForce.mag()
        if d < 100.:
            speed = self.maxSpeed*d/100.
        else:
            speed = self.maxSpeed
        steeringForce.normalize()
        steeringForce.mul(speed)
        steeringForce.sub(self.velocity)
        steeringForce.limit(self.maxForce)
        return steeringForce
    def pursuit(self,vehicle):
        deltaT = 0.5
        t = vehicle.location.copy()
        v = vehicle.velocity.copy()
        v.mul(deltaT)
        t.add(v)
        f = self.seek(t)
        return f
    def evade(self,vehicle):
        f = self.pursuit(vehicle)
        f.mul(-1.)
        return f
    def wandering(self):
        deltaTw = 0.5
        radius = 100.
        t = self.location.copy()
        v = self.velocity.copy()
        v.mul(deltaTw)
        t.add(v)
        theta = uniform(-pi,pi)
        r = Vector2D(radius*cos(theta),radius*sin(theta))
        t.add(r)
        f = self.seek(t)
        return f
    def stayInBox(self):
        if (self.location.x > self.boxWidth-10):
            self.velocity.x = -abs(self.velocity.x)
        elif(self.location.x < 10):
            self.velocity.x = abs(self.velocity.x)
        if (self.location.y > self.boxHeight-10):
            self.velocity.y = -abs(self.velocity.y)
        elif (self.location.y < 10):
            self.velocity.y = abs(self.velocity.y)
            
            
    def obstacleAvoidance(self, nPixels, intPixels, states):
        a = arange(0, nPixels, intPixels)
        vAux = Vector2D(self.velocity.x, self.velocity.y)
        vAux.normalize()
        xBase=vAux.x
        yBase=vAux.y
        for i in a:
            patch = self.world.terrain.getPatch(int(self.location.x+i*xBase),int(self.location.y+i*yBase))
            if patch.targetState in states:
                break
        if i < a[-1]:
            v2 = Vector2D(-vAux.y, vAux.x)
            v2.mul(0.5)
            v2.add(vAux)
            v2.normalize()
            xBase2=v2.x
            yBase2=v2.y
            patch = self.world.terrain.getPatch(int(self.location.x+i*xBase2),int(self.location.y+i*yBase2))
            if patch.targetState in states:
                vector = Vector2D(self.velocity.y, -self.velocity.x)
            else:
                vector = Vector2D(-self.velocity.y, self.velocity.x)
            vector.normalize()
            vector.mul(max((1.-(1.*i/nPixels))*self.maxForce*2, self.maxForce))
            return vector 
        else:
            return Vector2D( 0, 0)
        
    def display(self):
        pygame.draw.circle(self.screen,(255,0,0),
                           (int(self.location.x),int(self.location.y)),15)

class Animal(Mover):
    def __init__(self,screen,location,world):
        velocity = Vector2D(uniform(-10,10),uniform(-10,10))
        Mover.__init__(self,screen,location,velocity,1)
        self.id = None
        self.world = world
        self.energy = 0
        self.type = ''
        self.shape = None
        self.ungry_Limit = None
    def update(self,dt,terrain):
        self.move(dt)
        self.eat(terrain)
        self.reproduce(terrain)
        self.die()
    def move(self,dt):
        f = self.decide()
        self.applyForce(f)
        Mover.move(self,dt)
        self.stayInBox()
        self.energy -= dt 
     
    def escape(self, animalsRace):
        (col,line) = self.world.terrain.getPatchCoor(self.location.x, self.location.y)
        EscapeAnimals=() 
        n=0
        for race in animalsRace:
            print int(countAnimals[race])
            n += int(countAnimals[race])
        if n==0:
            return Vector2D(0,0)
        for (x,y) in FOOD_SEARCH_NEIGH:
            col += x
            line+=y
            if col<0 or line<0 or col>=self.world.terrain.ncols or line>=self.world.terrain.nlines:
                continue
            EscapeAnimals = set(EscapeAnimals).union(set(self.world.terrain.patches[col][line].whichAnimalsAreOn(self.world.animals.values(),animalsRace)))
        force = Vector2D(0,0)
        for animal in EscapeAnimals:
            f = self.flee(animal.location)
            force.add(f)
        return force     
     
     
    def eat(self,terrain):
        pass
    def reproduce(self,terrain):
        pass
    def die(self):
        if self.energy < 0:
            self.world.remove_animal(self)
    def display(self):
        pass
            
    
    

class Prey(Animal):
    def __init__(self,screen,location,world):
        Animal.__init__(self,screen,location,world)
        self.type = "prey"
        self.targetPatch= None
    def eat(self,terrain):
        patch = terrain.getPatch(self.location.x,self.location.y)
        energyGain = ENERGY_FROM_FOOD[patch.state]
        if energyGain > 0:
            self.energy += energyGain
            patch.countdown = TIME_TO_REGROW[patch.state]
            patch.state = 0
    def reproduce(self,terrain):
        pass
    def decide(self):
        pass
    
    def decidePrey(self, racesToEscape, statesToEat):
        if self.energy < self.ungry_Limit and self.targetPatch== None:
            (col,line) = self.world.terrain.getPatchCoor(self.location.x, self.location.y)
            for (x,y) in FOOD_SEARCH_NEIGH:
                col += x
                line+=y
                if col<0 or line<0 or col>=self.world.terrain.ncols or line>=self.world.terrain.nlines:
                    continue
                patch = self.world.terrain.patches[col][line]
                if patch.state in statesToEat and ENERGY_FROM_FOOD[patch.state]>0:
                    self.targetPatch = patch
                    break
        if self.energy < self.ungry_Limit and self.targetPatch!= None:
            f=Vector2D(0,0)
            if ENERGY_FROM_FOOD[self.targetPatch.state] ==0:
                self.targetPatch=None
            else:
                f = self.arriving(Vector2D((self.targetPatch.pxcor*self.targetPatch.w)+10,(self.targetPatch.pycor*self.targetPatch.h)+10))
        else:
            f = self.escape(racesToEscape)
            f2 = self.wandering()
            fObst = self.obstacleAvoidance(40, 10, array([6]))
            fObst.mul(10)   
            f.add(fObst)
            f.add(f2)
        return f
    
    def display(self):
        self.screen.blit(self.shape,(int(self.location.x-PREY_SIZE/2),
                                     int(self.location.y-PREY_SIZE/2)))
        if (self.energy < ENERGY_UNGRY_PREY): 
            myfont = pygame.font.SysFont("Comic Sans MS", 10)
            label = myfont.render(str(int(self.energy)), 1, (255,0,0))
            self.screen.blit(label,(int(self.location.x-PREY_SIZE/2 -2),
                                         int(self.location.y-PREY_SIZE/2 -2)))
                                         
class Rabbit(Prey):
    def __init__(self,screen,location,world):
        Prey.__init__(self,screen,location,world)
        self.race = "rabbit"
        self.shape = pygame.image.load('images/rabbit.png').convert_alpha()
        self.shape = pygame.transform.scale(self.shape,(PREY_SIZE,PREY_SIZE))
        self.energy = INITIAL_RABBIT_ENERGY
        self.ungry_Limit = ENERGY_UNGRY_RABBIT
    def reproduce(self,terrain):
        if self.energy >= ENERGY_TO_REPRODUCE_PREY:
            self.energy -= INITIAL_PREY_ENERGY
            patch = terrain.getPatch(self.location.x,self.location.y)
            pneigh = choice(patch.neighbors)
            x,y = pneigh.getCenter()
            p = Rabbit(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(p)

    def decide(self):
        return self.decidePrey(["wolf"], range(6))           
     

class Cow(Prey):
    def __init__(self,screen,location,world):
        Prey.__init__(self,screen,location,world)
        self.race = "cow"
        self.shape = pygame.image.load('images/cow.png').convert_alpha()
        self.shape = pygame.transform.scale(self.shape,(PREY_SIZE,PREY_SIZE))
        self.energy = INITIAL_COW_ENERGY
        self.ungry_Limit = ENERGY_UNGRY_COW
    def eat(self,terrain):
        patch = terrain.getPatch(self.location.x,self.location.y)
        if patch.state==2:
            energyGain = ENERGY_FROM_FOOD[patch.state]
            if energyGain > 0:
                self.energy += energyGain
                patch.countdown = TIME_TO_REGROW[patch.state]
                patch.state = 0    
    def reproduce(self,terrain):
        if self.energy >= ENERGY_TO_REPRODUCE_PREY:
            self.energy -= INITIAL_PREY_ENERGY
            patch = terrain.getPatch(self.location.x,self.location.y)
            pneigh = choice(patch.neighbors)
            x,y = pneigh.getCenter()
            p = Cow(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(p)    
    
    def decide(self):
        return self.decidePrey(["wolf"], [2])                                  

class Predator(Animal):
    def __init__(self,screen,location,world):
        Animal.__init__(self,screen,location,world)
        self.type = 'predator'
        self.shape = None
        self.targetPrey = None
    def eat(self,terrain):
        pass
    def reproduce(self,terrain):
        pass
    
    def decide(self):
        pass 

    def decidePredator(self, racesToEscape, racesToEat):
        if self.energy < self.ungry_Limit and self.targetPrey== None:
            (col,line) = self.world.terrain.getPatchCoor(self.location.x, self.location.y)
            for (x,y) in FOOD_SEARCH_NEIGH:
                col += x
                line+=y
                if col<0 or line<0 or col>=self.world.terrain.ncols or line>=self.world.terrain.nlines:
                    continue
                patch = self.world.terrain.patches[col][line]
                preys = patch.whichAnimalsAreOn(self.world.animals.values(),racesToEat)
                if any(preys):
                    self.targetPrey = preys[0].id
                    break
        if self.energy < self.ungry_Limit and self.targetPrey!= None:
            try:
                f=Vector2D(0,0)
                prey = self.world.animals[self.targetPrey]
                f = self.pursuit(prey)
            except KeyError:
                self.targetPrey=None
        else:
            f = self.escape(racesToEscape)
            f2 = self.wandering()
            fObst = self.obstacleAvoidance(40, 10, array([6]))
            fObst.mul(10)   
            f.add(fObst)
            f.add(f2)
        return f 
            
    def display(self):
        self.screen.blit(self.shape,(int(self.location.x-PREY_SIZE/2),
                                     int(self.location.y-PREY_SIZE/2)))
        if (self.energy<ENERGY_UNGRY_PREDATOR):
            myfont = pygame.font.SysFont("Comic Sans MS", 10)
            label = myfont.render(str(int(self.energy)), 1, (255,0,0))
            self.screen.blit(label,(int(self.location.x-PREY_SIZE/2 -2),
                                         int(self.location.y-PREY_SIZE/2 -2)))
                        
class Wolf(Predator):
    def __init__(self,screen,location,world):
        Predator.__init__(self,screen,location,world)
        self.race = "wolf"
        self.shape = pygame.image.load('images/wolf.png').convert_alpha()
        self.shape = pygame.transform.scale(self.shape,(PREY_SIZE,PREY_SIZE))
        self.energy = INITIAL_WOLF_ENERGY
        self.ungry_Limit = ENERGY_UNGRY_WOLF
    def reproduce(self,terrain):
        if self.energy >= ENERGY_TO_REPRODUCE_PREDATOR:
            self.energy -= INITIAL_PREDATOR_ENERGY
            patch = terrain.getPatch(self.location.x,self.location.y)
            pneigh = choice(patch.neighbors)
            x,y = pneigh.getCenter()
            p = Wolf(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(p)
    def eat(self, terrain):
        patch = terrain.getPatch(self.location.x,self.location.y)
        preys = patch.whichAnimalsAreOn(self.world.animals.values(),('cow','rabbit'))
        if len(preys) > 0:
            self.world.remove_animal(preys[0])
            self.energy += 30
            
    def decide(self):
        return self.decidePredator( ["bear"], ('cow','rabbit'))           
            
            
            
class Bear(Predator):
    def __init__(self,screen,location,world):
        Predator.__init__(self,screen,location,world)
        self.race = "bear"
        self.shape = pygame.image.load('images/bear.png').convert_alpha()
        self.shape = pygame.transform.scale(self.shape,(PREY_SIZE,PREY_SIZE))
        self.energy = INITIAL_BEAR_ENERGY
        self.ungry_Limit = ENERGY_UNGRY_BEAR
    def reproduce(self,terrain):
        if self.energy >= ENERGY_TO_REPRODUCE_PREDATOR:
            self.energy -= INITIAL_PREDATOR_ENERGY
            patch = terrain.getPatch(self.location.x,self.location.y)
            pneigh = choice(patch.neighbors)
            x,y = pneigh.getCenter()
            p = Bear(self.screen,Vector2D(x,y),self.world)
            self.world.add_animal(p)
    def eat(self, terrain):
        patch = terrain.getPatch(self.location.x,self.location.y)
        preys = patch.whichAnimalsAreOn(self.world.animals.values(),('wolf'))
        if len(preys) > 0:
            self.world.remove_animal(preys[0])
            self.energy += 30 
            
    def decide(self):
        return self.decidePredator( (''), ('wolf'))          

