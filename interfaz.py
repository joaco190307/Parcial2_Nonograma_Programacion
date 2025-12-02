import pygame

pygame.init()

""" 
Colores 
"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARKGRAY = (40, 40, 40)
BLUE = (40, 120, 200)
GREEN = (40, 180, 100)
RED = (200, 60, 60)

"""
Fuentes

"""
FONT = pygame.font.SysFont("arial", 20)
BIGFONT = pygame.font.SysFont("arial", 36)

class Button:
    def __init__(self, rect, text, color=BLUE, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect, border_radius=8)
        txt = FONT.render(self.text, True, self.text_color)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
