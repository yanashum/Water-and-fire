import pygame
import random
from water import water
from node import Node
from enums.algorithm import Algorithm


class Friend:
    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    TILE_SIZE = 4

    def __init__(self, x, y, alg):
        self.life = True
        self.path = []
        self.movement_path = []
        self.pos_x = x * Friend.TILE_SIZE
        self.pos_y = y * Friend.TILE_SIZE
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.range = 3
        self.barrel_limit = 1
        self.plant = False
        self.algorithm = alg

    def move(self, map, barrels, Put_out_firess, friend):

        if self.direction == 0:
            self.pos_y += 1
        elif self.direction == 1:
            self.pos_x += 1
        elif self.direction == 2:
            self.pos_y -= 1
        elif self.direction == 3:
            self.pos_x -= 1

        if self.pos_x % Friend.TILE_SIZE == 0 and self.pos_y % Friend.TILE_SIZE == 0:
            self.movement_path.pop(0)
            self.path.pop(0)
            if len(self.path) > 1:
                grid = self.create_grid(map, barrels, Put_out_firess, friend)
                next = self.path[1]
                if grid[next[0]][next[1]] > 1:
                    self.movement_path.clear()
                    self.path.clear()

        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1

    def make_move(self, map, barrels, Put_out_firess, friend):

        if not self.life:
            return
        if len(self.movement_path) == 0:
            if self.plant:
                barrels.append(self.plant_water(map))
                self.plant = False
                map[int(self.pos_x / Friend.TILE_SIZE)][int(self.pos_y / Friend.TILE_SIZE)] = 3
            if self.algorithm is Algorithm.friend_2:
                self.friend_2(self.create_grid(map, barrels, Put_out_firess, friend))
            else:
                self.friend_1(self.create_grid_friend_1(map, barrels, Put_out_firess, friend))

        else:
            self.direction = self.movement_path[0]
            self.move(map, barrels, Put_out_firess, friend)

    def plant_water(self, map):
        b = water(self.range, round(self.pos_x / Friend.TILE_SIZE), round(self.pos_y / Friend.TILE_SIZE), map, self)
        self.barrel_limit -= 1
        return b

    def check_death(self, exp):

        for e in exp:
            for s in e.sectors:
                if int(self.pos_x / Friend.TILE_SIZE) == s[0] and int(self.pos_y / Friend.TILE_SIZE) == s[1]:
                    self.life = False
                    return

    def friend_2(self, grid):

        new_path = [[int(self.pos_x / Friend.TILE_SIZE), int(self.pos_y / Friend.TILE_SIZE)]]
        depth = 0
        if self.barrel_limit == 0:
            self.friend_2_rec(grid, 0, new_path, depth)
        else:
            self.friend_2_rec(grid, 2, new_path, depth)

        self.path = new_path

    def friend_2_rec(self, grid, end, path, depth):

        last = path[-1]
        if depth > 200:
            return
        if grid[last[0]][last[1]] == 0 and end == 0:
            return
        elif end == 2:
            if grid[last[0] + 1][last[1]] == end or grid[last[0] - 1][last[1]] == end \
                    or grid[last[0]][last[1] + 1] == end \
                    or grid[last[0]][last[1] - 1] == end:
                if len(path) == 1 and end == 2:
                    self.plant = True
                return

        grid[last[0]][last[1]] = 9

        random.shuffle(self.dire)

        # safe
        if grid[last[0] + self.dire[0][0]][last[1] + self.dire[0][1]] == 0:
            path.append([last[0] + self.dire[0][0], last[1] + self.dire[0][1]])
            self.movement_path.append(self.dire[0][2])
        elif grid[last[0] + self.dire[1][0]][last[1] + self.dire[1][1]] == 0:
            path.append([last[0] + self.dire[1][0], last[1] + self.dire[1][1]])
            self.movement_path.append(self.dire[1][2])
        elif grid[last[0] + self.dire[2][0]][last[1] + self.dire[2][1]] == 0:
            path.append([last[0] + self.dire[2][0], last[1] + self.dire[2][1]])
            self.movement_path.append(self.dire[2][2])
        elif grid[last[0] + self.dire[3][0]][last[1] + self.dire[3][1]] == 0:
            path.append([last[0] + self.dire[3][0], last[1] + self.dire[3][1]])
            self.movement_path.append(self.dire[3][2])

        # unsafe
        elif grid[last[0] + self.dire[0][0]][last[1] + self.dire[0][1]] == 1:
            path.append([last[0] + self.dire[0][0], last[1] + self.dire[0][1]])
            self.movement_path.append(self.dire[0][2])
        elif grid[last[0] + self.dire[1][0]][last[1] + self.dire[1][1]] == 1:
            path.append([last[0] + self.dire[1][0], last[1] + self.dire[1][1]])
            self.movement_path.append(self.dire[1][2])
        elif grid[last[0] + self.dire[2][0]][last[1] + self.dire[2][1]] == 1:
            path.append([last[0] + self.dire[2][0], last[1] + self.dire[2][1]])
            self.movement_path.append(self.dire[2][2])
        elif grid[last[0] + self.dire[3][0]][last[1] + self.dire[3][1]] == 1:
            path.append([last[0] + self.dire[3][0], last[1] + self.dire[3][1]])
            self.movement_path.append(self.dire[3][2])
        else:
            if len(self.movement_path) > 0:
                path.pop(0)
                self.movement_path.pop(0)
        depth += 1
        self.friend_2_rec(grid, end, path, depth)

    def friend_1(self, grid):

        end = 1
        if self.barrel_limit == 0:
            end = 0

        visited = []
        open_list = []
        current = grid[int(self.pos_x / Friend.TILE_SIZE)][int(self.pos_y / Friend.TILE_SIZE)]
        current.weight = current.base_weight
        new_path = []
        while True:
            visited.append(current)
            random.shuffle(self.dire)
            if (current.value == end and end == 0) or \
                    (end == 1 and (
                            grid[current.x + 1][current.y].value == 1 or grid[current.x - 1][current.y].value == 1 or
                            grid[current.x][current.y + 1].value == 1 or grid[current.x][current.y - 1].value == 1)):
                new_path.append([current.x, current.y])
                while True:
                    if current.parent is None:
                        break
                    current = current.parent
                    new_path.append([current.x, current.y])
                new_path.reverse()
                for xd in range(len(new_path)):
                    if new_path[xd] is not new_path[-1]:
                        if new_path[xd][0] - new_path[xd + 1][0] == -1:
                            self.movement_path.append(1)
                        elif new_path[xd][0] - new_path[xd + 1][0] == 1:
                            self.movement_path.append(3)
                        elif new_path[xd][1] - new_path[xd + 1][1] == -1:
                            self.movement_path.append(0)
                        elif new_path[xd][1] - new_path[xd + 1][1] == 1:
                            self.movement_path.append(2)
                if len(new_path) == 1 and end == 1:
                    self.plant = True
                self.path = new_path
                return

            for i in range(len(self.dire)):
                if current.x + self.dire[i][0] < len(grid) and current.y + self.dire[i][1] < len(grid):
                    if grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].reach \
                            and grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]] not in visited:
                        if grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]] in open_list:
                            if grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].weight > \
                                    grid[current.x][current.y].weight \
                                    + grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].base_weight:
                                grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].parent = current
                                grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].weight = current.weight + \
                                                                                                        grid[current.x +
                                                                                                             self.dire[
                                                                                                                 i][0]][
                                                                                                            current.y +
                                                                                                            self.dire[
                                                                                                                i][
                                                                                                                1]].base_weight
                                grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].direction = self.dire[i][
                                    2]

                        else:
                            grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].parent = current
                            grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].weight = \
                                current.weight + grid[current.x + self.dire[i][0]][
                                    current.y + self.dire[i][1]].base_weight
                            grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]].direction = self.dire[i][2]
                            open_list.append(grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]])

            if len(open_list) == 0:
                self.path = [[int(self.pos_x / Friend.TILE_SIZE), int(self.pos_y / Friend.TILE_SIZE)]]
                return

            next_node = open_list[0]
            for n in open_list:
                if n.weight < next_node.weight:
                    next_node = n
            open_list.remove(next_node)
            current = next_node

    def create_grid(self, map, barrels, Put_out_firess, friends):
        grid = [[0] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - unsafe
        # 2 - destryable
        # 3 - unreachable

        for b in barrels:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]] = 1
            grid[b.pos_x][b.pos_y] = 3

        for e in Put_out_firess:
            for s in e.sectors:
                grid[s[0]][s[1]] = 3

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    grid[i][j] = 3
                elif map[i][j] == 2:
                    grid[i][j] = 2

        for x in friends:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                grid[int(x.pos_x / Friend.TILE_SIZE)][int(x.pos_y / Friend.TILE_SIZE)] = 2

        return grid

    def create_grid_friend_1(self, map, barrels, Put_out_firess, friends):
        grid = [[None] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - destroyable
        # 2 - unreachable
        # 3 - unsafe
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    grid[i][j] = Node(i, j, True, 1, 0)
                elif map[i][j] == 2:
                    grid[i][j] = Node(i, j, False, 999, 1)
                elif map[i][j] == 1:
                    grid[i][j] = Node(i, j, False, 999, 2)
                elif map[i][j] == 3:
                    grid[i][j] = Node(i, j, False, 999, 2)

        for b in barrels:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]].weight = 5
                grid[x[0]][x[1]].value = 3
            grid[b.pos_x][b.pos_y].reach = False

        for e in Put_out_firess:
            for s in e.sectors:
                grid[s[0]][s[1]].reach = False

        for x in friends:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                grid[int(x.pos_x / Friend.TILE_SIZE)][int(x.pos_y / Friend.TILE_SIZE)].reach = False
                grid[int(x.pos_x / Friend.TILE_SIZE)][int(x.pos_y / Friend.TILE_SIZE)].value = 1
        return grid

    def load_animations(self, en, scale):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        image_path = 'images/Friend/e'
        if en == '':
            image_path = 'images/hero/p'

        f1 = pygame.image.load(image_path + en + 'f0.png')
        f2 = pygame.image.load(image_path + en + 'f1.png')
        f3 = pygame.image.load(image_path + en + 'f2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load(image_path + en + 'r0.png')
        r2 = pygame.image.load(image_path + en + 'r1.png')
        r3 = pygame.image.load(image_path + en + 'r2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load(image_path + en + 'b0.png')
        b2 = pygame.image.load(image_path + en + 'b1.png')
        b3 = pygame.image.load(image_path + en + 'b2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load(image_path + en + 'l0.png')
        l2 = pygame.image.load(image_path + en + 'l1.png')
        l3 = pygame.image.load(image_path + en + 'l2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)
