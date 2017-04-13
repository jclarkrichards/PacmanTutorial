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
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            self.move(UP)
        elif key_pressed[K_DOWN]:
            self.move(DOWN)
        elif key_pressed[K_LEFT]:
            self.move(LEFT)
        elif key_pressed[K_RIGHT]:
            self.move(RIGHT)
        else:
            self.move(STOP)

    def move(self, direction):
        self.direction = direction

    def render(self, screen):
        px = int(self.position.x)
        py = int(self.position.y)
        pygame.draw.circle(screen, self.color, (px, py), self.radius)
