import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))
    circle = pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)
    pygame.display.flip()
