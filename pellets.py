import pygame
from vectors import Vector2D
from constants import *
from numpy import loadtxt

class Pellet(object):
    def __init__(self, x, y):
        self.name = "pellet"
        self.position = Vector2D(x, y)
        self.color = YELLOW
        self.radius = 4
        self.value = 10
        #self.visible = True

    def render(self, screen):
        #if self.visible:
        px = int(self.position.x)
        py = int(self.position.y)
        pygame.draw.circle(screen, self.color, (px, py), self.radius)


class PowerPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self, x, y)
        self.name = "powerpellet"
        self.radius = 8
        self.value = 50
        

class PelletGroup(object):
    def __init__(self, levelFile):
        self.pelletList = []
        self.createPelletList(levelFile)
        
    def createPelletList(self, levelFile):
        grid = loadtxt(levelFile, dtype=str)
        rows, cols = grid.shape
        for row in range(rows):
            for col in range(cols):
                if (grid[row][col] == "p" or 
                    grid[row][col] == "n"):
                    self.pelletList.append(Pellet(col*WIDTH, row*HEIGHT))
                if (grid[row][col] == "P" or
                    grid[row][col] == "N"):
                    self.pelletList.append(PowerPellet(col*WIDTH, row*HEIGHT))
                    
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
