import pygame, sys
from Background import *
from Sprites import Layout

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
LIGHT_BLUE = (196, 129, 82)

# ASSIGN LEVELS
level_select = []
level_counter = 0
level1 = Layout(LEVEL_1, BLOCK_SIZE)
level_select.append(level1)
level2 = Layout(LEVEL_2, BLOCK_SIZE)
level_select.append(level2)
level3 = Layout(LEVEL_3, BLOCK_SIZE)
level_select.append(level3)
level4 = Layout(LEVEL_4, BLOCK_SIZE)
level_select.append(level4)

# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(LIGHT_BLUE)

    level = level_select[level_counter]
    level.draw(screen)

    # draw_grid(SCREEN_W, SCREEN_H, BLOCK_SIZE)

    pygame.display.flip()
    clock.tick(FPS)


############################################################ USELESS STUFF DOWN HERE
# def draw_grid(width, height, size):
#     z = 0
#     for x in range(1, width - 50, size):
#         for y in range(1, height - 50, size):
#             z += 1
#             # rect = pygame.Rect(x, y, size, size)
#             # pygame.draw.rect(screen, WHITE, rect, 2)
#             if z not in range(10):
#                 screen.blit(class_floor, (x,y))





