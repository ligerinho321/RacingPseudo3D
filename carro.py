from utils import drawSprite
from sprites import Sprites
import pygame

class Carro:
    def __init__(self):
        self.sprite = Sprites()
        self.z = 0
        self.offset = 0
        self.speed = 0
        self.max_speed = 200
        self.aceel = 1
    
    def update(self):
        self.z += self.speed
        self.speed = (self.speed + self.aceel) if (self.speed < self.max_speed) else self.max_speed