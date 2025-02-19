import pygame

GROUND_BROWN = (139, 69, 19)

class Ground:
    def __init__(self):
        self.base_x = 0
        self.base_speed = 4

    def update(self):
        self.base_x -= self.base_speed
        if self.base_x <= -400:
            self.base_x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, GROUND_BROWN, (self.base_x, 550, 400, 50))
        pygame.draw.rect(screen, GROUND_BROWN, (self.base_x + 400, 550, 400, 50))