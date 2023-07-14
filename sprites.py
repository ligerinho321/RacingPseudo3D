import pygame

class Sprites:
    def __init__(self):
        self.image = None
        self.scaleX = 1
        self.scaleY = 1
        self.offsetX = 0
        self.offsetY = 0
        self.rect = None
    def get_width(self):
        return self.image.get_size()[0]
    def get_height(self):
        return self.image.get_size()[1]