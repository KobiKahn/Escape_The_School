import pygame, sys
import random
from Background import *
from Sprites import Layout, Timer

pygame.init()

# VARIABLES
# SCREEN SETUP
SCREEN_W = 1050
SCREEN_H = 600
BLOCK_SIZE = 50
FPS = 60

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Stop_The_Student')
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0,0,0)
LIGHT_BLUE = (52, 171, 235)
LIGHT_RED = (219, 0, 135)

# FONTS
comic_sans = pygame.font.SysFont('Comic Sans', 40)

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

# LEVEL NAMES
level_name = ''
level1_name = 'THE CLASSROOM'
level2_name = 'THE HALLWAY'
level3_name = 'THE PLAYGROUND'
level4_name = 'THE STREET'

# BACKGROUND IMAGES
classroom_bg = pygame.image.load('Classroom_Background.png').convert_alpha()

title_screen = pygame.image.load('Tag_Title_Screen.png').convert_alpha()

# SPRITE GROUPS
student_group = pygame.sprite.Group()
student_group.add(level1.student)

teacher_group = pygame.sprite.Group()
teacher_group.add(level1.teacher)

# DIFFERENT TIMERS
blue_timer = Timer(700, 4, LIGHT_BLUE)
red_timer = Timer(700, 4, LIGHT_RED)

timer_outline = pygame.image.load('Timer_Outline.png').convert_alpha()
timer_outline = pygame.transform.scale(timer_outline, (220, 55))

# INITIAL STUDENT SPEED AND TIMER
student_adv = False
timer = 0
collision = False
title_bool = False
# MAIN LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if title_bool == True:
        screen.blit(title_screen, (0, 0))

    else:
        # CHANGE WHO THE TAGGER IS
        timer += 1
        if timer >= 500:
            timer = 0
            if student_adv == True:
                student_adv = False
            else:
                student_adv = True

        # DRAW THINGS TO SCREEN
        screen.fill(BLACK)

        # DRAW HUD
        if level_counter == 0:
            level_name = comic_sans.render(f'{level1_name}', True, (255, 255, 255))
        elif level_counter == 1:
            level_name = comic_sans.render(f'{level2_name}', True, (255, 255, 255))
        elif level_counter == 2:
            level_name = comic_sans.render(f'{level3_name}', True, (255, 255, 255))
        elif level_counter == 3:
            level_name = comic_sans.render(f'{level4_name}', True, (255, 255, 255))
        screen.blit(level_name, (0,0))

        if student_adv:
            blue_timer.update(screen)
        else:
            red_timer.update(screen)

        screen.blit(timer_outline, (692, -5))

        # DRAW PLAY AREA
        if level_counter == 0:
            screen.blit(classroom_bg, (0, 50))
            student_group.draw(screen)
            teacher_group.draw(screen)

        level = level_select[level_counter]
        level.draw(screen, student_adv, collision)


        if level_counter == 0 and not collision:
            if student_adv:
                for student_sprite in student_group:
                    if pygame.sprite.spritecollide(student_sprite, teacher_group, True):
                        print('STUDENT WON!!')
                        collision = True
                        title_bool = True
                    else:
                        collision = False

            else:
                for teacher_sprite in teacher_group:
                    if pygame.sprite.spritecollide(teacher_sprite, student_group, True):
                        print('TEACHER WON!!')
                        collision = True
                        title_bool = True
                    else:
                        collision = False


    pygame.display.flip()
    clock.tick(FPS)





