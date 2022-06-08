import pygame, sys
from Background import *
import random

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

class Cars(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, car_type):
        super().__init__()
        self.car_sheet = SpriteSheet('Cars.png')

        self.x_val = random.randint(-100, -50)
        self.y_val = y
        self.vel = vel
        self.car_type = car_type

        # 10 by 2
        # 83 by 59
        # start x 20
        # start y 1
        # y padding = 4
        # x padding = 23
        car_list = self.car_sheet.load_grid_images(10, 2, 20, 23, 1, 4, 83, 59, -1)

        # MAKE EVERY INDIVIDUAL COLOR CAR
        self.black_car_list = []
        self.white_car_list = []
        self.yellow_car_list = []
        self.green_car_list = []
        self.red_car_list = []

        self.black_car_list.extend([car_list[0], car_list[1], car_list[3], car_list[14]])
        self.white_car_list.extend([car_list[4], car_list[8], car_list[9], car_list[18], car_list[19]])
        self.yellow_car_list.extend([car_list[2], car_list[6], car_list[17]])
        self.green_car_list.extend([car_list[5], car_list[15]])
        self.red_car_list.extend([car_list[7], car_list[11], car_list[16]])

        if self.car_type == 'black':
            # SET RANDOM CAR
            random_car = random.randint(0, (len(self.black_car_list) - 1))
            self.image = self.black_car_list[random_car]
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

        elif self.car_type == 'white':
            # SET RANDOM CAR
            random_car = random.randint(0, (len(self.white_car_list) - 1))
            self.image = self.white_car_list[random_car]
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

        elif self.car_type == 'yellow':
            # SET RANDOM CAR
            random_car = random.randint(0, (len(self.yellow_car_list) - 1))
            self.image = self.yellow_car_list[random_car]
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

        elif self.car_type == 'green':
            # SET RANDOM CAR
            random_car = random.randint(0, (len(self.green_car_list) - 1))
            self.image = self.green_car_list[random_car]
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

        elif self.car_type == 'red':
            # SET RANDOM CAR
            random_car = random.randint(0, (len(self.red_car_list) - 1))
            self.image = self.red_car_list[random_car]
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

    def update(self):

        self.rect.x += self.vel

        if self.rect.x >= 1050:
            self.rect.x = random.randint(-100, -50)
            self.rect.y = random.randint(50, 550)





