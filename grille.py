import pygame
import sys

# --- Configuration ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialisation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grille Pygame")
clock = pygame.time.Clock()

# Tableau représentant la couleur de chaque case
grid = [[WHITE for _ in range(COLS)] for _ in range(ROWS)]

# --- Fonctions ---
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, grid[r][c],
                             (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Dessiner les lignes de la grille
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def color_grid(row, col, color):
    grid[row][col] = color

# --- Boucle principale ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)  # Fond blanc
    draw_grid()         # Dessine les cases colorées + lignes
    pygame.display.flip()

    clock.tick(60)
