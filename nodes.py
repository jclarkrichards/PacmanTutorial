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
        self.homeList = []
        self.grid = None
        self.nodeStack = Stack()
        self.createMainList()

    def createMainList(self):
        self.createNodeList(self.mazeFile, self.nodeList)

        #self.grid = loadtxt(self.mazeFile, dtype=str)
        #startNode = self.findFirstNode(*self.grid.shape)
        #self.nodeStack.push(startNode)
        
        #while not self.nodeStack.isEmpty():
        #    node = self.nodeStack.pop()
        #    self.addNode(node, self.nodeList)
        #    leftNode = self.getPathNode(LEFT, node.row, node.column-1, self.nodeList)
        #    downNode = self.getPathNode(DOWN, node.row+1, node.column, self.nodeList)
        #    rightNode = self.getPathNode(RIGHT, node.row, node.column+1, self.nodeList)
        #    upNode = self.getPathNode(UP, node.row-1, node.column, self.nodeList)
        #    node.neighbors[LEFT] = leftNode
        #    node.neighbors[RIGHT] = rightNode
        #    node.neighbors[UP] = upNode
        #    node.neighbors[DOWN] = downNode
        #    self.addNodeToStack(leftNode, self.nodeList)
        #    self.addNodeToStack(rightNode, self.nodeList)
        #    self.addNodeToStack(upNode, self.nodeList)
        #    self.addNodeToStack(downNode, self.nodeList)
        self.setupPortalNodes()
        self.createHomeList("home.txt")

    def createHomeList(self, homeFile):
        self.createNodeList(homeFile, self.homeList)

        #self.grid = loadtxt(homeFile, dtype=str)
        #startNode = self.findFirstNode(*self.grid.shape)
        #self.nodeStack.push(startNode)
        #while not self.nodeStack.isEmpty():
        #    node = self.nodeStack.pop()
        #    self.addNode(node, self.homeList)
        #    leftNode = self.getPathNode(LEFT, node.row, node.column-1, self.homeList)
        #    downNode = self.getPathNode(DOWN, node.row+1, node.column, self.homeList)
        #    rightNode = self.getPathNode(RIGHT, node.row, node.column+1, self.homeList)
        #    upNode = self.getPathNode(UP, node.row-1, node.column, self.homeList)
        #    node.neighbors[LEFT] = leftNode
        #    node.neighbors[RIGHT] = rightNode
        #    node.neighbors[UP] = upNode
        #    node.neighbors[DOWN] = downNode
        #    self.addNodeToStack(leftNode, self.homeList)
        #    self.addNodeToStack(rightNode, self.homeList)
        #    self.addNodeToStack(upNode, self.homeList)
        #    self.addNodeToStack(downNode, self.homeList)
        self.moveHomeNodes()


    def createNodeList(self, textFile, nodeList):
        self.grid = loadtxt(textFile, dtype=str)
        startNode = self.findFirstNode(*self.grid.shape)
        self.nodeStack.push(startNode)
        while not self.nodeStack.isEmpty():
            node = self.nodeStack.pop()
            self.addNode(node, nodeList)
            leftNode = self.getPathNode(LEFT, node.row, node.column-1, nodeList)
            downNode = self.getPathNode(DOWN, node.row+1, node.column, nodeList)
            rightNode = self.getPathNode(RIGHT, node.row, node.column+1, nodeList)
            upNode = self.getPathNode(UP, node.row-1, node.column, nodeList)
            node.neighbors[LEFT] = leftNode
            node.neighbors[RIGHT] = rightNode
            node.neighbors[UP] = upNode
            node.neighbors[DOWN] = downNode
            self.addNodeToStack(leftNode, nodeList)
            self.addNodeToStack(rightNode, nodeList)
            self.addNodeToStack(upNode, nodeList)
            self.addNodeToStack(downNode, nodeList)

    def getNode(self, x, y, nodeList=[]):
        for node in nodeList:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    def getNodeFromNode(self, node, nodeList):
        if node is not None:
            for inode in nodeList:
                if node.row == inode.row and node.column == inode.column:
                    return inode
        return node

    def getPathNode(self, direction, row, col, nodeList):
        tempNode = self.followPath(direction, row, col)
        return self.getNodeFromNode(tempNode, nodeList)

    def findFirstNode(self, rows, cols):
        nodeFound = False
        for row in range(rows):
            for col in range(cols):
                if (self.grid[row][col] == "+" or
                    self.grid[row][col] == "n" or
                    self.grid[row][col] == "N"):
                    #print "found first node at " + str(row) + ", " + str(col)
                    return Node(row, col)
        return None

    def addNode(self, node, nodeList):
        nodeInList = self.nodeInList(node, nodeList)
        if not nodeInList:
            nodeList.append(node)

    def addNodeToStack(self, node, nodeList):
        if node is not None and not self.nodeInList(node, nodeList):
            self.nodeStack.push(node)

    def nodeInList(self, node, nodeList):
        for inode in nodeList:
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
            node1 = self.getNode(*pos1, nodeList=self.nodeList)
            node2 = self.getNode(*MAZEDATA[self.mazeFile]["portal"][pos1], nodeList=self.nodeList)
            node1.portalNode = node2
            node2.portalNode = node1

    def moveHomeNodes(self):
        '''Move the home nodes to the middle of the screen'''
        nodeA = self.getNode(*MAZEDATA[self.mazeFile]["linkNodes"][0], nodeList=self.nodeList)
        nodeB = self.getNode(*MAZEDATA[self.mazeFile]["linkNodes"][1], nodeList=self.nodeList)
        vec = (nodeA.position + nodeB.position) / 2.0
        vec = Vector2D(int(vec.x), int(vec.y))
        start = Vector2D(self.homeList[0].position.x, self.homeList[0].position.y)
        for node in self.homeList:
            node.position -= start
            node.position += vec
        nodeA.neighbors[RIGHT] = self.homeList[0]
        nodeB.neighbors[LEFT] = self.homeList[0]
        self.homeList[0].neighbors[RIGHT] = nodeB
        self.homeList[0].neighbors[LEFT] = nodeA
        
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
        for node in self.homeList:
            node.render(screen)
