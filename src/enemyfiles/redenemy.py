import math
from src.assets import *
from random import randint
from src.itemfiles.health import Health
from src.itemfiles.gold import Gold
from src.itemfiles.armor import Armor
from src.itemfiles.attackdamage import AttackDamage
from src.itemfiles.healthpotion import HealthPotion


class RedEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_cords, enemy_group, dead_enemy_group, attack_group, item_group, player, stats):
        super().__init__(enemy_group)
        self.enemy_group = enemy_group
        self.dead_enemy_group = dead_enemy_group
        self.attack_group = attack_group
        self.item_group = item_group
        self.player = player
        self.stats = stats
        self.hp = self.stats["health"]
        self.max_hp = self.stats["health"]
        self.speed = self.stats["speed"]
        self.damage = self.stats["attack"]
        self.armor = self.stats["armor"]
        self.image = red_enemy_right
        self.rect = self.image.get_rect().move(enemy_cords[0], enemy_cords[1])
        self.red_enemy_left_sprites = red_enemy_left_sprites
        self.red_enemy_right_sprites = red_enemy_right_sprites
        self.red_enemy_left_death_sprites = red_enemy_left_death_sprites
        self.red_enemy_right_death_sprites = red_enemy_right_death_sprites
        self.red_enemy_left_attack_sprites = red_enemy_left_attack_sprites
        self.red_enemy_right_attack_sprites = red_enemy_right_attack_sprites
        self.current_death_sprite = 0
        self.current_sprite = 0
        self.current_orientation = "right"
        self.hit_box = self.rect
        self.mass = 1
        self.restitution = 0.8
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.current_orientation == "right":
            self.move_right()
        if self.current_orientation == "left":
            self.move_left()
        self.move_def()

    def move_right(self):
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.red_enemy_right_sprites):
            self.current_sprite = 0
        self.image = self.red_enemy_right_sprites[int(self.current_sprite)]

    def move_left(self):
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.red_enemy_left_sprites):
            self.current_sprite = 0
        self.image = self.red_enemy_left_sprites[int(self.current_sprite)]

    def move_def(self):
        x_range = self.player.rect.centerx - self.rect.centerx
        y_range = self.player.rect.centery - self.rect.centery
        xy_range = math.hypot(x_range, y_range)
        if xy_range != 0:
            x_range /= xy_range*15
            y_range /= xy_range*15
        x_speed = self.speed * x_range
        y_speed = self.speed * y_range
        self.rect.x += x_speed
        self.rect.y += y_speed
        if self.rect.centerx > self.player.rect.centerx:
            self.current_orientation = "left"
        if self.rect.centerx < self.player.rect.centerx:
            self.current_orientation = "right"

    def detect_collision(self):
        if self.rect.colliderect(self.player.rect):
            if self.mask.overlap(self.player.mask, (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)) and self.player.resurrect_animation is False and self.player.channeling is False:
                self.hp -= self.damage * self.player.damage_bounce
                self.player.current_hp -= self.damage * (1-(self.player.armor/(self.player.armor+99))) * self.player.damage_reduction
                if self.current_orientation == "right":
                    self.right_attack_animation()
                if self.current_orientation == "left":
                    self.left_attack_animation()
        if not self.mask.overlap(self.player.mask, (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)):
            self.move()

    def left_attack_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.red_enemy_left_attack_sprites):
            self.current_sprite = 0
        self.image = self.red_enemy_left_attack_sprites[int(self.current_sprite)]

    def right_attack_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.red_enemy_right_attack_sprites):
            self.current_sprite = 0
        self.image = self.red_enemy_right_attack_sprites[int(self.current_sprite)]

    def left_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_left_death_sprites):
            self.kill()
            self.drop_loot()
        else:
            self.image = self.red_enemy_left_death_sprites[int(self.current_death_sprite)]

    def right_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_right_death_sprites):
            self.kill()
            self.drop_loot()
        else:
            self.image = self.red_enemy_right_death_sprites[int(self.current_death_sprite)]

    def death_check(self):
        if self.current_orientation == "right":
            self.right_death_animation()
        if self.current_orientation == "left":
            self.left_death_animation()

    def drop_loot(self):
        x = randint(0, 99)
        if x <= 10:
            Health(self.rect, self.item_group, self.player)
        elif 10 < x <= 20:
            Gold(self.rect, self.item_group, self.player, randint(10, 20))
        elif 20 < x <= 30:
            Armor(self.rect, self.item_group, self.player, 1)
        elif 30 < x <= 40:
            AttackDamage(self.rect, self.item_group, self.player, 1)
        elif 40 < x <= 50:
            HealthPotion(self.rect, self.item_group, self.player)

    def is_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.enemy_group.remove(self)
            self.dead_enemy_group.add(self)
            self.player.xp += self.stats["xp"]

    def update(self):
        self.is_alive()
        self.detect_collision()
