from settings import *
from assets import *
from random import randint
from hp import Hp
from gold import Gold
from armor import Armor
from attackdamage import AttackDamage


class GreenEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_cords, enemy_group, dead_enemy_group, attack_group, item_group, player):
        super().__init__(enemy_group)
        self.enemy_group = enemy_group
        self.attack_group = attack_group
        self.item_group = item_group
        self.dead_enemy_group = dead_enemy_group
        self.player = player
        self.speed = green_enemy_speed
        self.image = green_enemy_right
        self.rect = self.image.get_rect().move(enemy_cords[0], enemy_cords[1])
        self.enemy_left_sprites = green_enemy_left_sprites
        self.enemy_right_sprites = green_enemy_right_sprites
        self.green_enemy_left_death_sprites = green_enemy_left_death_sprites
        self.green_enemy_right_death_sprites = green_enemy_right_death_sprites
        self.green_enemy_left_blow_sprites = green_enemy_left_blow_sprites
        self.green_enemy_right_blow_sprites = green_enemy_right_blow_sprites
        self.current_sprite = 0
        self.current_orientation = "right"
        self.current_direction = "none"
        self.hp = green_enemy_hp
        self.timer = 0
        self.x_range = 0.3
        self.y_range = 0.3
        self.hit_box = self.rect
        self.mass = 1
        self.restitution = 0.8

    def move(self):
        if self.current_orientation == "right":
            self.move_right()
        if self.current_orientation == "left":
            self.move_left()

    def move_right(self):
        self.image = self.enemy_right_sprites[1]
        self.move_def()

    def move_left(self):
        self.image = self.enemy_left_sprites[1]
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
        self.image = self.enemy_right_sprites[0]

    def stand_left(self):
        self.speed = 0
        self.image = self.enemy_left_sprites[0]

    def is_alive(self):
        if self.hp <= 0:
            self.hp = 0
            if self in self.enemy_group:
                self.enemy_group.remove(self)
                self.dead_enemy_group.add(self)
            self.player.player_xp += green_enemy_xp

    def detect_collision(self):
        if self.rect.colliderect(self.player.rect) and not self.speed == 0:
            self.player.player_hp -= green_enemy_damage
            if self in self.enemy_group:
                self.enemy_group.remove(self)
                self.dead_enemy_group.add(self)
            self.rect.top -= 20
        if not self.rect.colliderect(self.player.rect):
            self.move()
        for x in self.attack_group:
            if self.rect.colliderect(x.rect):
                self.hp -= x.damage
        self.speed -= self.timer
        self.timer += 1.5
        if self.speed <= 0:
            if self.current_orientation == "right":
                self.stand_right()
            if self.current_orientation == "left":
                self.stand_left()
        if self.timer >= 100:
            self.check_direction()
            self.timer = 0

    def check_direction(self):
        self.x_range = (abs(self.rect.right - self.player.rect.left) + abs(self.rect.left - self.player.rect.right)) / 2000
        if self.x_range >= 0.6:
            self.x_range = 0.6
        self.y_range = (abs(self.rect.top - self.player.rect.bottom) + abs(self.rect.bottom - self.player.rect.top)) / 2000
        if self.y_range >= 0.6:
            self.y_range = 0.6
        self.speed = green_enemy_speed
        if self.rect.right > self.player.rect.right and self.rect.top > self.player.rect.top:
            self.current_direction = "top-left"
        if self.rect.right > self.player.rect.right and self.rect.top < self.player.rect.top:
            self.current_direction = "bottom-left"
        if self.rect.right < self.player.rect.right and self.rect.top > self.player.rect.top:
            self.current_direction = "top-right"
        if self.rect.right < self.player.rect.right and self.rect.top < self.player.rect.top:
            self.current_direction = "bottom-right"
        if self.rect.right == self.player.rect.right and self.rect.top > self.player.rect.top:
            self.current_direction = "top"
        if self.rect.right == self.player.rect.right and self.rect.top < self.player.rect.top:
            self.current_direction = "bottom"
        if self.rect.right > self.player.rect.right and self.rect.top == self.player.rect.top:
            self.current_direction = "left"
        if self.rect.right < self.player.rect.right and self.rect.top == self.player.rect.top:
            self.current_direction = "right"

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
        if self.hp <= 0:
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
            Hp(self.rect, self.item_group, self.player)
        elif 10 < x <= 20:
            Gold(self.rect, self.item_group, self.player, randint(50, 100))
        elif 20 < x <= 30:
            Armor(self.rect, self.item_group, self.player, 10)
        elif 30 < x <= 40:
            AttackDamage(self.rect, self.item_group, self.player, 1)

    def update(self):
        self.is_alive()
        self.detect_collision()
