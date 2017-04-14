import pygame
from vectors import Vector2D
from constants import *

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2D(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(screen, WHITE, self.position.toTuple(),
                                 self.neighbors[n].position.toTuple(), 4)
        pygame.draw.circle(screen, RED, self.position.toTuple(), 12)


class NodeGroup(object):
    def __init__(self):
        self.nodeList = []

    def setupTestNodes(self):
        nodeA = Node(5*WIDTH, 5*HEIGHT)
        nodeB = Node(10*WIDTH, 5*HEIGHT)
        nodeC = Node(5*WIDTH, 10*HEIGHT)
        nodeD = Node(10*WIDTH, 10*HEIGHT)
        nodeE = Node(13*WIDTH, 10*HEIGHT)
        nodeF = Node(5*WIDTH, 20*HEIGHT)
        nodeG = Node(13*WIDTH, 20*HEIGHT)
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF
        self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]
        
    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)
