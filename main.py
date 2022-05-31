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
        character_rect = pygame.Rect(250, 440, 550, 60)


        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if level_rect.collidepoint(pos):
                    running = False
                    return(True)

                elif character_rect.collidepoint(pos):
                    running = False
                    return(False)



        screen.fill(BLACK)
        screen.blit(title_background, (0,0))
        # pygame.draw.rect(screen, (0, 0, 0), character_rect)

        pygame.display.flip()
        clock.tick(FPS)

def character_screen():
    GREEN = (0, 227, 19)
    RED = (224, 0, 22)
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Stop_The_Student')
    running = True
    player1_select = None
    player2_select = None

    character_select_bg = pygame.image.load('Character_Select.png').convert_alpha()

    clock = pygame.time.Clock()
    # TEXT
    player1_ready = level_select_text.render('READY', True, RED)
    player2_ready = level_select_text.render('READY', True, RED)

    back = level_select_text.render('BACK', True, (255, 255, 255))
    p1_ready = False
    p2_ready = False

    while running:
        pos = pygame.mouse.get_pos()

        # RECTANGLES
        # PLAYER 1
        player1_student = pygame.Rect(42, 199, 60, 71)
        player1_teacher = pygame.Rect(197, 199, 60, 71)
        player1_nerd = pygame.Rect(355, 199, 60, 71)
        player1_cat = pygame.Rect(43, 381, 60, 71)
        player1_mouse = pygame.Rect(199, 381, 60, 71)
        player1_dog = pygame.Rect(358, 381, 60, 71)

        # PLAYER 2
        player2_student = pygame.Rect(617, 198, 60, 71)
        player2_teacher = pygame.Rect(792, 197, 60, 71)
        player2_nerd = pygame.Rect(939, 193, 60, 71)
        player2_cat = pygame.Rect(626, 376, 60, 71)
        player2_mouse = pygame.Rect(800, 373, 60, 71)
        player2_dog = pygame.Rect(950, 378, 60, 71)


        back_button = pygame.Rect(470, 499, 128, 68)

        ready1_rect = pygame.Rect(150, 520, 200, 60)
        ready2_rect = pygame.Rect(750, 520, 200, 60)



        # COLLISION
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                # PLAYER 1 COLLISION
                if player1_student.collidepoint(pos):
                    player1_select = 'Student'

                elif player1_teacher.collidepoint(pos):
                    player1_select = 'Teacher'

                elif player1_nerd.collidepoint(pos):
                    player1_select = 'Nerd'

                elif player1_cat.collidepoint(pos):
                    player1_select = 'Cat'

                elif player1_mouse.collidepoint(pos):
                    player1_select = 'Mouse'

                elif player1_dog.collidepoint(pos):
                    player1_select = 'Dog'

                # PLAYER 2 COLLISION
                elif player2_student.collidepoint(pos):
                    player2_select = 'Student'

                elif player2_teacher.collidepoint(pos):
                    player2_select = 'Teacher'

                elif player2_nerd.collidepoint(pos):
                    player2_select = 'Nerd'

                elif player2_cat.collidepoint(pos):
                    player2_select = 'Cat'

                elif player2_mouse.collidepoint(pos):
                    player2_select = 'Mouse'

                elif player2_dog.collidepoint(pos):
                    player2_select = 'Dog'



                elif ready1_rect.collidepoint(pos):
                    player1_ready = level_select_text.render('READY', True, GREEN)
                    p1_ready = True

                elif ready2_rect.collidepoint(pos):
                    player2_ready = level_select_text.render('READY', True, GREEN)
                    p2_ready = True

                if p1_ready and p2_ready and back_button.collidepoint(pos) and player1_select != None and player2_select != None:
                    print(player1_select, player2_select)
                    return(player1_select, player2_select)



        # print(player1_select)

        screen.blit(character_select_bg, (0,0))
        screen.blit(player1_ready, (150, 500))
        screen.blit(player2_ready, (750, 500))
        screen.blit(back, (470, 499))

        # pygame.draw.rect(screen, (255,255,255), ready1_rect)
        # pygame.draw.rect(screen, (255, 255, 255), ready2_rect)

        # DRAW INITIAL RECTANGLE OUTLINES
        pygame.draw.rect(screen, (255, 255, 255), player1_student, 3)
        pygame.draw.rect(screen, (255, 255, 255), player1_teacher, 3)
        pygame.draw.rect(screen, (255, 255, 255), player1_nerd, 3)
        pygame.draw.rect(screen, (255, 255, 255), player1_cat, 3)
        pygame.draw.rect(screen, (255, 255, 255), player1_mouse, 3)
        pygame.draw.rect(screen, (255, 255, 255), player1_dog, 3)

        pygame.draw.rect(screen, (255, 255, 255), player2_student, 3)
        pygame.draw.rect(screen, (255, 255, 255), player2_teacher, 3)
        pygame.draw.rect(screen, (255, 255, 255), player2_nerd, 3)
        pygame.draw.rect(screen, (255, 255, 255), player2_cat, 3)
        pygame.draw.rect(screen, (255, 255, 255), player2_mouse, 3)
        pygame.draw.rect(screen, (255, 255, 255), player2_dog, 3)

        # SELECT COLOR FOR PLAYER 1
        if player1_select == 'Student':
            pygame.draw.rect(screen, GREEN, player1_student, 3)
        elif player1_select == 'Teacher':
            pygame.draw.rect(screen, GREEN, player1_teacher, 3)

        elif player1_select == 'Nerd':
            pygame.draw.rect(screen, GREEN, player1_nerd, 3)

        elif player1_select == 'Cat':
            pygame.draw.rect(screen, GREEN, player1_cat, 3)

        elif player1_select == 'Mouse':
            pygame.draw.rect(screen, GREEN, player1_mouse, 3)

        elif player1_select == 'Dog':
            pygame.draw.rect(screen, GREEN, player1_dog, 3)

        # SELECT COLOR FOR PLAYER 2
        if player2_select == 'Student':
            pygame.draw.rect(screen, GREEN, player2_student, 3)
        elif player2_select == 'Teacher':
            pygame.draw.rect(screen, GREEN, player2_teacher, 3)

        elif player2_select == 'Nerd':
            pygame.draw.rect(screen, GREEN, player2_nerd, 3)

        elif player2_select == 'Cat':
            pygame.draw.rect(screen, GREEN, player2_cat, 3)

        elif player2_select == 'Mouse':
            pygame.draw.rect(screen, GREEN, player2_mouse, 3)

        elif player2_select == 'Dog':
            pygame.draw.rect(screen, GREEN, player2_dog, 3)


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


