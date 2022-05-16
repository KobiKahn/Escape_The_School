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
        self.height = 40
        self.width = 151

        # MAKE RECT OBJECT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, screen):
        dx = .5

        if self.width > 0:
            self.width -= dx
        else:
            self.width = 151

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.draw_rect(screen)

    def draw_rect(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


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
            self.teacher_images[i] = pygame.transform.scale(self.teacher_images[i], (50, 50))

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

    def update(self, student_adv):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # MOVING RIGHT
        if keys[pygame.K_d]:
            if student_adv:
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
            if student_adv:
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
            # if student_adv:
            #     dy = -5
            # else:
            #     dy = -6
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
            # if student_adv:
            #     dy = 5
            # else:
            #     dy = 6
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

        self.rect.x += dx
        self.rect.y += dy

    def draw_teacher(self, screen):
        screen.blit(self.image, self.rect)

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
            self.student_images[i] = pygame.transform.scale(self.student_images[i], (50, 50))

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

    def update(self, speed):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # MOVING RIGHT
        if keys[pygame.K_RIGHT]:
            if speed:
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
            if speed:
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
            # if speed:
            #     dy = -6
            # else:
            #     dy = -5
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
            # if speed:
            #     dy = 6
            # else:
            #     dy = 5
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


        self.rect.x += dx
        self.rect.y += dy


class Layout:
    def __init__(self, level_layout, BLOCK_SIZE):
        self.student_sheet = SpriteSheet('Student.png')
        self.teacher_sheet = SpriteSheet('Teacher.png')
        self.nerd_sheet = SpriteSheet('Nerd.png')
        self.dog_sheet = SpriteSheet('Dog.png')
        self.door_sheet = SpriteSheet('School_Door.png')

        self.layout = level_layout
        self.block_size = BLOCK_SIZE
        self.tile_list = []


        ############## MAKE IMAGES ################

        self.class_floor = pygame.image.load('School_Floor.png').convert_alpha()

        self.school_door_0 = self.door_sheet.image_at((4, 64, 16, 32))
        self.school_door_0 = pygame.transform.scale(self.school_door_0, (self.block_size, self.block_size))

        self.school_door_1 = self.door_sheet.image_at((4, 32, 10, 31))
        self.school_door_1 = pygame.transform.scale(self.school_door_1, (self.block_size, self.block_size))


        self.school_desk = pygame.image.load('Top_Down_Desk.png').convert_alpha()
        self.school_desk = pygame.transform.scale(self.school_desk, (self.block_size * 1.5, self.block_size))

        # PLAYGROUND
        self.grass = pygame.image.load('Grass.png').convert_alpha()
        self.grass = pygame.transform.scale(self.grass, (self.block_size, self.block_size))

        # STREET
        self.road = pygame.image.load('Road.png').convert_alpha()
        self.road = pygame.transform.scale(self.road, (self.block_size, self.block_size))

        counter = 0

        # MAKE LEVEL
        for i, row in enumerate(level_layout):
            for j, col in enumerate(row):
                x_val = j * self.block_size
                y_val = i * self.block_size

                if col == 'C':
                    img_rect = self.class_floor.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.class_floor, img_rect, 'Floor')
                    self.tile_list.append(tile)

                elif col == 'G':
                    img_rect = self.grass.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.grass, img_rect, 'Grass')
                    self.tile_list.append(tile)

                elif col == 'R':
                    img_rect = self.road.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.road, img_rect, 'Road')
                    self.tile_list.append(tile)

                elif col == 'E':
                    img_rect = self.school_door_0.get_rect()
                    img_rect.x = x_val
                    img_rect.y = y_val
                    tile = (self.road, img_rect, 'Door')
                    self.tile_list.append(tile)

                elif col == 'D':
                    img_rect = self.school_desk.get_rect()
                    img_rect.x = x_val - 11
                    img_rect.y = y_val
                    desk_tile = (self.school_desk, img_rect, 'Desk')
                    self.tile_list.append(desk_tile)

                elif col == 'P':
                    self.student = Student(x_val, y_val, self.tile_list, self.student_sheet)

                elif col == 'T':
                    self.teacher = Teacher(x_val, y_val, self.tile_list, self.teacher_sheet)



    def draw(self, screen, student_adv):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


        self.student.update(student_adv)
        self.teacher.update(student_adv)
        # self.player.draw_student(screen)




