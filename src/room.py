import pygame
import numpy as np


class Room(pygame.sprite.Sprite):
    def __init__(self, group, width, height, main_room, corridor, spawn_point, temp_id):
        super().__init__(group)
        self.id = temp_id
        self.spawn_point = spawn_point
        self.main = main_room
        self.corridor = corridor
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect().move((860, 440))
        self.position = pygame.Vector2(self.width+860, self.height+440)
        self.velocity = pygame.Vector2(np.random.uniform(-1, 1), np.random.uniform(-1, 1)).normalize() * 2
