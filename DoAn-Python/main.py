import sys
import pygame as pg
from pygame.locals import QUIT
from const import *
from Game import *

game = Game()
pause = TextButton(game.screen, "||", (W/12, H/15), 40, WHITE)
while True:
    if not game.started:
        game.startScreen()
    else:
        game.playScreen()
        
    pg.display.flip()
