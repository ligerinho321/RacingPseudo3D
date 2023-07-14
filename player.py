from sprites import Sprites
from utils import drawSprite
from settings import *
import pygame

class Player:
    def __init__(self):
        self.reto = pygame.image.load('images/sprites/player_straight.png').convert_alpha()
        self.left = pygame.image.load('images/sprites/player_left.png').convert_alpha()
        self.right = pygame.image.load('images/sprites/player_right.png').convert_alpha()
        self.reto_up = pygame.image.load('images/sprites/player_uphill_straight.png').convert_alpha()
        self.left_up = pygame.image.load('images/sprites/player_uphill_left.png').convert_alpha()
        self.right_up = pygame.image.load('images/sprites/player_uphill_right.png').convert_alpha()

        self.sprite = Sprites()
        self.sprite.image = self.reto
        self.maxRange = 4
        self.curvePower = 0
        self.centrifugalForce = 0
        self.speed = 0
        self.maxSpeed = 400
        self.accel = 1
        self.decel = -4
        self.speedPercent = 0
        self.x = 0

        self.font = pygame.font.SysFont('Arial',10)
    
    def width(self):
        return self.sprite.get_width()
    
    def height(self):
        return self.sprite.get_height()

    def chanceXToRight(self,curvePower):
        if self.x >= self.maxRange:
            self.x = self.maxRange
        else:
            self.x += curvePower

    def changeXToLeft(self,curvePower):
        if self.x <= -self.maxRange:
            self.x = -self.maxRange
        else:
            self.x -= curvePower

    def limit(self,value,minimum,maximo):
        return max(minimum,min(value,maximo))
    
    def increase(self,start,speed,length):
        start += speed
        if start >= length:
            start -= length
        elif start < 0:
            start += length
        return int(start)
    
    def update(self,camera,road,carros):
        
        key = pygame.key.get_pressed()
        
        camera.cursor = self.increase(camera.cursor,self.speed,road.length)
        segment = road.get_segment(camera.cursor)
        self.speedPercent = self.speed/self.maxSpeed

        self.centrifugalForce = 0.06 * self.speedPercent

        if segment.curva and self.speed:
            if segment.curva < 0:
                self.chanceXToRight(self.centrifugalForce)
            elif segment.curva > 0:
                self.changeXToLeft(self.centrifugalForce)

        if key[pygame.K_w]:
            self.speed += self.accel
        elif key[pygame.K_s]:
            self.speed += self.decel
        else:
            self.speed -= 1
        
        self.speed = self.limit(self.speed,0,self.maxSpeed)

        self.curvePower = 0.07 * self.speedPercent

        if key[pygame.K_d] and self.curvePower:
            self.chanceXToRight(self.curvePower)
            self.sprite.image = self.right

        elif key[pygame.K_a] and self.curvePower:
            self.changeXToLeft(self.curvePower)
            self.sprite.image = self.left

        else:
            self.sprite.image = self.reto
        
        if abs(self.x) > 2.5 and self.speed > 200:
            self.speed -= 2

        
    
    def render(self,camera,road,screen):
        scale = 1/ camera.h
        destX = camera.midpoint.x
        destY = screen_height
        drawSprite(self.sprite,camera,self,road.width,scale,destX,destY,0,screen)