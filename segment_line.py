from settings import *
from utils import drawSprite

class SegmentLine:
    def __init__(self):
        self.world_x = 0
        self.world_y = 0
        self.world_z = 0
        self.world_w = 0

        self.screen_x = 0
        self.screen_y = 0
        self.screen_w = 0

        self.index = 0
        self.scale = 0
        self.colors = None
        self.curva = 0
        self.clip = 0
        self.sprites = []
        self.carros = []
    
    def project(self,camera):
        self.scale = camera.distanci / (self.world_z - camera.z)

        x = self.scale * (self.world_x - camera.x)
        self.screen_x = (1 + x) * camera.midpoint.x

        y = self.scale * (self.world_y - camera.y)
        self.screen_y = (1 - y) * camera.midpoint.y

        self.screen_w = self.scale * self.world_w * screen_width
    
    def draw_sprite(self,camera,player,screen):
        for i in range(len(self.sprites)-1,-1,-1):
            sprite = self.sprites[i]
            scale = self.scale
            roadWidth = self.world_w
            destX = self.screen_x + self.screen_w * sprite.offsetX
            destY = self.screen_y
            drawSprite(sprite, camera, player, roadWidth, scale, destX, destY, self.clip,screen)
    
    def draw_carro(self,camera,player,screen):
        for i in range(len(self.carros)-1,-1,-1):
            sprite = self.carros[i].sprite
            scale = self.scale
            roadWidth = self.world_w
            destX = self.screen_x + self.screen_w * self.carros[i].offset
            destY = self.screen_y
            drawSprite(sprite, camera, player, roadWidth, scale, destX, destY, self.clip,screen)