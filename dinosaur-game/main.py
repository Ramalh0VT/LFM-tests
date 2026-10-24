import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Dinosaur Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Dinosaur class (simplified)
class Dinosaur:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 50
        self.speed = 5
        self.direction = 1  # 1 = right, -1 = left, 0 = down

    def move(self):
        self.x += self.speed * self.direction
        self.y -= self.direction * 5  # Adjust y based on direction

# Game loop
running = True
score = 0
obstacle = Dinosaur()

while running:
    screen.fill(WHITE)
    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            Dinosaur.speed = -1
        elif event.key == pygame.K_RIGHT:
            Dinosaur.speed = 1
        elif event.key == pygame.K_SPACE:
            score += 1

    # Update position
    Dinosaur.move()

    # Check collisions (simplified)
    if Dinosaur.x < 50 or Dinosaur.x > WIDTH - 50:
        score -= 10
        Dinosaur.x = 100  # Reset position

    # Draw everything
    pygame.draw.rect(screen, GREEN, (Dinosaur.x, Dinosaur.y, 100, 20))
    pygame.draw.circle(screen, RED, (Dinosaur.x, Dinosaur.y, 10), 5)
    pygame.display.update()

    # Draw score
    text = f"Score: {score}"
    pygame.draw.rect(screen, BLACK, (10, 10, 20, 20), 2)
    pygame.draw.text(screen, BLACK, (20, 20), text)

    pygame.display.flip()

# Close pygame
pygame.quit()
sys.exit()

