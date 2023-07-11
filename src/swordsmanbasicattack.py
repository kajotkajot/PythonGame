from assets import *


class SwordsmanBasicAttack(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.player = player
        self.animation_sprites = swordsman_basic_attack_animation_sprites
        self.current_sprite = 0
        self.image = self.animation_sprites[0]
        self.rect = self.image.get_rect().move(self.player.rect.right - 200, self.player.rect.top - 100)
        self.damage = 20

    def animation(self):
        self.current_sprite += 0.5
        if self.current_sprite >= len(self.animation_sprites):
            self.kill()
        else:
            self.image = self.animation_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.right - 200, self.player.rect.top - 100)

    def update(self):
        self.animation()
