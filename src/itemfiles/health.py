import math
import numpy as np
from src.assets import *


class Health(pygame.sprite.Sprite):
    def __init__(self, position, group, player):
        super().__init__(group)
        self.player = player
        self.image = health
        self.value = 10
        self.shadow = item_shadow
        self.rect = position
        self.origin = pygame.Rect.copy(self.rect)
        self.origin.x -= 15
        self.origin.y -= 35
        self.rect.x -= 15
        self.rect.y -= 35
        self.magnet_speed = 15
        self.time = 0
        self.transparency = 255
        self.attracted = False
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self):
        self.time += 0.06
        y = np.sin(1.1*self.time)*2
        self.rect.top -= y
        self.transparency -= 3.5*y
        self.shadow.set_alpha(self.transparency)

    def magnet(self):
        if abs(self.rect.center[0] - self.player.rect.center[0]) < 150 and abs(self.rect.center[1] - self.player.rect.center[1]) < 150 and self.player.alive and self.player.resurrect_animation is False:
            self.attracted = True
            x_range = self.player.rect.centerx - self.rect.centerx
            y_range = self.player.rect.centery - self.rect.centery
            xy_range = math.hypot(x_range, y_range)
            if xy_range != 0:
                x_range /= xy_range
                y_range /= xy_range
            x_speed = self.magnet_speed * x_range
            y_speed = self.magnet_speed * y_range
            self.rect.x += x_speed
            self.rect.y += y_speed

    def collision(self):
        if self.rect.colliderect(self.player.rect) and self.player.alive and self.player.resurrect_animation is False:
            if self.mask.overlap(self.player.mask, (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)):
                self.kill()
                self.player.stats["max_hp"] += self.value * self.player.character.skill2.current_value

    def update(self):
        self.collision()
        self.magnet()
        self.animation()
