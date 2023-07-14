import pygame

def drawSprite(sprite,camera,player,roadwidth,scale,destX,destY,clip,screen):
    midpoint = camera.midpoint
    spriteWidth = sprite.get_width()
    spriteHeight = sprite.get_height()
    offsetY = sprite.offsetY or 1
    scaleX = sprite.scaleX
    scaleY = sprite.scaleY
    fator  = 1/3
    destWidth = (spriteWidth * scale * midpoint.x) * (((roadwidth * scaleX) / player.width()) * fator)
    destHeight = (spriteHeight * scale * midpoint.x) * (((roadwidth * scaleY) / player.width()) * fator)
    destX -= destWidth * 0.5
    destY -= destHeight * offsetY
    clipHeight = max(0,destY + destHeight * offsetY - clip) if clip else 0
    sprite.rect = pygame.Rect(destX,destY,destWidth,destHeight)
    if clipHeight < destHeight and destWidth < 2000:
        surface = pygame.Surface((spriteWidth,spriteHeight),pygame.SRCALPHA)
        surface.blit(sprite.image,(0,0),(0,0,spriteWidth,spriteHeight-(spriteHeight * clipHeight/destHeight)))
        image = pygame.transform.scale(surface,(destWidth,destHeight))
        screen.blit(image,(destX,destY))
        #pygame.draw.rect(screen,'green',sprite.rect,1)

tracks = {
    'teste': {
        'length': 5000,
        'curvas': [
            {'start': 500, 'end': 800, 'curva': 1},
            {'start': 800, 'end': 1300, 'curva': -1},
            {'start': 1800, 'end': 2000, 'curva': 1.5},
            {'start': 2500, 'end': 2900, 'curva': 1},
            {'start': 4000, 'end': 4500, 'curva': -1}
        ],
        'colinas': [
            {'start': 500, 'end': 860, 'angulo': 0, 'altura': 8000, 'offset': 1},
            {'start': 1000, 'end': 1360, 'angulo': 0, 'altura': 5000, 'offset': -1},
            {'start': 2000, 'end': 2360, 'angulo': 0, 'altura': 10000, 'offset': 1},
            {'start': 2360, 'end': 2720, 'angulo': 0, 'altura': 5000, 'offset': -1},
            {'start': 3500, 'end': 3860, 'angulo': 0, 'altura': 8000, 'offset': -1},
        ]
    }
}