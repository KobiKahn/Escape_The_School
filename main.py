import pygame, sys
pygame.init()

SCREEN_W = 800
SCREEN_H = 500
BLOCK_SIZE = 50
FPS = 60

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

pygame.display.set_caption('Stop_The_Student')

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0,0,0)

class_floor_img = 'Class_Floor.png'
class_floor = pygame.image.load(class_floor_img).convert_alpha()

def draw_grid(width, height, size):

    for x in range(1, width, size):
        for y in range(1, height, size):
            # rect = pygame.Rect(x, y, size, size)
            # pygame.draw.rect(screen, WHITE, rect, 2)
            screen.blit(class_floor, (x,y))

while True:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    draw_grid(SCREEN_W, SCREEN_H, BLOCK_SIZE)

    pygame.display.flip()
    clock.tick(FPS)







