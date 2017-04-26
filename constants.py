from vectors import Vector2D

WIDTH = 16
HEIGHT = 16
NROWS = 36
NCOLS = 28
SCREENSIZE = (NCOLS*WIDTH, NROWS*HEIGHT)

UP = Vector2D(0, -1)
DOWN = Vector2D(0, 1)
LEFT = Vector2D(-1, 0)
RIGHT = Vector2D(1, 0)
STOP = Vector2D()

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MAZEDATA = {"maze1.txt":{"portal":{(0, 17*HEIGHT):(27*WIDTH, 17*HEIGHT)},
                         "linkNodes":{0:(12*WIDTH, 14*HEIGHT), 1:(15*WIDTH, 14*HEIGHT)}
                     }
        }
