import pygame
from vectors import Vector2D
from constants import *
from stacks import Stack
from numpy import loadtxt

class Node(object):
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2D(column*WIDTH, row*HEIGHT)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}
        self.portalNode = None

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                pygame.draw.line(screen, WHITE, self.position.toTuple(),
                                 self.neighbors[n].position.toTuple(), 4)
        pygame.draw.circle(screen, RED, self.position.toTuple(), 12)


class NodeGroup(object):
    def __init__(self, mazeFile):
        self.mazeFile = mazeFile
        self.nodeList = []
        self.grid = None
        self.nodeStack = Stack()
        self.createNodeList()

    def createNodeList(self):
        self.grid = loadtxt(self.mazeFile, dtype=str)
        startNode = self.findFirstNode(*self.grid.shape)
        self.nodeStack.push(startNode)
        
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.addNode(node)
            leftNode = self.getPathNode(LEFT, node.row, node.column-1)
            downNode = self.getPathNode(DOWN, node.row+1, node.column)
            rightNode = self.getPathNode(RIGHT, node.row, node.column+1)
            upNode = self.getPathNode(UP, node.row-1, node.column)
            node.neighbors[LEFT] = leftNode
            node.neighbors[RIGHT] = rightNode
            node.neighbors[UP] = upNode
            node.neighbors[DOWN] = downNode
            self.addNodeToStack(leftNode)
            self.addNodeToStack(rightNode)
            self.addNodeToStack(upNode)
            self.addNodeToStack(downNode)
        self.setupPortalNodes()

    def getNode(self, x, y):
        for node in self.nodeList:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    def getNodeFromNode(self, node):
        if node is not None:
            for inode in self.nodeList:
                if node.row == inode.row and node.column == inode.column:
                    return inode
        return node

    def getPathNode(self, direction, row, col):
        tempNode = self.followPath(direction, row, col)
        return self.getNodeFromNode(tempNode)

    def findFirstNode(self, rows, cols):
        nodeFound = False
        for row in range(rows):
            for col in range(cols):
                if (self.grid[row][col] == "+" or
                    self.grid[row][col] == "n" or
                    self.grid[row][col] == "N"):
                    return Node(row, col)
        return None

    def addNode(self, node):
        nodeInList = self.nodeInList(node)
        if not nodeInList:
            self.nodeList.append(node)

    def addNodeToStack(self, node):
        if node is not None and not self.nodeInList(node):
            self.nodeStack.push(node)

    def nodeInList(self, node):
        for inode in self.nodeList:
            if node.position.x == inode.position.x and node.position.y == inode.position.y:
                return True
        return False

    def followPath(self, direction, row, col):
        if direction == LEFT and col >= 0:
            return self.pathToFollow(LEFT, row, col, "-")
        elif direction == RIGHT and col < self.grid.shape[1]:
            return self.pathToFollow(RIGHT, row, col, "-")
        elif direction == UP and row >= 0:
            return self.pathToFollow(UP, row, col, "|")
        elif direction == DOWN and row < self.grid.shape[0]:
            return self.pathToFollow(DOWN, row, col, "|")
        else:
            return None

    def pathToFollow(self, direction, row, col, path):
        if (self.grid[row][col] == path or 
            self.grid[row][col] == "+" or
            self.grid[row][col] == "p" or
            self.grid[row][col] == "P"):
            while (self.grid[row][col] != "+" and
                   self.grid[row][col] != "n" and
                   self.grid[row][col] != "N"):
                #print str(row)+", "+str(col)
                if direction is LEFT: col -= 1
                elif direction is RIGHT: col += 1
                elif direction is UP: row -= 1
                elif direction is DOWN: row += 1
            #print "New node at "+str(row)+", "+str(col)
            return Node(row, col)
        else:
            return None

    def setupPortalNodes(self):
        for pos1 in MAZEDATA[self.mazeFile]["portal"].keys():
            #print pos1
            node1 = self.getNode(*pos1)
            node2 = self.getNode(*MAZEDATA[self.mazeFile]["portal"][pos1])
            node1.portalNode = node2
            node2.portalNode = node1
    
    def setupTestNodes(self):
        nodeA = Node(5, 5)
        nodeB = Node(5, 10)
        nodeC = Node(10, 5)
        nodeD = Node(10, 10)
        nodeE = Node(10, 13)
        nodeF = Node(20, 5)
        nodeG = Node(20, 13)
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
