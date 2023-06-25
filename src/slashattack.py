from settings import *


class SlashAttack(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.player = player
        self.animation_sprites = []
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation1.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation2.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation3.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation4.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation5.png'))
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
