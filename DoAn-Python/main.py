import sys
import pygame as pg
from pygame import gfxdraw
from pygame.locals import QUIT
from const import *
from Hexagon import *   

def drawRect(pos, height, boardSize):
    x, y = pos
    pg.draw.polygon(screen, RED, [(x,y), (x, y+height), (x+height-height/boardSize, y+height/2), (x+height-height/boardSize ,y+height/2+height)])
    pg.draw.polygon(screen, BLUE, [(x,y), (x+height-height/boardSize, y+height/2), (x, y+height), (x+height-height/boardSize, y+height/2+height)])


pg.init()
pg.display.set_caption('Draw')
screen = pg.display.set_mode((1000, 800))
screen.fill(WHITE)
firstHexagon = Hexagon(20, (250, 100))
x, y = firstHexagon.position
drawRect((x-2*firstHexagon.minimalRadius, y - 4 * firstHexagon.minimalRadius), firstHexagon.minimalRadius * (TILES+2) * 2, TILES)
queue = []
queue.append(firstHexagon)
for i in range(TILES-1):
    x, y = queue[len(queue)-1].findNextPoint()
    queue.append( Hexagon(firstHexagon.radius, (x,y)))
board = queue.copy()
for hexagon in queue:
    x, y = hexagon.position
    distance = hexagon.minimalRadius * 2
    for i in range(TILES-1):
        nextHexagon = Hexagon(firstHexagon.radius, (x, y + distance))
        distance +=  hexagon.minimalRadius * 2
        board.append(nextHexagon)


while True:

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()    
    for hexagon in board:
        if not hexagon.checkFilled:
            hexagon.fillHexagon(screen, WHITE)
            hexagon.render(screen)
            if hexagon.inHexagon(pg.mouse.get_pos()):
                hexagon.fillHexagon(screen, RED)
                hexagon.render(screen)
    if event.type == pg.MOUSEBUTTONDOWN:
        for hexagon in board:
            if hexagon.inHexagon(pg.mouse.get_pos()):
                hexagon.fillHexagon(screen, RED)
                hexagon.render(screen)
                hexagon.filled()

    pg.display.update()