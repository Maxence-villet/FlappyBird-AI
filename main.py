import pygame
import sys
import random
from bird import Bird
from pipe import PipeManager
from ground import Ground
from utils import display_score, display_game_over

pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)

population_size = 100
population = [Bird(50, 250) for _ in range(population_size)]
pipe_manager = PipeManager()
ground = Ground()
font = pygame.font.Font(None, 36)
generation = 0
best_score = 0
current_max_score = 0

def reset_game(birds):
    global pipe_manager, current_max_score
    pipe_manager = PipeManager()
    current_max_score = 0
    for bird in birds:
        bird.reset()

def evolve_population(birds):
    global generation, best_score
    generation += 1
    
    # Vérifier si la liste birds est vide
    if not birds:
        return [Bird(50, 250) for _ in range(population_size)] # Retourner une nouvelle population si birds est vide

    birds.sort(key=lambda bird: bird.score, reverse=True)
    best_score = max(best_score, birds[0].score)
    
    # Sélection des 30% meilleurs + 20% aléatoires pour la diversité
    elite_size = int(population_size * 0.3)
    elite = birds[:elite_size]
    random_selection = random.sample(birds, int(population_size * 0.2))
    
    new_population = elite + random_selection
    
    # Remplissage avec des enfants
    while len(new_population) < population_size:
        parent1 = random.choice(elite)
        parent2 = random.choice(elite)
        
        # Croisement et mutation
        child = Bird(50, 250)
        child.weights = [
            (p1 + p2) / 2 + random.uniform(-0.2, 0.2)  # Mutation plus forte
            for p1, p2 in zip(parent1.weights, parent2.weights)
        ]
        new_population.append(child)
    
    return new_population

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(SKY_BLUE)
    pipe_manager.update()
    ground.update()
    pipe_manager.draw(screen)
    ground.draw(screen)

    alive_birds = []
    dead_birds = []  # Liste pour stocker les oiseaux morts

    for bird in population:
        # Vérifier si l'oiseau est toujours en vie
        if bird.rect.bottom < 550 and not bird.check_collision(pipe_manager.pipes):
            bird.update(pipe_manager.pipes)
            bird.draw(screen)
            alive_birds.append(bird)
        else:
            # L'oiseau est mort, l'ajouter à dead_birds
            dead_birds.append(bird)

    # Supprimer les oiseaux morts de la population
    for dead_bird in dead_birds:
        population.remove(dead_bird)

    # Incrémenter le score uniquement si un oiseau passe un pipe
    for bird in alive_birds:
        score_increment = pipe_manager.check_scoring(bird.rect)
        if score_increment > 0:
            current_max_score += score_increment
            break  # Un seul point par pipe passé, peu importe le nombre d'oiseaux

    # Affichage des informations
    display_score(screen, current_max_score, font, WHITE)
    generation_text = font.render(f'Gen: {generation}', True, WHITE)
    alive_text = font.render(f'Alive: {len(alive_birds)}', True, WHITE)
    screen.blit(generation_text, (10, 50))
    screen.blit(alive_text, (10, 90))

    if not alive_birds:
        population = evolve_population(population)
        reset_game(population)

    pygame.display.update()
    clock.tick(60)