class Character(pygame.sprite.Sprite):
    def __init__(self, x_val, y_val, tile_list, character):
        super().__init__()
        self.student_sheet = SpriteSheet('Student.png')
        self.teacher_sheet = SpriteSheet('Teacher.png')
        self.nerd_sheet = SpriteSheet('Nerd.png')
        self.animal_sheet = SpriteSheet('Dog.png')

        self.x_val = x_val
        self.y_val = y_val
        self.tile_list = tile_list
        self.last = pygame.time.get_ticks()
        self.image_delay = 100
        self.current_frame = 0

        self.character = character

        # TEACHER ANIMATIONS
        if self.character == 'Teacher':
            self.teacher_images = self.teacher_sheet.load_grid_images(4, 4, 6, 11, 0, 0, 21, 32, -1)
            for i in range(len(self.teacher_images)):
                self.teacher_images[i] = pygame.transform.scale(self.teacher_images[i], (45, 45))


            # TEACHER RUNNING DOWN ANIMATIONS
            self.teacher_dn_images = self.teacher_sheet.load_grid_images(1, 4, 6, 11, 0, 0, 21, 32)
            for i in range(len(self.teacher_dn_images)):
                self.teacher_dn_images[i] = pygame.transform.scale(self.teacher_images[i], (45, 45))
            self.teacher_run_dn1 = self.teacher_dn_images[0]
            self.teacher_run_dn2 = self.teacher_dn_images[1]
            self.teacher_run_dn3 = self.teacher_dn_images[2]
            self.teacher_run_dn4 = self.teacher_dn_images[3]
            # MAKE A RUN DOWN LIST
            self.teacher_dn_list = [self.teacher_run_dn1, self.teacher_run_dn2, self.teacher_run_dn3, self.teacher_run_dn4]

            # TEACHER RUNNING RIGHT ANIMATIONS
            self.teacher_run_rt1 = self.teacher_images[12]
            self.teacher_run_rt2 = self.teacher_images[13]
            self.teacher_run_rt3 = self.teacher_images[14]
            self.teacher_run_rt4 = self.teacher_images[15]
            # MAKE A RUN RIGHT LIST
            self.teacher_rt_list = [self.teacher_run_rt1, self.teacher_run_rt2, self.teacher_run_rt3, self.teacher_run_rt4]

            # TEACHER RUNNING UP ANIMATIONS
            self.teacher_run_up1 = self.teacher_images[4]
            self.teacher_run_up2 = self.teacher_images[5]
            self.teacher_run_up3 = self.teacher_images[6]
            self.teacher_run_up4 = self.teacher_images[7]
            # MAKE A RUN UP LIST
            self.teacher_up_list = [self.teacher_run_up1, self.teacher_run_up2, self.teacher_run_up3, self.teacher_run_up4]

            # TEACHER RUNNING LEFT ANIMATIONS
            self.teacher_run_lt1 = self.teacher_images[8]
            self.teacher_run_lt2 = self.teacher_images[9]
            self.teacher_run_lt3 = self.teacher_images[10]
            self.teacher_run_lt4 = self.teacher_images[11]
            # MAKE A RUN LEFT LIST
            self.teacher_lt_list = [self.teacher_run_lt1, self.teacher_run_lt2, self.teacher_run_lt3, self.teacher_run_lt4]

            # TEACHER INITIAL IDLE
            self.teacher_idle_lt = self.teacher_run_lt3
            self.image = self.teacher_idle_lt
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

            # MAKE THE TAGGING RECTANGLE
            self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

            # MAKE ANIMATION DICTIONARY
            self.animation_dict = {"DN": self.teacher_dn_list, "RT": self.teacher_rt_list, "UP": self.teacher_up_list, "LT": self.teacher_lt_list}

        # STUDENT ANIMATIONS
        elif self.character == 'Student':
            # MAKE STUDENT IMAGES
            self.student_images = self.student_sheet.load_grid_images(4, 3, 0, 12, 0, 0, 33, 36, -1)
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

            # MAKE ANIMATION DICT
            self.animation_dict = {"DN": self.student_dn_list, "RT": self.student_rt_list, "UP": self.student_up_list, "LT": self.student_lt_list}

        # NERD ANIMATIONS
        elif self.character == 'Nerd':
            # MAKE NERD IMAGES
            self.nerd_images = self.nerd_sheet.load_grid_images(4, 4, 10, 15, 11, 16, 33, 32, -1)

            for i in range(len(self.nerd_images)):
                self.nerd_images[i] = pygame.transform.scale(self.nerd_images[i], (45, 45))

            # NERD RUNNING DOWN ANIMATIONS
            self.nerd_run_dn1 = self.nerd_images[0]
            self.nerd_run_dn2 = self.nerd_images[4]
            self.nerd_run_dn3 = self.nerd_images[8]
            self.nerd_run_dn4 = self.nerd_images[12]
            # MAKE A RUN DOWN LIST
            self.nerd_dn_list = [self.nerd_run_dn1, self.nerd_run_dn2, self.nerd_run_dn3, self.nerd_run_dn4]

            # NERD RUNNING RIGHT ANIMATIONS
            self.nerd_run_rt1 = self.nerd_images[3]
            self.nerd_run_rt2 = self.nerd_images[7]
            self.nerd_run_rt3 = self.nerd_images[11]
            self.nerd_run_rt4 = self.nerd_images[15]

            # MAKE A RUN RIGHT LIST
            self.nerd_rt_list = [self.nerd_run_rt1, self.nerd_run_rt2, self.nerd_run_rt3, self.nerd_run_rt4]

            # NERD RUNNING UP ANIMATIONS
            self.nerd_run_up1 = self.nerd_images[2]
            self.nerd_run_up2 = self.nerd_images[6]
            self.nerd_run_up3 = self.nerd_images[10]
            self.nerd_run_up4 = self.nerd_images[14]
            # MAKE A RUN UP LIST
            self.nerd_up_list = [self.nerd_run_up1, self.nerd_run_up2, self.nerd_run_up3, self.nerd_run_up4]

            # NERD RUNNING LEFT ANIMATIONS
            self.nerd_run_lt1 = self.nerd_images[1]
            self.nerd_run_lt2 = self.nerd_images[5]
            self.nerd_run_lt3 = self.nerd_images[9]
            self.nerd_run_lt4 = self.nerd_images[13]
            # MAKE A RUN LEFT LIST
            self.nerd_lt_list = [self.nerd_run_lt1, self.nerd_run_lt2, self.nerd_run_lt3, self.nerd_run_lt4]

            # NERD INITIAL IDLE
            self.nerd_idle_lt = self.nerd_run_lt3
            self.image = self.nerd_idle_lt
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

            self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

            # MAKE ANIMATION DICT
            self.animation_dict = {"DN": self.nerd_dn_list, "RT": self.nerd_rt_list, "UP": self.nerd_up_list, "LT": self.nerd_lt_list}


        # CAT ANIMATIONS
        elif self.character == 'Cat':
            # CAT RUNNING DOWN ANIMATIONS
            self.cat_dn_list = self.animal_sheet.load_grid_images(1, 3, 106, 20, 4, 0, 12, 27, -1)
            for i in range(len(self.cat_dn_list)):
                self.cat_dn_list[i] = pygame.transform.scale(self.cat_dn_list[i], (45, 45))

            self.cat_run_dn1 = self.cat_dn_list[0]
            self.cat_run_dn2 = self.cat_dn_list[1]
            self.cat_run_dn3 = self.cat_dn_list[2]

            # CAT RUNNING RIGHT ANIMATIONS
            self.cat_rt_list = self.animal_sheet.load_grid_images(1, 3, 98, 4, 71, 0, 28, 24, -1)
            for i in range(len(self.cat_rt_list)):
                self.cat_rt_list[i] = pygame.transform.scale(self.cat_rt_list[i], (45, 45))

            self.cat_run_rt1 = self.cat_rt_list[0]
            self.cat_run_rt2 = self.cat_rt_list[1]
            self.cat_run_rt3 = self.cat_rt_list[2]

            # CAT RUNNING UP ANIMATIONS
            self.cat_up_list = self.animal_sheet.load_grid_images(1, 3, 106, 20, 103, 0, 12, 24, -1)
            for i in range(len(self.cat_up_list)):
                self.cat_up_list[i] = pygame.transform.scale(self.cat_up_list[i], (45, 45))

            self.cat_run_up1 = self.cat_up_list[0]
            self.cat_run_up2 = self.cat_up_list[1]
            self.cat_run_up3 = self.cat_up_list[2]

            # CAT RUNNING LEFT ANIMATIONS
            self.cat_lt_list = self.animal_sheet.load_grid_images(1, 3, 98, 4, 39, 0, 28, 24, -1)
            for i in range(len(self.cat_lt_list)):
                self.cat_lt_list[i] = pygame.transform.scale(self.cat_lt_list[i], (45, 45))

            self.cat_run_lt1 = self.cat_lt_list[0]
            self.cat_run_lt2 = self.cat_lt_list[1]
            self.cat_run_lt3 = self.cat_lt_list[2]

            # CAT INITIAL IDLE
            self.cat_idle_lt = self.cat_run_lt2
            self.image = self.cat_idle_lt
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

            self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

            # MAKE ANIMATION DICT
            self.animation_dict = {"DN": self.cat_dn_list, "RT": self.cat_rt_list, "UP": self.cat_up_list, "LT": self.cat_lt_list}

            # DOG ANIMATIONS
        elif self.character == 'Dog':
            # DOG RUNNING DOWN ANIMATIONS

            self.dog_dn_list = self.animal_sheet.load_grid_images(1, 3, 9, 18, 130, 0, 14, 29, -1)
            for i in range(len(self.dog_dn_list)):
                self.dog_dn_list[i] = pygame.transform.scale(self.dog_dn_list[i], (45, 45))

            self.dog_run_dn1 = self.dog_dn_list[0]
            self.dog_run_dn2 = self.dog_dn_list[1]
            self.dog_run_dn3 = self.dog_dn_list[2]

            # DOG RUNNING RIGHT ANIMATIONS
            self.dog_rt_list = self.animal_sheet.load_grid_images(1, 3, 2, 2, 196, 0, 30, 28, -1)
            for i in range(len(self.dog_rt_list)):
                self.dog_rt_list[i] = pygame.transform.scale(self.dog_rt_list[i], (45, 45))

            self.dog_run_rt1 = self.dog_rt_list[0]
            self.dog_run_rt2 = self.dog_rt_list[1]
            self.dog_run_rt3 = self.dog_rt_list[2]

            # DOG RUNNING UP ANIMATIONS
            self.dog_up_list = self.animal_sheet.load_grid_images(1, 3, 9, 18, 229, 0, 14, 27, -1)
            for i in range(len(self.dog_up_list)):
                self.dog_up_list[i] = pygame.transform.scale(self.dog_up_list[i], (45, 45))

            self.dog_run_up1 = self.dog_up_list[0]
            self.dog_run_up2 = self.dog_up_list[1]
            self.dog_run_up3 = self.dog_up_list[2]

            # DOG RUNNING LEFT ANIMATIONS
            self.dog_lt_list = self.animal_sheet.load_grid_images(1, 3, 0, 2, 165, 0, 30, 27, -1)
            for i in range(len(self.dog_lt_list)):
                self.dog_lt_list[i] = pygame.transform.scale(self.dog_lt_list[i], (45, 45))

            self.dog_run_lt1 = self.dog_lt_list[0]
            self.dog_run_lt2 = self.dog_lt_list[1]
            self.dog_run_lt3 = self.dog_lt_list[2]

            # DOG INITIAL IDLE
            self.dog_idle_lt = self.dog_run_lt2
            self.image = self.dog_idle_lt
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

            self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

            # MAKE ANIMATION DICT
            self.animation_dict = {"DN": self.dog_dn_list, "RT": self.dog_rt_list, "UP": self.dog_up_list, "LT": self.dog_lt_list}

        elif self.character == 'Mouse':
            # MOUSE RUNNING DOWN ANIMATIONS
            self.mouse_dn_list = []
            self.mouse_run_dn1 = self.animal_sheet.image_at((10, 2, 15, 29), -1)
            # self.mouse_run_dn2 = self.animal_sheet.image_at((40, 6, 15, 26), -1)
            # self.mouse_run_dn3 = self.animal_sheet.image_at((74, 6, 15, 26), -1)

            self.mouse_dn_list.append(self.mouse_run_dn1)
            # self.mouse_dn_list.append(self.mouse_run_dn2)
            # self.mouse_dn_list.append(self.mouse_run_dn3)
            # self.animal_sheet.load_grid_images(1, 3, 10, 15, 1, 0, 15, 29, -1)
            for i in range(len(self.mouse_dn_list)):
                self.mouse_dn_list[i] = pygame.transform.scale(self.mouse_dn_list[i], (40, 45))



            # MOUSE RUNNING RIGHT ANIMATIONS
            self.mouse_rt_list = self.animal_sheet.load_grid_images(1, 3, 1, 2, 76, 0, 30, 20, -1)
            for i in range(len(self.mouse_rt_list)):
                self.mouse_rt_list[i] = pygame.transform.scale(self.mouse_rt_list[i], (45, 45))

            self.mouse_run_rt1 = self.mouse_rt_list[0]
            self.mouse_run_rt2 = self.mouse_rt_list[1]
            self.mouse_run_rt3 = self.mouse_rt_list[2]

            # MOUSE RUNNING UP ANIMATIONS
            self.mouse_up_list = self.animal_sheet.load_grid_images(1, 3, 10, 18, 96, 0, 13, 29, -1)
            for i in range(len(self.mouse_up_list)):
                self.mouse_up_list[i] = pygame.transform.scale(self.mouse_up_list[i], (40, 45))

            self.mouse_run_up1 = self.mouse_up_list[0]
            self.mouse_run_up2 = self.mouse_up_list[1]
            self.mouse_run_up3 = self.mouse_up_list[2]

            # MOUSE RUNNING LEFT ANIMATIONS
            self.mouse_lt_list = self.animal_sheet.load_grid_images(1, 3, 0, 1, 47, 0, 31, 17, -1)
            for i in range(len(self.mouse_lt_list)):
                self.mouse_lt_list[i] = pygame.transform.scale(self.mouse_lt_list[i], (45, 45))

            self.mouse_run_lt1 = self.mouse_lt_list[0]
            # self.mouse_run_lt2 = self.mouse_lt_list[1]
            # self.mouse_run_lt3 = self.mouse_lt_list[2]

            # MOUSE INITIAL IDLE
            self.mouse_idle_lt = self.mouse_run_lt1
            self.image = self.mouse_idle_lt
            self.rect = self.image.get_rect()
            self.rect.x = self.x_val
            self.rect.y = self.y_val

            self.tagger_rect = pygame.Rect(self.rect.centerx, self.rect.top - 10, 20, 20)

            # MAKE ANIMATION DICT
            self.animation_dict = {"DN": self.mouse_dn_list, "RT": self.mouse_rt_list, "UP": self.mouse_up_list, "LT": self.mouse_lt_list}



    def update(self, screen, player1_adv, who):

        LIGHT_BLUE = (52, 171, 235)
        LIGHT_RED = (219, 0, 135)
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()

        # CHECK IF PLAYER IS PLAYER 1
        if who == 'P1':
            if keys[pygame.K_d]:
                if player1_adv:
                    dx = 6
                else:
                    dx = 5
                self.left = False
                self.right = True
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['RT']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['RT'][self.current_frame]

            # MOVING LEFT
            elif keys[pygame.K_a]:
                if player1_adv:
                    dx = -6
                else:
                    dx = -5

                self.left = True
                self.right = False
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['LT']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['LT'][self.current_frame]

            # MOVING UP
            if keys[pygame.K_w]:
                dy = -5

                self.up = True
                self.down = False
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['UP']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['UP'][self.current_frame]

            # MOVING DOWN
            if keys[pygame.K_s]:
                dy = 5

                self.up = False
                self.down = True

                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['DN']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['DN'][self.current_frame]

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
                if tile[-1] == 'Collision':
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

        else:
            if keys[pygame.K_RIGHT]:
                if player1_adv:
                    dx = 5
                else:
                    dx = 6
                self.left = False
                self.right = True
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['RT']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['RT'][self.current_frame]

            # MOVING LEFT
            elif keys[pygame.K_LEFT]:
                if player1_adv:
                    dx = -5
                else:
                    dx = -6

                self.left = True
                self.right = False
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['LT']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['LT'][self.current_frame]

            # MOVING UP
            if keys[pygame.K_UP]:
                dy = -5

                self.up = True
                self.down = False
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['UP']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['UP'][self.current_frame]

            # MOVING DOWN
            if keys[pygame.K_DOWN]:
                dy = 5

                self.up = False
                self.down = True

                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay:
                    self.last = now

                if (self.current_frame + 1) < len(self.animation_dict['DN']):
                    self.current_frame += 1
                else:
                    self.current_frame = 0
                self.image = self.animation_dict['DN'][self.current_frame]

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

            self.rect.x += dx
            self.rect.y += dy

            # RECTANGLE THAT SHOWS WHO IS TAGGER
            self.tagger_rect.x = self.rect.centerx - 6
            self.tagger_rect.y = self.rect.top - 22

            # DRAW TAGGING RECTANGLE
            if player1_adv == False:
                pygame.draw.rect(screen, LIGHT_RED, self.tagger_rect)


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
    def __init__(self, level_layout, BLOCK_SIZE, char1, char2):
        # print(char1)
        # print(char2)
        self.student_sheet = SpriteSheet('Student.png')
        self.teacher_sheet = SpriteSheet('Teacher.png')
        self.nerd_sheet = SpriteSheet('Nerd.png')
        self.animal_sheet = SpriteSheet('Dog.png')
        self.fence_sheet = SpriteSheet('Fence.png')

        self.layout = level_layout
        self.block_size = BLOCK_SIZE
        self.tile_list = []
        self.char1 = char1
        self.char2 = char2


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
                    # self.player1 = Student(x_val, y_val, self.tile_list, self.student_sheet)
                    self.player1 = Character(x_val, y_val, self.tile_list, self.char1)

                elif col == '2':
                    self.player2 = Character(x_val, y_val, self.tile_list, self.char2)

                elif col == 'b':
                    self.black_car = Cars(x_val, y_val, 4, 'black')

                elif col == 'w':
                    self.white_car = Cars(x_val, y_val, 7, 'white')

                elif col == 'y':
                    self.yellow_car = Cars(x_val, y_val, 2, 'yellow')

                elif col == 'g':
                    self.green_car = Cars(x_val, y_val, 3, 'green')

                elif col == 'r':
                    self.red_car = Cars(x_val, y_val, 5, 'red')


    def draw(self, screen, player1_adv):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


        self.player1.update(screen, player1_adv, 'P1')
        self.player2.update(screen, player1_adv, 'P2')
        # self.player.draw_student(screen)




