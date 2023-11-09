from collections import deque
import sys
import pygame as pg
from pygame import gfxdraw
from pygame.locals import QUIT
from const import *
from Hexagon import *   

def DFS(start, finish, player):
    stack = deque()
    stack.append(start)
    visited = []
    while len(stack):
        current = stack.pop()
        for hexagon in finish:
            if current is hexagon:
                return True
        visited.append(current)
        listNeighbour = current.findAllNeighbour(listHexagon)
        for hexagon in listNeighbour:
            if hexagon not in visited and hexagon.state == player:
                stack.append(hexagon)
    return False

def checkWin():
    for row in range(TILES):
        if coordinate[0][row].state == 1:
            if DFS(coordinate[0][row], redBorder, 1):
                return 1
    for col in range(TILES):
        if coordinate[col][0].state == 2:
            if DFS(coordinate[col][0], blueBorder, 2):
                return 2
    return 0

def winScreen(txt):
    win = True
    while win:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()    
        showBoard()
        font = pg.font.SysFont('Verdana', 100)
        text = font.render(txt, False, BLACK)
        rect = text.get_rect(center = (400, 100))
        screen.blit(text, rect)
        pg.display.flip()
    
def drawRect(pos, height, boardSize):
    x, y = pos
    pg.draw.polygon(screen, RED, [(x,y), (x, y+height), (x+height-height/boardSize, y+height/2), (x+height-height/boardSize ,y+height/2+height)])
    pg.draw.polygon(screen, BLUE, [(x,y), (x+height-height/boardSize, y+height/2), (x, y+height), (x+height-height/boardSize, y+height/2+height)])
def showBoard():
    for col in range(TILES):
        for row in range(TILES):
            if coordinate[col][row].state == 0:
                coordinate[col][row].fillHexagon(screen, WHITE)
                coordinate[col][row].render(screen)
                if coordinate[col][row].inHexagon(pg.mouse.get_pos()):
                    if PLAYER == 1:
                        coordinate[col][row].fillHexagon(screen, RED)
                        coordinate[col][row].render(screen)
                    else:
                        coordinate[col][row].fillHexagon(screen, BLUE)
                        coordinate[col][row].render(screen)

pg.init()
pg.display.set_caption('Draw')
clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))
screen.fill(WHITE)
x, y = STARTPOS

listHexagon = []
redBorder = []
blueBorder = []
coordinate = [[0 for i in range(TILES)] for j in range(TILES)]
for i in range(TILES):
    distance = 0
    for j in range(TILES):
        coordinate[i][j] = Hexagon(HEXRADIUS, (x, y+distance))
        distance += coordinate[i][j].minimalRadius * 2
        listHexagon.append(coordinate[i][j])
        if i == TILES-1:
            redBorder.append(coordinate[i][j])
        if j == TILES-1:
            blueBorder.append(coordinate[i][j])
    x, y = coordinate[i][0].findNextPoint()

x, y = STARTPOS
drawRect((x-2*coordinate[0][0].minimalRadius, y - 4 * coordinate[0][0].minimalRadius), coordinate[0][0].minimalRadius * (TILES+2) * 2, TILES)

#firstHexagon = Hexagon(20, (250, 100))
#x, y = firstHexagon.position
#drawRect((x-2*firstHexagon.minimalRadius, y - 4 * firstHexagon.minimalRadius), firstHexagon.minimalRadius * (TILES+2) * 2, TILES)
#queue = []
#queue.append(firstHexagon)
#for i in range(TILES-1):
#    x, y = queue[len(queue)-1].findNextPoint()
#    queue.append( Hexagon(firstHexagon.radius, (x,y)))
#board = queue.copy()
#for hexagon in queue:
#    x, y = hexagon.position
#    distance = hexagon.minimalRadius * 2
#    for i in range(TILES-1):
#        nextHexagon = Hexagon(firstHexagon.radius, (x, y + distance))
#        distance +=  hexagon.minimalRadius * 2
#        board.append(nextHexagon)


while True:
#    hexagon.clock.tick(FPS)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()    
#    for hexagon in board:
#        if not hexagon.checkFilled:
#            hexagon.fillHexagon(screen, WHITE)
#            hexagon.render(screen)
#            if hexagon.inHexagon(pg.mouse.get_pos()):
#                hexagon.fillHexagon(screen, hexagon.getNextColor())
#                hexagon.render(screen)
    showBoard()
                
#    if pg.mouse.get_pressed()[0]:
#        for hexagon in board:
#            if hexagon.inHexagon(pg.mouse.get_pos()) and not hexagon.checkFilled:
#                hexagon.fillHexagon(screen, hexagon.getNextColor())
#                hexagon.render(screen)
#                hexagon.filled()
#            hexagon.currentPlayer = 3 - hexagon.currentPlayer
#        hexagon.filled()
    if event.type == pg.MOUSEBUTTONDOWN:
        for col in range(TILES):
            for row in range(TILES):
                if coordinate[col][row].inHexagon(pg.mouse.get_pos())\
                    and coordinate[col][row].state == 0:
                        if PLAYER == 1:
                            coordinate[col][row].fillHexagon(screen, RED)
                            coordinate[col][row].render(screen)
                            coordinate[col][row].captured(PLAYER)
                            print("Red capture ("+str(col)+","+str(row)+")")
                        else:
                            coordinate[col][row].fillHexagon(screen, BLUE)
                            coordinate[col][row].render(screen)
                            coordinate[col][row].captured(PLAYER)
                            print("Blue capture ("+str(col)+","+str(row)+")")
                        PLAYER = 3 - PLAYER

    if checkWin() == 1:
        winScreen("Player 1 win")
    if checkWin() == 2:
        winScreen("Player 2 win")

    pg.display.update()
