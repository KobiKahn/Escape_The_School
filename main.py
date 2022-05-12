import pygame, sys
from Background import *
from Sprites import Layout

pygame.init()

SCREEN_W = 1050
SCREEN_H = 550
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


# BACKGROUND IMAGES
classroom_bg = pygame.image.load('Classroom_Background.png').convert_alpha()

# SPRITE GROUPS
student_group = pygame.sprite.Group()
student_group.add(level1.student)

# MAIN LOOP    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # screen.fill(BLACK)

    screen.blit(classroom_bg, (0,0))

    level = level_select[level_counter]
    level.draw(screen)

    student_group.draw(screen)
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





