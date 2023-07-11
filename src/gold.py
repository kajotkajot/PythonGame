from assets import *
import numpy as np


class Gold(pygame.sprite.Sprite):
    def __init__(self, position, group, player, gold_value):
        super().__init__(group)
        self.player = player
        self.image = gold
        self.value = gold_value
        self.shadow = item_shadow
        self.rect = position
        self.origin = pygame.Rect.copy(self.rect)
        self.origin.x -= 15
        self.origin.y -= 35
        self.rect.x -= 15
        self.rect.y -= 35
        self.magnet_speed = 0.1
        self.time = 0
        self.transparency = 255
        self.attracted = False

    def animation(self):
        if self.attracted is False:
            self.time += 0.06
            y = np.sin(1.1*self.time)*2
            self.rect.top -= y
            self.transparency -= 3.5*y
            self.shadow.set_alpha(self.transparency)

    def magnet(self):
        if abs(self.rect.center[0] - self.player.rect.center[0]) < 150 and abs(self.rect.center[1] - self.player.rect.center[1]) < 150:
            self.attracted = True
            x_range = abs(self.rect.center[0] - self.player.rect.center[0])
            y_range = abs(self.rect.center[1] - self.player.rect.center[1])
            x_speed = self.magnet_speed * x_range
            y_speed = self.magnet_speed * y_range
            self.magnet_speed += 0.05
            if self.rect.center[0] > self.player.rect.center[0] and self.rect.center[1] > self.player.rect.center[1]:
                self.rect.right -= x_speed
                self.rect.bottom -= y_speed
            if self.rect.center[0] > self.player.rect.center[0] and self.rect.center[1] < self.player.rect.center[1]:
                self.rect.right -= x_speed
                self.rect.top += y_speed
            if self.rect.center[0] < self.player.rect.center[0] and self.rect.center[1] > self.player.rect.center[1]:
                self.rect.left += x_speed
                self.rect.bottom -= y_speed
            if self.rect.center[0] < self.player.rect.center[0] and self.rect.center[1] < self.player.rect.center[1]:
                self.rect.left += x_speed
                self.rect.top += y_speed
            if self.rect.center[0] == self.player.rect.center[0] and self.rect.center[1] > self.player.rect.center[1]:
                self.rect.bottom -= y_speed
            if self.rect.center[0] == self.player.rect.center[0] and self.rect.center[1] < self.player.rect.center[1]:
                self.rect.top += y_speed
            if self.rect.center[0] > self.player.rect.center[0] and self.rect.center[1] == self.player.rect.center[1]:
                self.rect.right -= x_speed
            if self.rect.center[0] < self.player.rect.center[0] and self.rect.center[1] == self.player.rect.center[1]:
                self.rect.left += x_speed

    def collision(self):
        if self.rect.colliderect(self.player.rect):
            self.kill()
            self.player.player_gold += self.value

    def update(self):
        self.collision()
        self.magnet()
        self.animation()
