import pygame
from entities import MazeMouse
from constants import *
from vectors import Vector2D
from random import randint
from stacks import Stack

class Mode(object):
    def __init__(self, name="", time=None, speedMult=1):
        self.name = name
        self.time = time
        self.speedMult = speedMult

    
class Ghost(MazeMouse):
    def __init__(self, nodes):
        MazeMouse.__init__(self, nodes)
        self.name = "ghost"
        self.goal = Vector2D()
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0

    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]

    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            self.portal()
            validDirections = self.getValidDirections()
            self.direction = self.getClosestDirection(validDirections)
            #self.direction = self.randomDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if not key == self.direction * -1:
                    validDirections.append(key)

        if len(validDirections) == 0:
            validDirections.append(self.forceBacktrack())

        return validDirections
        
    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT
    
    def getClosestDirection(self, validDirections):
        '''Return the direction that gets ghost closer to goal'''
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction*WIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]
        
    def setupModeStack(self):
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", time=5))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        return modes

    def setScatterGoal(self):
        self.goal = Vector2D()

    def setChaseGoal(self, pacman):
        self.goal = pacman.position

    def modeUpdate(self, dt):
        self.modeTimer += dt
        if self.mode.time is not None:
            if self.modeTimer >= self.mode.time:
                self.mode = self.modeStack.pop()
                self.modeTimer = 0

    def update(self, dt, pacman):
        speedMod = self.speed * self.mode.speedMult
        self.position += self.direction * speedMod * dt
        self.modeUpdate(dt)
        if self.mode.name == "CHASE":
            self.setChaseGoal(pacman)
        elif self.mode.name == "SCATTER":
            self.setScatterGoal()
        self.moveBySelf()
