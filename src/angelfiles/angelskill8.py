from src.assets import *
from src.angelfiles.angelskill9 import AngelSkill9


class AngelSkill8(pygame.sprite.Sprite):
    def __init__(self, player, group, attack_group, enemy_group, active):
        super().__init__(group)
        self.type = "active"
        self.player = player
        self.attack_group = attack_group
        self.enemy_group = enemy_group
        self.active = active
        self.current_sprite = 0
        self.animation_left_sprites = angel_left_resurrect_sprites
        self.animation_right_sprites = angel_right_resurrect_sprites
        self.image = self.animation_right_sprites[0]
        self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def animation_left(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.animation_left_sprites):
            self.player.channeling = False
            if self.player.explosion_on_death:
                skill9_timer = pygame.time.get_ticks()
                AngelSkill9(self.player, self.attack_group, self.enemy_group, skill9_timer)
            self.player.stats["health"] = self.player.stats["max_hp"] * self.player.stats["resurrection_value"]
            self.player.stats["resurrections"] -= 1
            self.player.resurrect_animation = False
            self.current_sprite = 0
        else:
            self.image = self.animation_left_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def animation_right(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.animation_right_sprites):
            self.player.channeling = False
            if self.player.explosion_on_death:
                skill9_timer = pygame.time.get_ticks()
                AngelSkill9(self.player, self.attack_group, self.enemy_group, skill9_timer)
            self.player.stats["health"] = self.player.stats["max_hp"] * self.player.stats["resurrection_value"]
            self.player.stats["resurrections"] -= 1
            self.player.resurrect_animation = False
            self.current_sprite = 0
        else:
            self.image = self.animation_right_sprites[int(self.current_sprite)]
            self.rect = self.image.get_rect().move(self.player.rect.x, self.player.rect.y)

    def check_orientation(self):
        if self.player.current_orientation == "left":
            self.animation_left()
        if self.player.current_orientation == "right":
            self.animation_right()

    def check_state(self):
        if self.player.stats["health"] <= 0 and self.player.stats["resurrections"] > 0:
            self.player.channeling = True
            self.player.resurrect_animation = True
            self.check_orientation()

    def update(self):
        if self.active:
            self.check_state()
