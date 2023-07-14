import math
from settings import *
import pygame

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 1500
        self.z = 0
        self.h = self.y
        fieldOfView = (120/180)*math.pi
        theta = fieldOfView / 2
        self.distanci = 1/math.tan(theta)
        self.midpoint = pygame.math.Vector2(screen_width/2,screen_height/2)
        self.cursor = 0
        self.maxSpeed = 600
        self.speed = 0