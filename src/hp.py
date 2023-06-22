from settings import *
import numpy as np


# hp class
class Hp:
    def __init__(self, position):
        self.image = hp_heart
        self.value = hp_value
        self.shadow = hp_heart_shadow
        self.pos = position
        self.origin = pygame.Rect.copy(self.pos)
        self.origin.top -= 15
        self.pos.top -= 15
        self.time = 0
        self.transparency = 255

    def animation(self):
        self.time += 0.06
        y = np.sin(1.1*self.time)*2
        self.pos.top -= y
        self.transparency -= 3.5*y
        self.shadow.set_alpha(self.transparency)
        screen.blit(self.shadow, self.origin)
        screen.blit(self.image, self.pos)

    def collision(self, player):
        if self.pos.colliderect(player.pos):
            hp_list.remove(self)
            player.player_hp += self.value

    def update(self, player):
        self.collision(player)
        self.animation()
