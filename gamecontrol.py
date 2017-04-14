import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = None
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        
    def startGame(self):
        self.pacman = Pacman()
        self.nodes = NodeGroup()
        self.nodes.setupTestNodes()
        
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.checkEvents()
        self.render()
        
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.render(self.screen)
        self.nodes.render(self.screen)
        pygame.display.update()
        

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
