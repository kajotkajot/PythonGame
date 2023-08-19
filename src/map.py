import math
import numpy as np
from settings import *
from random import randint
from spritegroups import RoomGroup
from room import Room


class Map:
    def __init__(self):
        self.room_group = RoomGroup()
        self.sizes = np.random.normal(mean_size, stddev, square_count)
        self.main_rooms = np.random.normal(mean_size * 2, stddev * 2, main_count)
        self.sizes = np.clip(self.sizes, stddev, 2 * mean_size)

    def create_map(self):
        for room, x in zip(self.main_rooms, range(main_count)):
            step1 = math.sqrt(room)
            w_temp = step1 + randint(-10, 10)
            h_temp = step1 + randint(-10, 10)
            Room(self.room_group, int(w_temp), int(h_temp), True, False, False, x)

        for size in self.sizes:
            step1 = math.sqrt(size)
            w_temp = step1 + randint(-5, 5)
            h_temp = step1 + randint(-5, 5)
            Room(self.room_group, int(w_temp), int(h_temp), False, False, False, None)

    def update(self, player):
        self.room_group.create_map()
        self.room_group.custom_draw(player)
