import pygame, sys
from Background import *


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]


    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0, y_margin=0, y_padding=0, width = None, height = None, colorkey = None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.

        if width and height:
            x_sprite_size = width
            y_sprite_size = height

        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                             - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                             - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)


class Timer:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.height = 38
        self.width = 200

        # MAKE RECT OBJECT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, screen):
        dx = .4

        if self.width > 0:
            self.width -= dx
        else:
            self.width = 200

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw_rect(screen)

    def draw_rect(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        return self.width


class Teacher(pygame.sprite.Sprite):
    def __init__(self, x_val, y_val, tile_list, sprite_sheet):
        super().__init__()
        self.x_val = x_val
        self.y_val = y_val
        self.tile_list = tile_list
        self.sprite_sheet = sprite_sheet
        self.last = pygame.time.get_ticks()
        self.image_delay = 100
        self.current_frame = 0

        self.teacher_images = self.sprite_sheet.load_grid_images(4, 4, 6, 11, 0, 0, 21, 32, -1)
        for i in range(len(self.teacher_images)):
            self.teacher_images[i] = pygame.transform.scale(self.teacher_images[i], (45, 45))

        # STUDENT RUNNING DOWN ANIMATIONS
        self.teacher_run_dn1 = self.teacher_images[0]
        self.teacher_run_dn2 = self.teacher_images[1]
        self.teacher_run_dn3 = self.teacher_images[2]
        self.teacher_run_dn4 = self.teacher_images[3]
        # MAKE A RUN DOWN LIST
        self.teacher_dn_list = [self.teacher_run_dn1, self.teacher_run_dn2, self.teacher_run_dn3]

        # teacher RUNNING RIGHT ANIMATIONS
        self.teacher_run_rt1 = self.teacher_images[12]
        self.teacher_run_rt2 = self.teacher_images[13]
        self.teacher_run_rt3 = self.teacher_images[14]
        self.teacher_run_rt4 = self.teacher_images[15]
        # MAKE A RUN RIGHT LIST
        self.teacher_rt_list = [self.teacher_run_rt1, self.teacher_run_rt2, self.teacher_run_rt3]

        # teacher RUNNING UP ANIMATIONS
        self.teacher_run_up1 = self.teacher_images[4]
        self.teacher_run_up2 = self.teacher_images[5]
        self.teacher_run_up3 = self.teacher_images[6]
        self.teacher_run_up4 = self.teacher_images[7]
        # MAKE A RUN UP LIST
        self.teacher_up_list = [self.teacher_run_up1, self.teacher_run_up2, self.teacher_run_up3]

        # teacher RUNNING LEFT ANIMATIONS
        self.teacher_run_lt1 = self.teacher_images[8]
        self.teacher_run_lt2 = self.teacher_images[9]
        self.teacher_run_lt3 = self.teacher_images[10]
        self.teacher_run_lt4 = self.teacher_images[11]
        # MAKE A RUN LEFT LIST
        self.teacher_lt_list = [self.teacher_run_lt1, self.teacher_run_lt2, self.teacher_run_lt3]

        # STUDENT INITIAL IDLE
        self.teacher_idle_lt = self.teacher_run_lt3
        self.image = self.teacher_idle_lt
        self.rect = self.image.get_rect()
        self.rect.x = self.x_val
        self.rect.y = self.y_val

        self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

    def update(self, player1_adv, screen):
        LIGHT_RED = (219, 0, 135)
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # MOVING RIGHT
        if keys[pygame.K_d]:
            if player1_adv:
                dx = 5
            else:
                dx = 6
            self.left = False
            self.right = True
            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.teacher_rt_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.teacher_rt_list[self.current_frame]

        # MOVING LEFT
        elif keys[pygame.K_a]:
            if player1_adv:
                dx = -5
            else:
                dx = -6

            self.left = True
            self.right = False
            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.teacher_lt_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.teacher_lt_list[self.current_frame]

        # MOVING UP
        if keys[pygame.K_w]:
            dy = -5

            self.up = True
            self.down = False
            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.teacher_up_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.teacher_up_list[self.current_frame]

        # MOVING DOWN
        if keys[pygame.K_s]:
            dy = 5

            self.up = False
            self.down = True

            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.teacher_dn_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.teacher_dn_list[self.current_frame]

        # COLLISION
        # COLLISION WITH WALLS
        if self.rect.left <= 1:
            dx = 0
            if keys[pygame.K_d]:
                dx = 5

        elif self.rect.right >= 1049:
            dx = 0
            if keys[pygame.K_a]:
                dx = -5

        if self.rect.top <= 55:
            dy = 0
            if keys[pygame.K_s]:
                dy = 5
        if self.rect.bottom >= 599:
            dy = 0
            if keys[pygame.K_w]:
                dy = -5

        # COLLISIONS
        for tile in self.tile_list:
            if tile[2] == 'Collision':
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width - 5, self.rect.height - 5):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width - 5, self.rect.height - 5):
                    dy = 0

        self.rect.x += dx
        self.rect.y += dy

        # RECTANGLE THAT SHOWS WHO IS TAGGER
        self.tagger_rect.x = self.rect.centerx - 6
        self.tagger_rect.y = self.rect.top - 22

        # DRAW TAGGING RECTANGLE
        if player1_adv == False:
            pygame.draw.rect(screen, LIGHT_RED, self.tagger_rect)


