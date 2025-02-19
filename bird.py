import pygame
import random

BIRD_YELLOW = (255, 255, 0)

class Bird:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.weights = [random.uniform(-2, 2) for _ in range(3)]  # Poids pour l'IA
        self.score = 0

    def update(self, pipes):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.top <= 0:
            self.rect.top = 0

        # Décision de saut basée sur les poids et les informations sur les tuyaux
        if pipes:
            next_pipe = next((p for p in pipes if p['top'].right > self.rect.left), None)
            if next_pipe:
                dx = next_pipe['top'].x - self.rect.centerx
                dy_top = next_pipe['top'].bottom - self.rect.centery
                dy_bottom = next_pipe['bottom'].top - self.rect.centery
            
                # Activation avec fonction sigmoïde
                activation = (
                    self.weights[0] * dx +
                    self.weights[1] * dy_top +
                    self.weights[2] * dy_bottom
                )
                if activation > 0: #seuil d'activation
                    self.jump()


    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, screen):
        pygame.draw.rect(screen, BIRD_YELLOW, self.rect)

    def check_collision(self, pipes):
        for pipe in pipes:
            if self.rect.colliderect(pipe['top']) or self.rect.colliderect(pipe['bottom']):
                return True
        return False

    def reset(self):
        self.rect.y = 250
        self.velocity = 0
        self.score = 0