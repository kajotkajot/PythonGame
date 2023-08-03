from src.assets import *


class AngelSkill9(pygame.sprite.Sprite):
    def __init__(self, player, group, enemy_group, timer):
        super().__init__(group)
        self.player = player
        self.enemy_group = enemy_group
        self.timer = timer
        self.damage = self.player.attack * self.player.character.skill9.current_value
        self.current_sprite = 0
        self.current_time = pygame.time.get_ticks()
        self.animation_left_sprites = self.player.character.player_left_explosion_sprites
        self.animation_right_sprites = self.player.character.player_right_explosion_sprites
        self.image = self.animation_right_sprites[0]
        self.shockwave_sprite = 0
        self.shockwave_sprites = angel_skill9_sprites
        self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)
        self.current_position = self.player.rect.topleft
        self.player.channeling = True
        self.mask = pygame.mask.from_surface(self.image)

    def animation_left(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.animation_left_sprites):
            self.player.channeling = False
            self.shockwave()
        else:
            self.image = self.animation_left_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)
            self.current_position = self.player.rect.topleft

    def animation_right(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.animation_right_sprites):
            self.player.channeling = False
            self.shockwave()
        else:
            self.image = self.animation_right_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)
            self.current_position = self.player.rect.topleft

    def shockwave(self):
        self.shockwave_sprite += 0.25
        if self.shockwave_sprite >= len(self.shockwave_sprites):
            self.kill()
        else:
            self.image = self.shockwave_sprites[int(self.shockwave_sprite)]
            image_size = self.image.get_width()/2 - 100
            self.rect = self.image.get_rect().move(self.current_position[0]-image_size, self.current_position[1]-image_size)
        self.check_collision()

    def check_orientation(self):
        if self.player.current_orientation == "left":
            self.animation_left()
        if self.player.current_orientation == "right":
            self.animation_right()

    def check_collision(self):
        for enemy in self.enemy_group:
            if self.rect.colliderect(enemy.rect):
                if self.mask.overlap(enemy.mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
                    enemy.hp -= self.damage*(1-((enemy.armor*self.player.armor_reduction)/((enemy.armor*self.player.armor_reduction)+99)))

    def update(self):
        self.check_orientation()