class Student(pygame.sprite.Sprite):
    def __init__(self, x_val, y_val, tile_list, sprite_sheet):
        super().__init__()
        # INITIAL VARIABLES
        self.x_val = x_val
        self.y_val = y_val
        self.tile_list = tile_list
        self.sprite_sheet = sprite_sheet
        self.last = pygame.time.get_ticks()
        self.image_delay = 100
        self.current_frame = 0


        # MAKE STUDENT IMAGES
        self.student_images = self.sprite_sheet.load_grid_images(4, 3, 0, 12, 0, 0, 33, 36, -1)
        for i in range(len(self.student_images)):
            self.student_images[i] = pygame.transform.scale(self.student_images[i], (45, 45))

        # STUDENT RUNNING DOWN ANIMATIONS
        self.student_run_dn1 = self.student_images[0]
        self.student_run_dn2 = self.student_images[1]
        self.student_run_dn3 = self.student_images[2]
        # MAKE A RUN DOWN LIST
        self.student_dn_list = [self.student_run_dn1, self.student_run_dn2, self.student_run_dn3]

        # STUDENT RUNNING RIGHT ANIMATIONS
        self.student_run_rt1 = self.student_images[3]
        self.student_run_rt2 = self.student_images[4]
        self.student_run_rt3 = self.student_images[5]
        # MAKE A RUN RIGHT LIST
        self.student_rt_list = [self.student_run_rt1, self.student_run_rt2, self.student_run_rt3]

        # STUDENT RUNNING UP ANIMATIONS
        self.student_run_up1 = self.student_images[6]
        self.student_run_up2 = self.student_images[7]
        self.student_run_up3 = self.student_images[8]
        # MAKE A RUN UP LIST
        self.student_up_list = [self.student_run_up1, self.student_run_up2, self.student_run_up3]

        # STUDENT RUNNING LEFT ANIMATIONS
        self.student_run_lt1 = self.student_images[9]
        self.student_run_lt2 = self.student_images[10]
        self.student_run_lt3 = self.student_images[11]
        # MAKE A RUN LEFT LIST
        self.student_lt_list = [self.student_run_lt1, self.student_run_lt2, self.student_run_lt3]

        # STUDENT INITIAL IDLE
        self.student_idle_lt = self.student_run_lt3
        self.image = self.student_idle_lt
        self.rect = self.image.get_rect()
        self.rect.x = self.x_val
        self.rect.y = self.y_val

        self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

    def update(self, player1_adv, screen):
        LIGHT_BLUE = (52, 171, 235)
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # MOVING RIGHT
        if keys[pygame.K_RIGHT]:
            if player1_adv:
                dx = 6
            else:
                dx = 5
            self.left = False
            self.right = True
            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.student_rt_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.student_rt_list[self.current_frame]

        # MOVING LEFT
        elif keys[pygame.K_LEFT]:
            if player1_adv:
                dx = -6
            else:
                dx = -5

            self.left = True
            self.right = False
            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.student_lt_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.student_lt_list[self.current_frame]

        # MOVING UP
        if keys[pygame.K_UP]:
            dy = -5

            self.up = True
            self.down = False
            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.student_up_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.student_up_list[self.current_frame]

        # MOVING DOWN
        if keys[pygame.K_DOWN]:
            dy = 5

            self.up = False
            self.down = True

            now = pygame.time.get_ticks()
            if (now - self.last) >= self.image_delay:
                self.last = now

            if (self.current_frame + 1) < len(self.student_dn_list):
                self.current_frame += 1
            else:
                self.current_frame = 0
            self.image = self.student_dn_list[self.current_frame]

