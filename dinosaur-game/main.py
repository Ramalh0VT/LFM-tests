import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
dinosaur = pygame.Rect(100, 100, 50, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    dinosaur.move(-10, 0)  # Simple movement
    pygame.display.update()
pygame.time.wait(100)
pygame.quit()

