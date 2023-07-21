import math
from settings import *


class AngelSkill9(pygame.sprite.Sprite):
    def __init__(self, player, group, enemy_group, timer):
        super().__init__(group)
        self.player = player
        self.enemy_group = enemy_group
        self.timer = timer
        self.damage = 20
        self.current_sprite = 0
        self.current_time = pygame.time.get_ticks()
        self.animation_left_sprites = self.player.player_left_explosion_sprites
        self.animation_right_sprites = self.player.player_right_explosion_sprites
        self.image = self.animation_right_sprites[0]
        self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)
        self.player.channeling = True

    def animation_left(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.animation_left_sprites):
            self.player.channeling = False
            self.kill()
        else:
            self.image = self.animation_left_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def animation_right(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.animation_right_sprites):
            self.player.channeling = False
            self.kill()
        else:
            self.image = self.animation_right_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def check_orientation(self):
        if self.player.current_orientation == "left":
            self.animation_left()
        if self.player.current_orientation == "right":
            self.animation_right()

    def action(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > self.player.skill9_duration:
            self.player.channeling = False
            self.kill()

    def check_collision(self):
        for enemy in self.enemy_group:
            if math.hypot(self.player.rect.x - enemy.rect.x, self.player.rect.y - enemy.rect.y) <= 500:
                enemy.hp -= self.damage

    def update(self):
        self.action()
        self.check_orientation()
        self.check_collision()
