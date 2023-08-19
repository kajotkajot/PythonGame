from src.settings import *


class AngelBasic(pygame.sprite.Sprite):
    def __init__(self, player, group, enemy_group):
        super().__init__(group)
        self.player = player
        self.enemy_group = enemy_group
        self.animation_left_sprites = self.player.character.player_left_basic_attack_sprites
        self.animation_right_sprites = self.player.character.player_right_basic_attack_sprites
        self.current_sprite = 0
        self.image = self.animation_right_sprites[0]
        self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)
        self.damage = self.player.stats["attack"]
        self.player.basic_attack_animation = True
        self.mask = pygame.mask.from_surface(self.image)

    def animation_left(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.animation_left_sprites):
            self.player.basic_attack_animation = False
            self.kill()
        else:
            self.image = self.animation_left_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def animation_right(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.animation_right_sprites):
            self.player.basic_attack_animation = False
            self.kill()
        else:
            self.image = self.animation_right_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def check_orientation(self):
        if self.player.current_orientation == "left":
            self.animation_left()
        if self.player.current_orientation == "right":
            self.animation_right()

    def check_collision(self):
        for enemy in self.enemy_group:
            if self.rect.colliderect(enemy.rect):
                if self.mask.overlap(enemy.mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
                    enemy.stats["health"] -= self.damage*(1-((enemy.stats["armor"]*self.player.stats["armor_reduction"])/((enemy.stats["armor"]*self.player.stats["armor_reduction"])+99)))

    def update(self):
        self.check_orientation()
        self.check_collision()
