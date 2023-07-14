import pygame,math
import pygame.gfxdraw

class Gauge:
    def __init__(self):
        self.angulo_inicial = -225
        self.angulo_final = 45
        self.angulo_total = -self.angulo_inicial + self.angulo_final
        self.x = 905
        self.y = 531
        self.raio = 80

        self.color = pygame.Color(255,0,0)
        self.font = pygame.font.SysFont('Arial',10)

    def draw(self,screen,speedPercent):
        for i in range(13):
            distanci = 15 if i%2==0 else 10
            angulo = math.radians(-225+22.5*i)
            start_x,start_y = self.raio*math.cos(angulo)+self.x, self.raio*math.sin(angulo)+self.y
            end_x,end_y = (self.raio-distanci)*math.cos(angulo)+self.x, (self.raio-distanci)*math.sin(angulo)+self.y

            pygame.draw.line(screen,'white',(start_x,start_y),(end_x,end_y))
        
        for i in range(7):
                angle = math.radians(self.angulo_inicial+45*i)
                x = 50*math.cos(angle)+self.x
                y = 50*math.sin(angle)+self.y
                text = self.font.render(str(60*i),False,'white')
                text_rect = text.get_rect(center = (x,y))
                screen.blit(text,text_rect)

        pygame.gfxdraw.arc(screen,self.x,self.y,self.raio,self.angulo_inicial,self.angulo_final,self.color)

        speed_angle = (speedPercent * self.angulo_total) + self.angulo_inicial
        angle = math.radians(speed_angle)
        x = 50*math.cos(angle)+self.x
        y = 50*math.sin(angle)+self.y
        pygame.draw.line(screen,'red',(self.x,self.y),(x,y),2)