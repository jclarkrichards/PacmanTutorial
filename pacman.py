import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *
from entities import MazeMouse

class Pacman(MazeMouse):
    def __init__(self, nodes):
        MazeMouse.__init__(self, nodes)
        self.name = "pacman"
        self.color = YELLOW


    def getValidKey(self):
        '''Return the direction vectors based on the key presses'''
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        elif key_pressed[K_DOWN]:
            return DOWN
        elif key_pressed[K_LEFT]:
            return LEFT
        elif key_pressed[K_RIGHT]:
            return RIGHT
        return None
        

    def update(self, dt):
        self.position += self.direction*self.speed*dt
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.moveBySelf()


    def moveByKey(self, direction):
        if self.direction is STOP:
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction

        else:
            if direction == self.direction * -1:
                self.reverseDirection()

            if self.overshotTarget():
                self.node = self.target
                self.portal()
                if self.node.neighbors[direction] is not None:
                    self.target = self.node.neighbors[direction]
                    if self.direction != direction:
                        self.direction = direction
                        self.setPosition()
                else:#no neighbors in direction
                    #if self.direction is not STOP:
                    if self.node.neighbors[self.direction] is not None:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.setPosition()
                        self.direction = STOP


