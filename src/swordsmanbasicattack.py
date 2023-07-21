from assets import *
from settings import *


class SwordsmanBasicAttack(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.player = player
        self.animation_sprites = swordsman_basic_attack_animation_sprites
        self.current_sprite = 0
        self.image = self.animation_sprites[0]
        self.rect = self.image.get_rect().move(self.player.rect.centerx - 0.75*PLAYER_WIDTH, self.player.rect.centery - 0.75*PLAYER_HEIGHT)
        self.damage = 20
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self):
        self.current_sprite += 0.5
        if self.current_sprite >= len(self.animation_sprites):
            self.kill()
        else:
            self.image = self.animation_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.centerx - 0.75*PLAYER_WIDTH, self.player.rect.centery - 0.75*PLAYER_HEIGHT)

    def update(self):
        self.animation()
