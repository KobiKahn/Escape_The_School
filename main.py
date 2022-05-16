import pygame, sys
import random
from Background import *
from Sprites import Layout

pygame.init()

# VARIABLES
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

teacher_group = pygame.sprite.Group()
teacher_group.add(level1.teacher)

# INITIAL STUDENT SPEED AND TIMER
student_adv = False
timer = 0

# MAIN LOOP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # CHANGE WHO THE TAGGER IS
    timer += 1
    if timer >= 300:
        timer = 0

        if student_adv == True:
            student_adv = False
            print('Student is slow now')
        else:
            student_adv = True
            print('Student is fast now')
        # print(student_adv)

    # DRAW THINGS TO SCREEN
    screen.blit(classroom_bg, (0, 0))

    level = level_select[level_counter]
    level.draw(screen, student_adv)

    student_group.draw(screen)
    teacher_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)





