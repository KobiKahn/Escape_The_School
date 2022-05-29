import pygame, sys
import random
from Background import *
from Sprites import Layout, Timer

pygame.init()

# FUNCTIONS

def start_screen(lx, ly, lw, lh):
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Stop_The_Student')
    running = True

    clock = pygame.time.Clock()
    while running:
        title_background = pygame.image.load('Tag_Title_Screen.png').convert_alpha()
        level_rect = pygame.Rect(lx, ly, lw, lh)

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if level_rect.collidepoint(pos):
                    running = False

        screen.fill(BLACK)
        screen.blit(title_background, (0,0))
        # pygame.draw.rect(screen, (0, 0, 0), level_rect)

        pygame.display.flip()
        clock.tick(FPS)


def level_screen():
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Stop_The_Student')
    running = True

    clock = pygame.time.Clock()
    while running:
        pos = pygame.mouse.get_pos()

        level1_button = pygame.Rect(50, 110, 230, 60)
        level2_button = pygame.Rect(370, 110, 230, 60)
        level3_button = pygame.Rect(670, 110, 230, 60)
        back_button = pygame.Rect(50, 515, 152, 60)

        level_1 = level_select_text.render(f'LEVEL 1', True, (255, 255, 255))
        level_2 = level_select_text.render(f'LEVEL 2', True, (255, 255, 255))
        level_3 = level_select_text.render(f'LEVEL 3', True, (255, 255, 255))

        back = level_select_text.render(f'BACK', True, (255, 255, 255))


        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:
                if level1_button.collidepoint(pos):
                    running = False
                    return (True, 0)

                elif level2_button.collidepoint(pos):
                    runnning = False
                    return (True, 1)
                elif level3_button.collidepoint(pos):
                    running = False
                    return (True, 2)
                elif back_button.collidepoint(pos):
                    running = False
                    return(False)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if level1_button.collidepoint(pos):
            level_1 = level_select_text.render(f'LEVEL 1', True, (255, 60, 30))

        elif level2_button.collidepoint(pos):
            level_2 = level_select_text.render(f'LEVEL 2', True, (255, 60, 30))

        elif level3_button.collidepoint(pos):
            level_3 = level_select_text.render(f'LEVEL 3', True, (255, 60, 30))

        elif back_button.collidepoint(pos):
            back = level_select_text.render(f'BACK', True, (255, 60, 30))


        screen.fill(LIGHT_BLUE)
        # pygame.draw.rect(screen, (0, 0, 0), level1_button)
        # pygame.draw.rect(screen, (0, 0, 0), level2_button)
        # pygame.draw.rect(screen, (0, 0, 0), level3_button)
        # pygame.draw.rect(screen, (0,0,0), back_button)

        screen.blit(level_1, (50, 100))
        screen.blit(level_2, (370, 100))
        screen.blit(level_3, (670, 100))
        screen.blit(back, (50, 500))

        pygame.display.flip()
        clock.tick(FPS)

def play_screen(level_counter):
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Stop_The_Student')
    # INITIAL VALS
    level_name = ''
    level1_name = 'THE CLASSROOM'
    level2_name = 'THE PLAYGROUND'
    level3_name = 'THE STREET'

    blue_timer = Timer(700, 4, LIGHT_BLUE)
    red_timer = Timer(700, 4, LIGHT_RED)

    running = True
    timer = 0
    student_adv = False

    # ASSIGN LEVELS
    level_select = []
    level1 = Layout(LEVEL_1, BLOCK_SIZE)
    level_select.append(level1)
    level2 = Layout(LEVEL_2, BLOCK_SIZE)
    level_select.append(level2)
    level3 = Layout(LEVEL_3, BLOCK_SIZE)
    level_select.append(level3)

    # BACKGROUND IMAGES
    classroom_bg = pygame.image.load('Classroom_Background.png').convert_alpha()

    # SPRITE GROUPS
    student_group = pygame.sprite.Group()
    student_group.add(level1.student)

    teacher_group = pygame.sprite.Group()
    teacher_group.add(level1.teacher)

    timer_outline = pygame.image.load('Timer_Outline.png').convert_alpha()
    timer_outline = pygame.transform.scale(timer_outline, (220, 55))

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        screen.blit(level_name, (0, 0))

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
        level.draw(screen, student_adv)

        # COLLISION
        if level_counter == 0:
            if student_adv:
                for student_sprite in student_group:
                    if pygame.sprite.spritecollide(student_sprite, teacher_group, True):
                        print('STUDENT WON!!')
                        running = False
                        return('STUDENT')

            else:
                for teacher_sprite in teacher_group:
                    if pygame.sprite.spritecollide(teacher_sprite, student_group, True):
                        print('TEACHER WON!!')
                        running = False
                        return('TEACHER')

        pygame.display.flip()
        clock.tick(FPS)

def end_screen(winner):
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Stop_The_Student')
    running = True

    # BUTTONS
    title_button = pygame.Rect(135, 500, 320, 50)
    exit_button = pygame.Rect(885, 500, 140, 50)



    clock = pygame.time.Clock()

    while running:
        winner_text = comic_sans.render(f'{winner} WON THE GAME!!', True, (255, 255, 255))
        title_text = comic_sans.render(f'TITLE SCREEN', True, (255, 255, 255))
        exit_text = comic_sans.render(f'EXIT', True, (255, 255, 255))

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                if title_button.collidepoint(pos):
                    return True
                elif exit_button.collidepoint(pos):
                    return False


        if title_button.collidepoint(pos):
            title_text = comic_sans.render(f'TITLE SCREEN', True, (255, 60, 30))

        elif exit_button.collidepoint(pos):
            exit_text = comic_sans.render(f'EXIT', True, (255, 60, 30))

        # pygame.draw.rect(screen, LIGHT_BLUE, title_button)
        # pygame.draw.rect(screen, LIGHT_BLUE, exit_button)

        screen.blit(winner_text, (250, 280))
        screen.blit(title_text, (140, 500))
        screen.blit(exit_text, (890, 500))

        pygame.display.flip()
        clock.tick(FPS)

def character_screen():
    player1_nerd = pygame.Rect(30, 30, 50, 50)
    player1_student = pygame.Rect(30, 90, 50, 50)
    player1_teacher = pygame.Rect(30, 150, 50, 50)
    player1_dog = pygame.Rect(30, 210, 50, 50)
    player1_cat = pygame.Rect(30, 270, 50, 50)
    player1_mouse = pygame.Rect(30, 330, 50, 50)


# VARIABLES
# SCREEN SETUP
SCREEN_W = 1050
SCREEN_H = 600
BLOCK_SIZE = 50
FPS = 60


# COLORS
WHITE = (255, 255, 255)
BLACK = (0,0,0)
LIGHT_BLUE = (52, 171, 235)
LIGHT_RED = (219, 0, 135)

# FONTS
comic_sans = pygame.font.SysFont('Comic Sans', 40)
level_select_text = pygame.font.SysFont('Comic Sans', 60)

clock = pygame.time.Clock()

game_run = True
# MAIN LOOP
while game_run:
    start_screen(359, 269, 367, 57)

    level_tuple = level_screen()
    if level_tuple == False:
        pass

    elif level_tuple[0]:
        level_counter = level_tuple[1]
        winner = play_screen(level_counter)
        if end_screen(winner):
            pass
        else:
            game_run = False



