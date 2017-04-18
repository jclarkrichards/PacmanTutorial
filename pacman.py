import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *

class Pacman(object):
    def __init__(self):
        self.name = "pacman"
        self.position = Vector2D(200,400)
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        
    def update(self, dt):
        self.position += self.direction*self.speed*dt
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.direction = STOP

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        elif key_pressed[K_DOWN]:
            return DOWN
        elif key_pressed[K_LEFT]:
            return LEFT
        elif key_pressed[K_RIGHT]:
            return RIGHT
        else:
            return None
        
    def moveByKey(self, direction):
        self.direction = direction

    def render(self, screen):
        px = int(self.position.x)
        py = int(self.position.y)
        pygame.draw.circle(screen, self.color, (px, py), self.radius)
