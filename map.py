from enum import Enum
from copy import deepcopy
import random
import os
import pygame
import time
import math


class Tile(Enum):
    PATH = 0
    WALL = 1

    def __str__(self):
        if self == Tile.PATH:
            return "██"
        elif self == Tile.WALL:
            return "  "

    def __repr__(self):
        return str(self)


class Map():
    def __init__(self, w, h):
        self.width = w
        self.height = h

        self.start_pos = [0.5, 0.5]

        self.open_space_tolerance = random.randint(1, 75)
        self.closed_space_tolerance = random.randint(0, 15)
        self.disjoint_tolerance = random.randint(1, 50)

        self.tiles = self.generate()

    def done(self, tiles):
        adjs = [(n-1, m-1) for n in range(3)
                for m in range(3) if (n-1) != 0 or (m-1) != 0]
        done = True
        for r in range(len(tiles)):
            for c in range(len(tiles[r])):
                adj_to_path = False
                for adj in adjs:
                    if(r+adj[0] >= 0 and c+adj[1] >= 0):
                        try:
                            if tiles[r+adj[0]][c+adj[1]] == Tile.PATH:
                                adj_to_path = True
                                break
                        except IndexError:
                            adj_to_path = True
                            break
                        if(random.randint(0, 100) < self.closed_space_tolerance):
                            adj_to_path = True
                            break
                if not (tiles[r][c] == Tile.PATH or adj_to_path):
                    done = False
        return done

    def is_legal_path(self, tiles, pos):
        corners = [[(1, 1), (1, 0), (0, 1)],
                   [(1, -1), (1, 0), (0, -1)],
                   [(-1, 1), (-1, 0), (0, 1)],
                   [(-1, -1), (-1, 0), (0, -1)]]

        adjs = [(1, 0), (-1, 0), (0, 1), (-1, 0)]

        for i in range(len(corners)):
            for p in range(len(corners[i])):
                x, y = corners[i][p]
                x += pos[0]
                y += pos[1]
                corners[i][p] = (x, y)

        for a in range(len(adjs)):
            x, y = adjs[a]
            x += pos[0]
            y += pos[1]
            adjs[a] = (x, y)

        legal = True

        for c in corners:
            if(all(map(lambda x: tiles[x[0]][x[1]] == Tile.PATH if (0 <= x[0] < self.height and 0 <= x[1] < self.width) else False, c))):
                if(random.randint(0, 100) > self.open_space_tolerance):
                    legal = False
                    break
            else:
                try:
                    if(tiles[c[0][0]][c[0][1]] == Tile.PATH and tiles[c[1][0]][c[1][1]] == Tile.WALL and tiles[c[2][0]][c[2][1]] == Tile.WALL):
                        legal = False
                        break
                except IndexError:
                    pass

        if legal and (all(map(lambda x: not (tiles[x[0]][x[1]] == Tile.PATH if (0 <= x[0] < self.height and 0 <= x[1] < self.width) else True), adjs))):
            if(random.randint(0, 100) > self.disjoint_tolerance):
                legal = False

        if(0 <= pos[0] < self.height and 0 <= pos[1] < self.width):
            return legal
        else:
            return False

    def generate(self):

        init = [[Tile.WALL for n in range(self.width)]
                for m in range(self.height)]

        done = False
        tpos = list(map(math.floor, (reversed(self.start_pos))))
        # print(tpos)
        std_dirs = ((0, -1), (0, 1), (1, 0), (-1, 0))

        tdir = (0, 0)
        same_dir_weight = 3

        no_new_path_cnt = 0
        while(not self.done(init)):
            if(random.randint(0, 25) == 25):
                same_dir_weight = random.randint(0, 6)
            weighted_dirs = list(std_dirs) + \
                [tdir for n in range(same_dir_weight)]
            s = ""
            for row in init:
                s += "".join(map(str, row))
                s += "\n"

            s += "Open Space Tolerance: " + \
                str(self.open_space_tolerance) + "\n"
            s += "Closed Space Tolerance: " + \
                str(self.closed_space_tolerance) + "\n"
            s += "Disjoint Tolerance: " + str(self.disjoint_tolerance) + "\n"

            # os.system('clear')
            # print(s)
            init[tpos[0]][tpos[1]] = Tile.PATH
            opts = ([(tpos[0] + n, tpos[1] + m) for n, m in weighted_dirs])
            random.shuffle(opts)

            new_path = False
            # print(no_new_path_cnt)
            for tile in opts:
                if self.is_legal_path(init, tile) and init[tile[0]][tile[1]] == Tile.WALL:
                    new_path = True
                    tdir = (tile[0] - tpos[0], tile[1] - tpos[1])
                    tpos = tile
                    no_new_path_cnt = 0
                    break
            # print(new_path)
            if not new_path:
                if no_new_path_cnt < 10:
                    for tile in opts:
                        try:
                            if init[tile[0]][tile[1]] == Tile.PATH:
                                tpos = tile
                                no_new_path_cnt += 1
                                tdir = (0, 0)
                                break
                        except IndexError:
                            continue
                else:
                    teleported = False
                    illegals = []
                    while(not teleported):
                        teleport_to = (random.randint(
                            0, self.height), random.randint(0, self.width))
                        if teleport_to in illegals:
                            pass
                        elif not self.is_legal_path(init, teleport_to):
                            illegals += [teleport_to]
                        else:
                            tpos = teleport_to
                            teleported = True
                            no_new_path_cnt = 0
                            tdir = (0, 0)
        return init

    def __getitem__(self, t):
        return self.tiles[t[1]][t[0]]

    def string_rep(self, pos):
        s = ""
        t = deepcopy(self.tiles)
        t[math.floor(pos[1])][math.floor(pos[0])] = "▒▒"
        for row in t:
            s += "".join(map(str, row))
            s += "\n"

        s += "Open Space Tolerance: " + str(self.open_space_tolerance) + "\n"
        s += "Closed Space Tolerance: " + \
            str(self.closed_space_tolerance) + "\n"
        s += "Disjoint Tolerance: " + str(self.disjoint_tolerance) + "\n"

        return s
