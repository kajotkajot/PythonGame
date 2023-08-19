import math
import numpy as np
from src.assets import *
from random import randint
from src.itemfiles.health import Health
from src.itemfiles.gold import Gold
from src.itemfiles.armor import Armor
from src.itemfiles.attackdamage import AttackDamage
from src.itemfiles.healthpotion import HealthPotion


class GreenEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_cords, enemy_group, dead_enemy_group, attack_group, item_group, player, stats):
        super().__init__(enemy_group)
        self.enemy_group = enemy_group
        self.dead_enemy_group = dead_enemy_group
        self.attack_group = attack_group
        self.item_group = item_group
        self.player = player
        self.stats = {key: value for key, value in stats.items()}
        self.speed = self.stats["speed"]
        self.image = green_enemy_right
        self.rect = self.image.get_rect().move(enemy_cords[0], enemy_cords[1])
        self.origin_position = self.rect.center
        self.green_enemy_left_sprites = green_enemy_left_sprites
        self.green_enemy_right_sprites = green_enemy_right_sprites
        self.green_enemy_left_death_sprites = green_enemy_left_death_sprites
        self.green_enemy_right_death_sprites = green_enemy_right_death_sprites
        self.green_enemy_left_blow_sprites = green_enemy_left_blow_sprites
        self.green_enemy_right_blow_sprites = green_enemy_right_blow_sprites
        self.current_sprite = 0
        self.current_orientation = "right"
        self.current_direction = "none"
        self.timer = 0
        self.x_range = 0.3
        self.y_range = 0.3
        self.hit_box = self.rect
        self.mass = 1
        self.restitution = 0.8
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_timer = np.random.uniform(75, 125)
        self.going_back = False
        self.going_back_timer = 0

    def move(self):
        if self.current_orientation == "right":
            self.image = self.green_enemy_right_sprites[1]
        if self.current_orientation == "left":
            self.image = self.green_enemy_left_sprites[1]
        self.move_def()

    def move_def(self):
        x_speed = (self.speed * self.x_range) / 3
        y_speed = (self.speed * self.y_range) / 4
        if self.current_direction == "top-left":
            self.rect.right -= x_speed
            self.rect.top -= y_speed
            self.current_orientation = "left"
        if self.current_direction == "bottom-left":
            self.rect.right -= x_speed
            self.rect.top += y_speed
            self.current_orientation = "left"
        if self.current_direction == "top-right":
            self.rect.right += x_speed
            self.rect.top -= y_speed
            self.current_orientation = "right"
        if self.current_direction == "bottom-right":
            self.rect.right += x_speed
            self.rect.top += y_speed
            self.current_orientation = "right"
        if self.current_direction == "top":
            self.rect.top -= y_speed
        if self.current_direction == "bottom":
            self.rect.top += y_speed
        if self.current_direction == "left":
            self.rect.right -= x_speed
            self.current_orientation = "left"
        if self.current_direction == "right":
            self.rect.right += x_speed
            self.current_orientation = "right"

    def stand_right(self):
        self.speed = 0
        self.image = self.green_enemy_right_sprites[0]

    def stand_left(self):
        self.speed = 0
        self.image = self.green_enemy_left_sprites[0]

    def is_alive(self):
        if self.stats["health"] <= 0:
            self.stats["health"] = 0
            if self in self.enemy_group:
                self.enemy_group.remove(self)
                self.dead_enemy_group.add(self)
            self.player.xp += self.stats["xp"]

    def wait(self):
        if self.going_back_timer < 60:
            self.going_back_timer += 1
        else:
            self.going_back = True

    def move_back(self):
        x_range = self.origin_position[0] - self.rect.centerx
        y_range = self.origin_position[1] - self.rect.centery
        xy_range = math.hypot(x_range, y_range)
        if xy_range != 0:
            x_range /= xy_range*15
            y_range /= xy_range*15
        x_speed = self.stats["speed"] / 2.5 * x_range
        y_speed = self.stats["speed"] / 2.5 * y_range
        self.rect.x += x_speed
        self.rect.y += y_speed
        if self.rect.centerx > self.origin_position[0]:
            self.current_orientation = "left"
        if self.rect.centerx < self.origin_position[0]:
            self.current_orientation = "right"

    def detect_collision(self):
        if self.rect.colliderect(self.player.rect) and not self.speed == 0:
            if self.mask.overlap(self.player.mask, (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)) and self.player.resurrect_animation is False and self.player.channeling is False:
                self.player.stats["health"] -= self.stats["attack"] * (1-(self.player.stats["armor"]/(self.player.stats["armor"]+99))) * self.player.stats["damage_reduction"]
                if self in self.enemy_group:
                    self.enemy_group.remove(self)
                    self.dead_enemy_group.add(self)
                self.rect.top -= 20
        if not self.mask.overlap(self.player.mask, (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)):
            if math.hypot(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery) <= 750:
                self.move()
            else:
                if not self.origin_position[0]-5 <= self.rect.centerx <= self.origin_position[0]+5 and not self.origin_position[1]-5 <= self.rect.centery <= self.origin_position[1]+5:
                    if self.going_back:
                        self.move_back()
                    else:
                        self.wait()
                else:
                    self.going_back = False
                    self.going_back_timer = 0
        self.speed -= self.timer
        self.timer += 1.5
        if self.speed <= 0:
            if self.current_orientation == "right":
                self.stand_right()
            if self.current_orientation == "left":
                self.stand_left()
        if self.timer >= self.jump_timer:
            self.check_direction()
            self.timer = 0

    def check_direction(self):
        self.x_range = (abs(self.rect.centerx - self.player.rect.centerx) + abs(self.rect.centerx - self.player.rect.centerx)) / 2000
        if self.x_range >= 0.6:
            self.x_range = 0.6
        self.y_range = (abs(self.rect.centery - self.player.rect.centery) + abs(self.rect.centery - self.player.rect.centery)) / 2000
        if self.y_range >= 0.6:
            self.y_range = 0.6
        self.speed = self.stats["speed"]
        if self.rect.centerx > self.player.rect.centerx:
            if self.rect.centery > self.player.rect.centery:
                self.current_direction = "top-left"
            if self.rect.centery < self.player.rect.centery:
                self.current_direction = "bottom-left"
            if self.rect.centery == self.player.rect.centery:
                self.current_direction = "left"
        if self.rect.centerx < self.player.rect.centerx:
            if self.rect.centery > self.player.rect.centery:
                self.current_direction = "top-right"
            if self.rect.centery < self.player.rect.centery:
                self.current_direction = "bottom-right"
            if self.rect.centery == self.player.rect.centery:
                self.current_direction = "right"
        if self.rect.centerx == self.player.rect.centerx:
            if self.rect.centery > self.player.rect.centery:
                self.current_direction = "top"
            if self.rect.centery < self.player.rect.centery:
                self.current_direction = "bottom"

    def right_death_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.green_enemy_right_death_sprites):
            self.kill()
            self.drop_loot()
        else:
            self.image = self.green_enemy_right_death_sprites[int(self.current_sprite)]

    def left_death_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.green_enemy_left_death_sprites):
            self.kill()
            self.drop_loot()
        else:
            self.image = self.green_enemy_left_death_sprites[int(self.current_sprite)]

    def right_blow_animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.green_enemy_right_blow_sprites):
            self.kill()
        else:
            self.image = self.green_enemy_right_blow_sprites[int(self.current_sprite)]

    def left_blow_animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.green_enemy_left_blow_sprites):
            self.kill()
        else:
            self.image = self.green_enemy_left_blow_sprites[int(self.current_sprite)]

    def death_check(self):
        if self.stats["health"] <= 0:
            if self.current_orientation == "right":
                self.right_death_animation()
            if self.current_orientation == "left":
                self.left_death_animation()
        else:
            if self.current_orientation == "right":
                self.right_blow_animation()
            if self.current_orientation == "left":
                self.left_blow_animation()

    def drop_loot(self):
        x = randint(0, 99)
        if x <= 10:
            Health(self.rect, self.item_group, self.player)
        elif 10 < x <= 20:
            Gold(self.rect, self.item_group, self.player, randint(50, 100))
        elif 20 < x <= 30:
            Armor(self.rect, self.item_group, self.player, 1)
        elif 30 < x <= 40:
            AttackDamage(self.rect, self.item_group, self.player, 1)
        elif 40 < x <= 50:
            HealthPotion(self.rect, self.item_group, self.player)

    def update(self):
        self.is_alive()
        self.detect_collision()
