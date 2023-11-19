from collections import deque
import sys
import pygame as pg
from os import path
from pygame import gfxdraw
from pygame.locals import QUIT
from const import *
from Hexagon import *   
from TextButton import *

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Hex game')
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((W, H))
        #Tạo đường dẫn đến thư mục img
        img_path = path.join(path.dirname(__file__), "img")
        #Load background
        self.background = pg.image.load(path.join(img_path, "bg1.jpg")).convert_alpha()
        #Khởi tạo toạ độ board
        self.coordinate = [[0 for i in range(TILES)] for j in range(TILES)]
        #Danh sách các ô trong board
        self.listHexagon = []
        #Danh sách các ô giáp đường viền đỏ
        self.redBorder = []
        #Danh sách các ô giáp đường viền xanh
        self.blueBorder = []
        self.PLAYER = 1
        self.started = False
        self.rect = False

    def drawRect(self, pos, height, boardSize):
        """Vẽ đường viền cho board"""
        x, y = pos
        pg.draw.polygon(self.screen, RED, [(x,y), (x, y+height), (x+height-height/boardSize, y+height/2), (x+height-height/boardSize ,y+height/2+height)])
        pg.draw.polygon(self.screen, BLUE, [(x,y), (x+height-height/boardSize, y+height/2), (x, y+height), (x+height-height/boardSize, y+height/2+height)])

    def createBoard(self):   
        """Tạo board"""
        x, y = STARTPOS
        for i in range(TILES):
            distance = 0
            for j in range(TILES):
                self.coordinate[i][j] = Hexagon(HEXRADIUS, (x, y+distance))
                distance += self.coordinate[i][j].minimalRadius * 2
                self.listHexagon.append(self.coordinate[i][j])
                if i == TILES-1:
                    self.redBorder.append(self.coordinate[i][j])
                if j == TILES-1:
                    self.blueBorder.append(self.coordinate[i][j])
            x, y = self.coordinate[i][0].findNextPoint()
    def resetBoard(self):
        """Reset trạng thái board"""
        for hexagon in self.listHexagon:
            hexagon.state = 0

    def showBoard(self):
        """Vẽ board ra màn hình"""
        x, y = STARTPOS
        self.drawRect((x-2*self.coordinate[0][0].minimalRadius, y - 4 * self.coordinate[0][0].minimalRadius), self.coordinate[0][0].minimalRadius * (TILES+2) * 2, TILES)
        for col in range(TILES):
            for row in range(TILES):
                if self.coordinate[col][row].state == 0:
                    self.coordinate[col][row].fillHexagon(self.screen, WHITE)
                    self.coordinate[col][row].render(self.screen)
                    if self.coordinate[col][row].inHexagon(pg.mouse.get_pos()):
                        if self.PLAYER == 1 :
                            self.coordinate[col][row].fillHexagon(self.screen, RED)
                            self.coordinate[col][row].render(self.screen)
                        else:
                            self.coordinate[col][row].fillHexagon(self.screen, BLUE)
                            self.coordinate[col][row].render(self.screen)
                elif self.coordinate[col][row].state == 1:
                    self.coordinate[col][row].fillHexagon(self.screen, RED)
                    self.coordinate[col][row].render(self.screen)
                else:
                    self.coordinate[col][row].fillHexagon(self.screen, BLUE)
                    self.coordinate[col][row].render(self.screen)

    def capture(self):
        """Khi người chơi click vào 1 ô trắng thì ô sẽ chuyển màu thành màu của ng chơi đó"""
        for col in range(TILES):
            for row in range(TILES):
                if self.coordinate[col][row].inHexagon(pg.mouse.get_pos())\
                    and self.coordinate[col][row].state == 0:
                        if self.PLAYER == 1:
                            self.coordinate[col][row].captured(self.PLAYER)
                            print("Red capture ("+str(col)+","+str(row)+")")
                        else:
                            self.coordinate[col][row].captured(self.PLAYER)
                            print("Blue capture ("+str(col)+","+str(row)+")")
                        self.PLAYER = 3 - self.PLAYER
    
    def DFS(self, start, finish, player):
        """Thuật toán tìm theo chiều sâu"""
        stack = deque()
        stack.append(start)
        visited = []
        while len(stack):
            current = stack.pop()
            for hexagon in finish:
                if current is hexagon:
                    return True
            visited.append(current)
            listNeighbour = current.findAllNeighbour(self.listHexagon)
            for hexagon in listNeighbour:
                if hexagon not in visited and hexagon.state == player:
                    stack.append(hexagon)
        return False
    
    def checkWin(self):
        """TÌm người chiến thắng bằng thuật toán DFS"""
        for row in range(TILES):
            if self.coordinate[0][row].state == 1:
                if self.DFS(self.coordinate[0][row], self.redBorder, 1):
                    return 1
        for col in range(TILES):
            if self.coordinate[col][0].state == 2:
                if self.DFS(self.coordinate[col][0], self.blueBorder, 2):
                    return 2
        return 0
    
    def winScreen(self, txt, color):
        """Màn hình thông báo người chiến thắng"""
        win = True
        winner = TextButton(self.screen, txt, (W/2, H/10), 100, color)
        back = TextButton(self.screen, "Quay lại", (W/8, H - H/15), 60, WHITE)
        while win:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            self.showBoard()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.click():
                        self.started = False
                        win = False
                        self.rect = False
                        self.resetBoard()
                        return True
            self.showBoard()
            winner.printText(100)
            back.render()
            pg.display.flip()
            
    def startScreen(self):
        """Màn hình bắt đầu"""
        start = True
        title = TextButton(self.screen, "HEX GAME", (W/2, H/4), 100, GOLD)
        startGame = TextButton(self.screen, "Bắt đầu chơi", (W/2, H/2), 60, BLUE)
        rule = TextButton(self.screen, "Luật chơi", (W/2, H - H/3), 60, BLUE)
        buttons = [startGame, rule]
        while start:
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if startGame.click():
                        self.started = True
                        start = False
                        self.rect = False
                        return True
                    elif rule.click():
                        self.ruleScreen()
                        return True
            title.printText(100)
            for b in buttons:
                b.render()
            pg.display.flip()

    def ruleScreen(self):
        """Màn hình luật chơi"""
        rule = True
        title = TextButton(self.screen, "Luật chơi", (W/2, 200), 60, RED)
        line1 = TextButton(self.screen, "2 người chơi thay phiên nhau chọn 1", (W/2, 300), 30, WHITE)
        line2 = TextButton(self.screen, " ô trắng trên board để chiếm đóng.", (W/2, 350), 30, WHITE)
        line3 = TextButton(self.screen, "Người chơi nào tạo được 1 đường liên kết", (W/2, 400), 30, WHITE)
        line4 = TextButton(self.screen, "2 cạnh đối diện nhau có màu đường viền", (W/2, 450), 30, WHITE)
        line5 = TextButton(self.screen, "ứng với màu của người chơi đó sẽ là người chiến thắng", (W/2, 500), 30, WHITE)
        back = TextButton(self.screen, "Quay lại", (W/8, H - H/15), 60, BLUE)
        text = [line1, line2, line3, line4, line5]
        while rule:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.click():
                        self.started = False
                        rule = False
            for t in text:
                t.printText(30)
            title.printText(60)
            back.render()
            pg.display.flip()

    def pauseScreen(self):
        """Màn hình tạm dừng"""
        pause = True
        cont = TextButton(self.screen, "Tiếp tục", (W/2, H/3), 80, GOLD)
        back = TextButton(self.screen, "Quay về", (W/2, H/2), 80, GOLD)
        buttons = [cont, back]
        while pause:
            self.shadow()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()    
                if event.type == pg.MOUSEBUTTONDOWN:
                    if cont.click():
                        self.screen.fill(WHITE)
                        self.screen.blit(self.background, (0, 0))
                        self.rect = False
                        return True
                    elif back.click():
                        self.started = False
                        pause = False
                        self.rect = False
                        self.resetBoard()
                        return False
            for b in buttons:
                b.render()
            pg.display.flip()

    def shadow(self):
        """Đổ bóng cho màn hình"""
        shadow = pg.Surface((W, H))
        shadow.set_alpha(200)
        self.screen.blit(shadow, (0, 0))
        

        

    
    