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



class Student:
    def __init__(self, x_val, y_val, tile_list, sprite_sheet):
        self.x_val = x_val
        self.y_val = y_val
        self.tile_list = tile_list


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
        self.player_list = []
        self.enemy_list = []


        ############## MAKE IMAGES ################
        # CLASSROOM
        # self.class_floor = pygame.image.load('Class_Floor.png').convert_alpha()
        # self.class_floor = pygame.transform.scale(self.class_floor, (self.block_size, self.block_size))

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
                    self.player = Student(x_val, y_val, self.tile_list, self.student_sheet)


    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])




