from assets import *


class SlashAttack(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.player = player
        self.animation_sprites = slash_attack_animation_sprites
        self.current_sprite = 0
        self.image = self.animation_sprites[0]
        self.rect = self.image.get_rect().move(self.player.rect.right - 150, self.player.rect.top - 70)
        self.damage = 10

    def animation(self):
        self.current_sprite += 0.5
        if self.current_sprite >= len(self.animation_sprites):
            self.kill()
        else:
            self.image = self.animation_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.right - 150, self.player.rect.top - 70)

    def update(self):
        self.animation()
