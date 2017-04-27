import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from ghosts import Ghost
from pellets import PelletGroup

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = None
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.score = 0

    def setBackground(self):
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        
    def startGame(self):
        self.nodes = NodeGroup("maze1.txt")
        self.pellets = PelletGroup("maze1.txt")
        self.pacman = Pacman(self.nodes.nodeList)
        self.ghost = Ghost(self.nodes.nodeList)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.checkPelletDrivenEvents()
        self.checkGhostEvents()
        self.pacman.update(dt)
        self.ghost.update(dt, self.pacman)
        self.checkEvents()
        self.render()

    def checkPelletDrivenEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.score += pellet.value
            self.pellets.pelletList.remove(pellet)
            
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def checkPelletDrivenEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.score += pellet.value
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghost.setFreightMode()

    def checkGhostEvents(self):
        eaten = self.pacman.eatGhost(self.ghost)
        
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()
        

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
