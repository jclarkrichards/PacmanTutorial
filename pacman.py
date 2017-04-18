import pygame
from pygame.locals import *
from vectors import Vector2D
from constants import *

class Pacman(object):
    def __init__(self, nodes):
        self.name = "pacman"
        self.nodes = nodes
        self.node = nodes[0]
        self.target = self.node
        self.setPosition()
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW


    def setPosition(self):
        self.position = self.node.position.copy()


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
            self.moveWithKeyed(direction)
        else:
            self.moveWithoutKeyed()


    def moveWithoutKeyed(self):
        if self.direction is not STOP:
            if self.overshotTarget():
                self.node = self.target
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.setPosition()
                    self.direction = STOP

            
    def moveWithKeyed(self, direction):
        if self.direction is STOP:
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction

        else:
            if direction == self.direction * -1:
                self.reverseDirection()

            if self.overshotTarget():
                self.node = self.target
                if self.node.neighbors[direction] is not None:
                    self.target = self.node.neighbors[direction]
                    self.direction = direction
                    self.setPosition()
                else:#no neighbors in direction
                    #if self.direction is not STOP:
                    if self.node.neighbors[self.direction] is not None:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.setPosition()
                        self.direction = STOP


    def overshotTarget(self):
        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        node2Target = vec1.magnitudeSquared()
        node2Self = vec2.magnitudeSquared()
        return node2Self >= node2Target


    def reverseDirection(self):
        if self.direction is UP: self.direction = DOWN
        elif self.direction is DOWN: self.direction = UP
        elif self.direction is LEFT: self.direction = RIGHT
        elif self.direction is RIGHT: self.direction = LEFT

        temp = self.node
        self.node = self.target
        self.target = temp
        

    def setNextTarget(self, direction):
        self.target = self.node.neighbors[direction]
        self.direction = direction


    def render(self, screen):
        px = int(self.position.x)
        py = int(self.position.y)
        pygame.draw.circle(screen, self.color, (px, py), self.radius)