def play_screen(level_counter, char1, char2):
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Stop_The_Student')
    # INITIAL VALS
    level_name = ''
    level1_name = 'THE CLASSROOM'
    level2_name = 'THE YARD'
    level3_name = 'THE STREET'

    blue_timer = Timer(700, 4, LIGHT_BLUE)
    red_timer = Timer(700, 4, LIGHT_RED)

    running = True
    timer = 0
    player1_adv = False
    # print(char1, char2)

    # ASSIGN LEVELS
    level_select = []
    level1 = Layout(LEVEL_1, BLOCK_SIZE, char1, char2)
    level_select.append(level1)
    level2 = Layout(LEVEL_2, BLOCK_SIZE, char1, char2)
    level_select.append(level2)
    level3 = Layout(LEVEL_3, BLOCK_SIZE, char1, char2)
    level_select.append(level3)

    # BACKGROUND IMAGES
    classroom_bg = pygame.image.load('Classroom_Background.png').convert_alpha()

    yard_bg = pygame.image.load('Grass_Level.png').convert_alpha()

    # SPRITE GROUPS
    player1_group = pygame.sprite.Group()
    player2_group = pygame.sprite.Group()
    if level_counter == 0:
        player1_group.add(level1.player1)
        player2_group.add(level1.player2)

    elif level_counter == 1:
        player1_group.add(level2.player1)
        player2_group.add(level2.player2)

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
            if player1_adv == True:
                player1_adv = False
            else:
                player1_adv = True

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

        if player1_adv:
            blue_timer.update(screen)
        else:
            red_timer.update(screen)

        screen.blit(timer_outline, (692, -5))

        # DRAW PLAY AREA
        if level_counter == 0:
            screen.blit(classroom_bg, (0, 50))
            player1_group.draw(screen)
            player2_group.draw(screen)

        elif level_counter == 1:
            screen.blit(yard_bg, (0, 50))
            player1_group.draw(screen)
            player2_group.draw(screen)


        level = level_select[level_counter]
        level.draw(screen, player1_adv)

        # COLLISION
        if player1_adv:
            for player1_sprite in player1_group:
                if pygame.sprite.spritecollide(player1_sprite, player2_group, True):
                    # print('PLAYER 1 WON!!')
                    running = False
                    return('PLAYER 1')

        else:
            for player2_sprite in player2_group:
                if pygame.sprite.spritecollide(player2_sprite, player1_group, True):
                    # print('PLAYER 2 WON!!')
                    running = False
                    return('PLAYER 2')

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
# BASE CHARACTERS IF PERSON DOESNT SELECT NEW ONES
char1 = 'Student'
char2 = 'Teacher'

# MAIN LOOP
while game_run:
    if start_screen(359, 269, 367, 57):
        level_tuple = level_screen()

        if level_tuple == False:
            pass

        elif level_tuple[0]:
            level_counter = level_tuple[1]
            winner = play_screen(level_counter, char1, char2)
            if end_screen(winner):
                pass
            else:
                game_run = False
    else:
        char1, char2 = character_screen()