# COLLISION
        # COLLISION WITH WALLS
        if self.rect.left <= 1:
            dx = 0
            if keys[pygame.K_RIGHT]:
                dx = 5

        elif self.rect.right >= 1049:
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -5

        if self.rect.top <= 55:
            dy = 0
            if keys[pygame.K_DOWN]:
                dy = 5
        if self.rect.bottom >= 599:
            dy = 0
            if keys[pygame.K_UP]:
                dy = -5

        # COLLISIONS
        for tile in self.tile_list:
            if tile[2] == 'Collision':
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width - 5, self.rect.height - 5):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width - 5, self.rect.height - 5):
                    dy = 0



        # SET POSITION FOR PLAYER AND TAGGING RECTANGLE
        self.rect.x += dx
        self.rect.y += dy
        self.tagger_rect.x = self.rect.centerx - 6
        self.tagger_rect.y = self.rect.top - 22

        # DRAW TAGGING RECTANGLE
        if player1_adv:
            pygame.draw.rect(screen, LIGHT_BLUE, self.tagger_rect)


class Layout:
    def __init__(self, level_layout, BLOCK_SIZE):
        self.student_sheet = SpriteSheet('Student.png')
        self.teacher_sheet = SpriteSheet('Teacher.png')
        self.nerd_sheet = SpriteSheet('Nerd.png')
        self.dog_sheet = SpriteSheet('Dog.png')
        self.fence_sheet = SpriteSheet('Fence.png')

        self.layout = level_layout
        self.block_size = BLOCK_SIZE
        self.tile_list = []


        ############## MAKE IMAGES ################

        self.school_desk = pygame.image.load('Top_Down_Desk.png').convert_alpha()
        self.school_desk = pygame.transform.scale(self.school_desk, (self.block_size * 1.1, self.block_size))

        # YARD
        self.vert_fence = pygame.image.load('Vert_Fence.png').convert_alpha()
        self.vert_fence = pygame.transform.scale(self.vert_fence, (self.block_size / 2, self.block_size / 1.5))

        self.hor_fence = pygame.image.load('Hor_Fence.png').convert_alpha()
        self.hor_fence = pygame.transform.scale(self.hor_fence, (self.block_size / 1.5, self.block_size / 2))


        # MAKE LEVEL
        for i, row in enumerate(level_layout):
            for j, col in enumerate(row):
                x_val = j * self.block_size
                y_val = i * self.block_size

                if col == 'D':
                    img_rect = self.school_desk.get_rect()
                    img_rect.x = x_val - 11
                    img_rect.y = y_val
                    desk_tile = (self.school_desk, img_rect, 'Collision')
                    self.tile_list.append(desk_tile)

                elif col == 'V':
                    img_rect = self.vert_fence.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    vert_tile = (self.vert_fence, img_rect, 'Collision')
                    self.tile_list.append(vert_tile)

                elif col == 'H':
                    img_rect = self.hor_fence.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    hor_tile = (self.hor_fence, img_rect, 'Collision')
                    self.tile_list.append(hor_tile)


                elif col == '1':
                    self.player1 = Student(x_val, y_val, self.tile_list, self.student_sheet)

                elif col == '2':
                    self.player2 = Teacher(x_val, y_val, self.tile_list, self.teacher_sheet)



    def draw(self, screen, player1_adv):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


        self.player1.update(player1_adv, screen)
        self.player2.update(player1_adv, screen)
        # self.player.draw_student(screen)




