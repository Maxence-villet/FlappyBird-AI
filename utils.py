import pygame

def display_score(screen, score, font, color):
    score_surface = font.render(f'Score: {score}', True, color)
    screen.blit(score_surface, (10, 10))

def display_game_over(screen, font, color):
    game_over_text = font.render('Game Over! Space to restart', True, color)
    screen.blit(game_over_text, (70, 250))