from enum import Enum
from copy import deepcopy
import random
import os
import pygame
import time
import math

from map import Map, Tile


class Game():

    fps = 60

    def __init__(self):
        self.map_width = 10
        self.map_height = 10
        self.map = Map(self.map_width, self.map_height)
        self.pos = self.map.start_pos

        print(self.map.string_rep(self.pos))

    def play(self):

        pygame.init()

        self.tile_size = 16

        self.display_width = (self.map_width) * self.tile_size
        self.display_height = (self.map_height + 1) * self.tile_size

        self.game_display = pygame.display.set_mode(
            (self.display_width, self.display_height))

        self.patterns = self.patterns()
        self.imgs_map = self.imgs_map()

        self.player_img = pygame.image.load('tiles/player.png')

        self.clock = pygame.time.Clock()

        while(True):
            self.game_loop()

    def patterns(self):

        # List of tiles which should always be drawn first.
        # All other tiles are assumed to be part of the 'foreground',
        # and are drawn after background tiles.
        self.background_tiles = []
        pats = {}

        self.floor_tile = pygame.image.load('tiles/floor_tile.png')
        floor_tile = self.floor_tile

        self.background_tiles.append(self.floor_tile)
        # FIRST PATTERN: Wall facing 'down'
        # ALL OTHER PATTERNS SHOULD OVERRIDE THIS ONE
        self.wall_tile = pygame.image.load('tiles/wall_tile.png')
        wall_tile = self.wall_tile

        self.black_tile = pygame.image.load('tiles/black_tile.png')
        black_tile = self.black_tile

        wall_pat = (
            (Tile.WALL,),
            (Tile.PATH,)
        )

        wall_imgs = (
            (
                (wall_tile,),
                (floor_tile,)
            ),
        )

        pats[wall_pat] = wall_imgs

        # SINGLETON PATTERN
        singleton_wall_pat = (
            (Tile.PATH, Tile.PATH, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.PATH, Tile.PATH))

        table_tile = pygame.image.load('tiles/table_tile.png')
        table_pc_tile = pygame.image.load('tiles/table_pc_tile.png')

        singleton_wall_imgs = (
            (
                (floor_tile, floor_tile, floor_tile),
                (floor_tile, table_pc_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile)),
            (
                (floor_tile, floor_tile, floor_tile),
                (floor_tile, table_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile)
            )
        )

        pats[singleton_wall_pat] = singleton_wall_imgs

        # 2x1 (Horiz) Pattern
        wall_2x1_pat = (
            (Tile.PATH, Tile.PATH, Tile.PATH, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.PATH, Tile.PATH, Tile.PATH))

        table_2x1_left_tile = pygame.image.load('tiles/2x1table_left.png')
        table_2x1_right_tile = pygame.image.load('tiles/2x1table_right.png')

        wall_2x1_imgs = (
            (
                (floor_tile, floor_tile, floor_tile, floor_tile),
                (floor_tile, table_2x1_left_tile,
                 table_2x1_right_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile, floor_tile)
            ),
        )

        pats[wall_2x1_pat] = wall_2x1_imgs

        # 1x2 (Vert) Pattern
        wall_1x2_pat = (
            (Tile.PATH, Tile.PATH, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.PATH, Tile.PATH)
        )

        table_1x2_top_tile = pygame.image.load('tiles/1x2table_top.png')
        table_1x2_bot_tile = pygame.image.load('tiles/1x2table_bot.png')

        plants_1x2_top_tile = pygame.image.load('tiles/1x2_plants_top.png')
        plants_1x2_bot_tile = pygame.image.load('tiles/1x2_plants_bot.png')

        wall_1x2_imgs = (
            (
                (floor_tile, floor_tile, floor_tile),
                (floor_tile, table_1x2_top_tile, floor_tile),
                (floor_tile, table_1x2_bot_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile, floor_tile)
            ),
            (
                (floor_tile, floor_tile, floor_tile),
                (floor_tile, plants_1x2_top_tile, floor_tile),
                (floor_tile, plants_1x2_bot_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile)
            )
        )

        pats[wall_1x2_pat] = wall_1x2_imgs

        # 2x2 Pattern
        wall_2x2_pat = (
            (Tile.PATH, Tile.PATH, Tile.PATH, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.PATH, Tile.PATH, Tile.PATH)
        )

        table1_2x2_topleft_tile = pygame.image.load(
            'tiles/2x2table1_topleft.png')
        table1_2x2_topright_tile = pygame.image.load(
            'tiles/2x2table1_topright.png')
        table1_2x2_botleft_tile = pygame.image.load(
            'tiles/2x2table1_botleft.png')
        table1_2x2_botright_tile = pygame.image.load(
            'tiles/2x2table1_botright.png')

        pingpong_topleft_tile = pygame.image.load('tiles/pingpong_topleft.png')
        pingpong_topright_tile = pygame.image.load(
            'tiles/pingpong_topright.png')
        pingpong_botleft_tile = pygame.image.load('tiles/pingpong_botleft.png')
        pingpong_botright_tile = pygame.image.load(
            'tiles/pingpong_botright.png')

        wall_2x2_imgs = (
            (
                (floor_tile, floor_tile, floor_tile, floor_tile),
                (floor_tile, table1_2x2_topleft_tile,
                 table1_2x2_topright_tile, floor_tile),
                (floor_tile, table1_2x2_botleft_tile,
                 table1_2x2_botright_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile, floor_tile)
            ),
            (
                (floor_tile, floor_tile, floor_tile, floor_tile),
                (floor_tile, pingpong_topleft_tile,
                 pingpong_topright_tile, floor_tile),
                (floor_tile, pingpong_botleft_tile,
                 pingpong_botright_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile, floor_tile)
            )
        )

        pats[wall_2x2_pat] = wall_2x2_imgs

        # L pattern
        L_botleft_tile = pygame.image.load('tiles/L_botleft.png')
        L_botright_tile = pygame.image.load('tiles/L_botright.png')
        L_topright_tile = pygame.image.load('tiles/L_topright.png')

        L_pat = (
            (Tile.PATH, Tile.PATH, Tile.PATH, Tile.PATH),
            (Tile.PATH, Tile.PATH, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.WALL, Tile.WALL, Tile.PATH),
            (Tile.PATH, Tile.PATH, Tile.PATH, Tile.PATH)
        )

        L_imgs = (
            (
                (floor_tile, floor_tile, floor_tile, floor_tile),
                (floor_tile, floor_tile, L_topright_tile, floor_tile),
                (floor_tile, L_botleft_tile, L_botright_tile, floor_tile),
                (floor_tile, floor_tile, floor_tile, floor_tile)
            ),
        )

        pats[L_pat] = L_imgs

        # Patterns have horizontal symmetry
        flipped_pats = {}
        lambda flip: x + 1
        def flip_pat(p): return tuple([tuple(reversed(row)) for row in p])

        def flip_imgs(i): return tuple(map(
            lambda i: flip_pat(
                tuple([
                    tuple([s if s == self.floor_tile else pygame.transform.flip(s, True, False) for s in row]) for row in i])), i))

        for pat in pats:
            flipped_pats[flip_pat(pat)] = flip_imgs(pats[pat])
        for flipped_pat in flipped_pats:
            pats[flipped_pat] = flipped_pats[flipped_pat]
        return pats

    def imgs_map(self):

        default_path_img = pygame.image.load('tiles/floor_tile.png')
        default_wall_img = pygame.image.load('tiles/black_tile.png')

        imgs_map = [[self.black_tile if self.map[(m, n)] == Tile.WALL else self.floor_tile for m in range(
            self.map_width)] for n in range(self.map_height)]

        for pat in self.patterns:
            pat_height = len(pat)
            pat_width = len(pat[0])
            for n in range(self.map_height - pat_height + 1):
                for m in range(self.map_width - pat_width + 1):
                    matches_pattern = True
                    for i in range(pat_height):
                        for j in range(pat_width):
                            if self.map[(m + j, n + i)] != pat[i][j]:
                                matches_pattern = False
                    if matches_pattern:
                        img_pat = self.patterns[pat][random.randint(
                            0, len(self.patterns[pat])-1)]
                        for i in range(pat_height):
                            for j in range(pat_width):
                                imgs_map[n+i][m+j] = img_pat[i][j]
        return imgs_map

    def game_loop(self):
        start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        black = (0, 0, 0)
        white = (255, 255, 255)

        self.game_display.fill(white)

        wall_img = self.wall_tile
        black_img = self.black_tile

        # Draw a bottom floor layer
        for n in range(self.map_width):
            for m in range(self.map_height):
                self.game_display.blit(
                    self.floor_tile, (n * self.tile_size, (m+1) * self.tile_size))

        # Draw a row of walls above the level
        for n in range(self.map_width):
            if(self.map[(n, 0)] == Tile.PATH):
                self.game_display.blit(wall_img, (self.tile_size * n, 0))
            else:
                self.game_display.blit(black_img, (self.tile_size * n, 0))

        # Movement + collision detection
        dirs = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0),
                pygame.K_DOWN: (0, 1), pygame.K_UP: (0, -1)}

        keys = pygame.key.get_pressed()
        moved = False

        offsets = {pygame.K_LEFT: (-0.1875, -0.375), pygame.K_RIGHT: (
            0.1875, -0.375), pygame.K_DOWN: (0, -0.375), pygame.K_UP: (0, -0.375)}

        def offset(c, o):
            return [c[i] + o[i] for i in range(2)]

        dt = self.clock.tick(60) * 0.005
        for key in dirs:
            if(not moved and keys[key]):
                try:
                    can_move = False
                    offset_pos = offset(self.pos, offsets[key])
                    next_pos = offset(offset_pos, list(
                        map(lambda x: x * dt, dirs[key])))
                    next_tile = list(map(math.floor, next_pos))
                    if(next_tile == list(map(math.floor, [self.pos[i] + offsets[key][i] for i in range(2)]))):
                        can_move = True
                    else:
                        if not (0 <= next_tile[1] < self.map.height and 0 <= next_tile[0] < self.map.width):
                            raise Game.IllegalMove
                        else:
                            if key in (pygame.K_LEFT, pygame.K_RIGHT):
                                if self.map[next_tile] != Tile.WALL:
                                    can_move = True
                            elif key in (pygame.K_DOWN, pygame.K_UP):
                                if(all([self.map[list(map(math.floor, [self.pos[i] + offsets[k][i] + dirs[key][i] * dt for i in range(2)]))] != Tile.WALL for k in (pygame.K_LEFT, pygame.K_RIGHT)])):
                                    can_move = True
                    if(can_move):
                        self.pos = [next_pos[i] - offsets[key][i]
                                    for i in range(2)]
                        moved = True
                except (KeyError, Game.IllegalMove):
                    break

        # Draw tiles and the player
        player_img = self.player_img
        player_img2 = pygame.image.load('tiles/player2.png')

        def draw_imgs(imgs_map, condition, draw_player):
            for n in range(self.map_height):
                for m in range(self.map_width):
                    coord = [m, n]
                    img = imgs_map[n][m]
                    if condition(img):
                        self.game_display.blit(
                            imgs_map[n][m], ((m) * self.tile_size, (n+1) * self.tile_size))
                    if(draw_player):
                        if(coord[0] == 0 and math.floor(self.pos[1]) == coord[1]):
                            self.game_display.blit(player_img, [(
                                self.pos[0] - 0.4375) * self.tile_size, (self.pos[1] - 1.625 + 1) * self.tile_size])

        draw_imgs(self.imgs_map, lambda x: x in self.background_tiles, False)
        draw_imgs(self.imgs_map, lambda x: not x in self.background_tiles, True)

        pygame.display.update()

        end = time.time()
        # print(end-start)

    class IllegalMove(Exception):
        pass

    def move(self):
        i = input("")

        dirs = {"a": (0, -1), "d": (0, 1), "s": (1, 0), "w": (-1, 0)}
