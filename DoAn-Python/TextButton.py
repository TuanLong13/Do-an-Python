import pygame as pg
from const import *
class TextButton:
    def __init__(self, surface, txt, pos, size, color):
        self.surface = surface
        self.text = txt
        self.pos = pos
        self.size = size
        self.color = color
        self.originalColor = color
        self.rect = pg.Rect(20, 40, 20, 20)
    
    def render(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.color = ORANGE
            self.printText(self.size-10)
        else:
            self.color = self.originalColor
            self.printText(self.size)
    
    def click(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            return True
        return False
        
    def printText(self, size):
        """In text ra màn hình"""
        font = pg.font.SysFont('Verdana', size)
        text = font.render(self.text, False, self.color)
        self.rect = text.get_rect(center = self.pos)
        self.surface.blit(text, self.rect)     