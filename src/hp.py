from settings import *
from assets import *
import numpy as np


class Hp(pygame.sprite.Sprite):
    def __init__(self, position, group, player):
        super().__init__(group)
        self.player = player
        self.image = hp_heart
        self.value = hp_value
        self.shadow = hp_heart_shadow
        self.rect = position
        self.origin = pygame.Rect.copy(self.rect)
        self.origin.x -= 15
        self.origin.y -= 35
        self.rect.x -= 15
        self.rect.y -= 35
        self.time = 0
        self.transparency = 255

    def animation(self):
        self.time += 0.06
        y = np.sin(1.1*self.time)*2
        self.rect.top -= y
        self.transparency -= 3.5*y
        self.shadow.set_alpha(self.transparency)

    def collision(self):
        if self.rect.colliderect(self.player.rect):
            self.kill()
            self.player.player_hp += self.value

    def update(self):
        self.collision()
        self.animation()
