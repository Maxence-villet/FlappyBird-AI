import pygame
import random

PIPE_GREEN = (0, 128, 0)

class PipeManager:
    def __init__(self):
        self.pipes = []
        self.pipe_width = 70
        self.pipe_gap = 150
        self.pipe_frequency = 1500  # milliseconds
        self.last_pipe = pygame.time.get_ticks()
        
        # Générer un premier pipe immédiatement
        self.generate_pipe()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe > self.pipe_frequency:
            self.generate_pipe()
            self.last_pipe = current_time

        for pipe in self.pipes:
            pipe['top'].x -= 4
            pipe['bottom'].x -= 4

        self.pipes = [pipe for pipe in self.pipes if pipe['top'].right > 0]

    def generate_pipe(self):
        pipe_height = random.randint(150, 400)
        top_pipe = pygame.Rect(400, 0, self.pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(400, pipe_height + self.pipe_gap, self.pipe_width, 600 - pipe_height - self.pipe_gap)
        self.pipes.append({'top': top_pipe, 'bottom': bottom_pipe, 'passed': False})

    def draw(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, PIPE_GREEN, pipe['top'])
            pygame.draw.rect(screen, PIPE_GREEN, pipe['bottom'])

    def check_scoring(self, bird_rect):
        score_increment = 0
        for pipe in self.pipes:
            if not pipe['passed'] and bird_rect.left > pipe['top'].right:
                score_increment = 1
                pipe['passed'] = True
        return score_increment

    def reset(self):
        self.pipes.clear()
        self.last_pipe = pygame.time.get_ticks()
        # Regénérer un premier pipe immédiatement après le reset
        self.generate_pipe()