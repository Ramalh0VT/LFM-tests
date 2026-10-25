import pygame
import sys
from random import randint

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dinosaur Game')

# Load images
dinosaur_image = pygame.image.load('dinosaur.png')
cactus_image = pygame.image.load('cactus.png')
background_image = pygame.image.load('background.png')

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Dinosaur class
class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = dinosaur_image.get_width()
        self.height = dinosaur_image.get_height()
        self.velocity = 0
        self.jumping = False
        self.jump_height = 20

    def move(self):
        if self.jumping:
            self.y -= self.velocity
            self.velocity -= 1
            if self.velocity <= -self.jump_height:
                self.y = HEIGHT - self.height
                self.jumping = False
                self.velocity = 0
        else:
            self.y += 2
            if self.y > HEIGHT - self.height:
                self.y = HEIGHT - self.height

    def draw(self):
        screen.blit(dinosaur_image, (self.x, self.y))

# Cactus class
class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - cactus_image.get_height()
        self.width = cactus_image.get_width()
        self.speed = 5

    def move(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = WIDTH + self.width

    def draw(self):
        screen.blit(cactus_image, (self.x, self.y))

# Game loop
clock = pygame.time.Clock()
dinosaur = Dinosaur(100, HEIGHT - dinosaur_image.get_height())
cactus = Cactus(WIDTH)

def game_over():
    font = pygame.font.Font(None, 72)
    text = font.render('Game Over', True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 
text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dinosaur.jumping:
                dinosaur.jumping = True

    # Update game objects
    dinosaur.move()
    cactus.move()

    # Check for collision
    if dinosaur.x < cactus.x + cactus.width and dinosaur.x + dinosaur.width > cactus.x and dinosaur.y < cactus.y + cactus.height and dinosaur.y + dinosaur.height > cactus.y:
        game_over()

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw game objects
    dinosaur.draw()
    cactus.draw()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()

