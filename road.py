from segment_line import SegmentLine
from settings import colors
import pygame,math,os
from settings import *
from sprites import Sprites
from utils import tracks
from carro import Carro
from random import choice, randint

def import_sprites():
    sprite = {}
    for image in os.listdir('images/sprites'):
        sprite[image.split('.')[0]] = pygame.image.load(f'images/sprites/{image}').convert_alpha()
    
    return sprite

class Road:
    def __init__(self):
        self.segments = []
        self.segmentLength = 200 #a distancia
        self.segmentsLength = 0 #a quantindade de segmentos
        self.length = 0
        self.rumbleLength = 13
        self.width = 2000
        self.carros = []

        self.sprites = import_sprites()
    
    def create(self):
        pos = [1000,2000,3000,1500,4000,3500]
        for i in range(tracks['teste']['length']):
            line = SegmentLine()
            line.world_z = i * self.segmentLength + 0.000001
            line.world_w = self.width
            line.index = i

            lightestColors = { 'road': '#6B6B6B', 'grass':(255, 228, 179), 'rumble': 'white', 'strip': '#6B6B6B' }
            darkestColors = { 'road': '#696969', 'grass': (255, 219, 153), 'rumble': 'red', 'strip': 'white' }

            line.colors = lightestColors if (i//self.rumbleLength)%2 else darkestColors

            for n in tracks['teste']['curvas']:
                if i >= n['start'] and i <= n['end']:
                    line.curva = n['curva']
            
            for n in tracks['teste']['colinas']:
                if i >= n['start'] and i <= n['end']:
                    line.world_y = n['offset'] * math.sin(n['angulo'] / 180*math.pi) * n['altura']
                    n['angulo'] += 0.5
            
            if i%30 == 0 and i >= 0 and i <= 5000:
                sprite = Sprites()
                sprite.image = self.sprites['cactus']
                sprite.offsetX = choice([-3,-4,-5])
                line.sprites.append(sprite)

                sprite = Sprites()
                sprite.image = self.sprites['cactus']
                sprite.offsetX = choice([3,4,5])
                line.sprites.append(sprite)

                image = choice(['boulder2'])
                sprite = Sprites()
                sprite.image = self.sprites[image]
                sprite.offsetX = choice([-6,-7,-8])
                line.sprites.append(sprite)

                image = choice(['boulder2'])
                sprite = Sprites()
                sprite.image = self.sprites[image]
                sprite.offsetX = choice([6,7,8])
                line.sprites.append(sprite)

                image = choice(['boulder2','dead_tree2'])
                sprite = Sprites()
                sprite.image = self.sprites[image]
                sprite.offsetX = choice([9,10,11,12,13])
                line.sprites.append(sprite)

                image = choice(['boulder2','dead_tree2'])
                sprite = Sprites()
                sprite.image = self.sprites[image]
                sprite.offsetX = choice([-9,-10,-11,-12,-13])
                line.sprites.append(sprite)
            
            if i%1000 == 0:
                n = randint(1,9)
                sprite = Sprites()
                sprite.image = self.sprites[f'billboard0{n}']
                sprite.offsetX = 1.5
                line.sprites.append(sprite)

                n = randint(1,9)
                sprite = Sprites()
                sprite.image = self.sprites[f'billboard0{n}']
                sprite.offsetX = -1.5
                line.sprites.append(sprite)
            
            offset = choice([50,100,150])
            if i%offset == 0:
                sprite = Sprites()
                sprite.image = pygame.transform.flip(self.sprites['palm_tree'],True,False)
                sprite.offsetX = -2
                line.sprites.append(sprite)
            
            offset = choice([50,150,200])
            if i%offset == 0:
                sprite = Sprites()
                sprite.image = self.sprites['palm_tree']
                sprite.offsetX = 2
                line.sprites.append(sprite)
            
            self.segments.append(line)
                
            
        self.segmentsLength = len(self.segments)
        self.length = self.segmentsLength * self.segmentLength

        for i in pos:
            n = randint(1,4)
            offset = choice([0.5,-0.5])
            carro = Carro()
            carro.sprite.image = self.sprites[f'car0{n}']
            carro.offset = offset
            carro.z = i * self.segmentLength + 0.00001
            self.segments[i].carros.append(carro)
            self.carros.append(carro)
    
    def get_segment(self,cursor):
        return self.segments[(cursor//self.segmentLength)%self.segmentsLength]
    
    def get_segment_index(self,index):
        return self.segments[index%self.segmentsLength]
    
    def update(self,camera,player):
        for carro in self.carros:
            atual_segment = self.get_segment(int(carro.z))
            carro.update()
            next_segment = self.get_segment(int(carro.z))
            if atual_segment != next_segment:
                atual_segment.carros.remove(carro)
                next_segment.carros.append(carro)

        for carro in self.carros:
            if carro.sprite.rect and carro.sprite.rect.colliderect(player.sprite.rect):
                if carro.sprite.rect.y < player.sprite.rect.y:
                    camera.cursor -= 200
                    player.speed = player.speed * 0.5
                else:
                    atual_segment = self.get_segment(int(carro.z))
                    carro.z -= 400
                    carro.speed = 0
                    next_segment = self.get_segment(int(carro.z))
                    atual_segment.carros.remove(carro)
                    next_segment.carros.append(carro)

    def render(self,camera,player,screen):
        baseSegment = self.get_segment(camera.cursor)
        start_pos = baseSegment.index
        camera.y = camera.h + baseSegment.world_y
        visibleSegments = 300
        maxy = screen_height
        anx = 0
        snx = 0

        for i in range(start_pos,start_pos+visibleSegments):
            current_segment = self.get_segment_index(i)
            current_segment.clip = maxy
            camera.z = camera.cursor - (self.length if i >= self.segmentsLength else 0)
            camera.x =  player.x*current_segment.world_w -snx
            current_segment.project(camera)

            anx += current_segment.curva
            snx += anx

            if current_segment.screen_y >= maxy or (current_segment.world_z - camera.z) <= camera.distanci:
                continue

            if i > 0:
                prev_segment = self.get_segment_index(i-1)
                if current_segment.screen_y >= prev_segment.screen_y:
                    continue
                color = current_segment.colors

                pygame.draw.polygon(screen,color['road'],[
                    (prev_segment.screen_x - prev_segment.screen_w,prev_segment.screen_y),
                    (current_segment.screen_x - current_segment.screen_w,current_segment.screen_y),
                    (current_segment.screen_x + current_segment.screen_w,current_segment.screen_y),
                    (prev_segment.screen_x + prev_segment.screen_w,prev_segment.screen_y),
                ])

                #draw rumble left
                pygame.draw.polygon(screen,color['rumble'],[
                    (prev_segment.screen_x - prev_segment.screen_w*1.2,prev_segment.screen_y),
                    (current_segment.screen_x - current_segment.screen_w*1.2,current_segment.screen_y),
                    (current_segment.screen_x - current_segment.screen_w,current_segment.screen_y),
                    (prev_segment.screen_x - prev_segment.screen_w,prev_segment.screen_y)

                ])

                #draw rumble right
                pygame.draw.polygon(screen,color['rumble'],[
                    (prev_segment.screen_x + prev_segment.screen_w*1.2,prev_segment.screen_y),
                    (current_segment.screen_x + current_segment.screen_w*1.2,current_segment.screen_y),
                    (current_segment.screen_x + current_segment.screen_w,current_segment.screen_y),
                    (prev_segment.screen_x + prev_segment.screen_w,prev_segment.screen_y)

                ])

                #draw grass left
                pygame.draw.polygon(screen,color['grass'],[
                    (0,prev_segment.screen_y),
                    (0,current_segment.screen_y),
                    (current_segment.screen_x - current_segment.screen_w*1.2,current_segment.screen_y),
                    (prev_segment.screen_x - prev_segment.screen_w*1.2,prev_segment.screen_y)
                ])

                #draw grass right
                pygame.draw.polygon(screen,color['grass'],[
                    (screen_width,prev_segment.screen_y),
                    (screen_width,current_segment.screen_y),
                    (current_segment.screen_x + current_segment.screen_w*1.2,current_segment.screen_y),
                    (prev_segment.screen_x + prev_segment.screen_w*1.2,prev_segment.screen_y)
                ])

                #draw lane
                pygame.draw.polygon(screen,color['strip'],[
                    (prev_segment.screen_x - prev_segment.screen_w*0.01,prev_segment.screen_y),
                    (current_segment.screen_x - current_segment.screen_w*0.01,current_segment.screen_y),
                    (current_segment.screen_x + current_segment.screen_w*0.01,current_segment.screen_y),
                    (prev_segment.screen_x + prev_segment.screen_w*0.01,prev_segment.screen_y)
                ])
            maxy = current_segment.screen_y


        for i in range(start_pos + visibleSegments, start_pos, -1):
            segment = self.get_segment_index(i)
            if segment.sprites:
                segment.draw_sprite(camera,player,screen)
            if segment.carros:
                segment.draw_carro(camera,player,screen)