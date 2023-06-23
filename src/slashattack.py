from settings import *


# slash attack class
class SlashAttack:
    def __init__(self, player):
        self.animation_sprites = []
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation1.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation2.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation3.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation4.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation5.png'))
        self.current_sprite = 0
        self.image = self.animation_sprites[0]
        self.pos = self.image.get_rect().move(player.pos.right - 150, player.pos.top - 70)
        self.damage = 10

    def animation(self, player):
        self.current_sprite += 0.5
        if self.current_sprite >= len(self.animation_sprites):
            attacks.remove(self)
        else:
            self.image = self.animation_sprites[int(self.current_sprite)]
            self.pos = self.image.get_rect().move(player.pos.right - 150, player.pos.top - 70)
        screen.blit(self.image, self.pos)

    def update(self, player):
        self.animation(player)
