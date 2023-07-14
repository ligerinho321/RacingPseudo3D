import pygame,sys,math
from settings import *
from road import Road
from camera import Camera
from player import Player
from gauger import Gauge

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Racing-Pseudo3D')
clock = pygame.time.Clock()
camera = Camera()
player = Player()
gauge = Gauge()
road = Road()
road.create()

while True:
    clock.tick(fps)
    screen.fill((26, 198, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    road.render(camera,player,screen)
    player.render(camera,road,screen)
    gauge.draw(screen,player.speedPercent)
    road.update(camera,player)
    player.update(camera,road,road.carros)


    pygame.display.flip()
    