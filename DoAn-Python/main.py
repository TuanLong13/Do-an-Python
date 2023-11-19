from collections import deque
import sys
import pygame as pg
from pygame import gfxdraw
from pygame.locals import QUIT
from const import *
from Game import *

game = Game()
game.createBoard()
while True:
    if not game.started:
        game.startScreen()
    else:
        game.clock.tick(FPS)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()    
            if event.type == pg.MOUSEBUTTONDOWN:
                game.capture()
        game.showBoard()
        if game.checkWin() == 1:
            game.winScreen("Player 1 win", RED)
        if game.checkWin() == 2:
            game.winScreen("Player 2 win", BLUE)

    pg.display.flip()
