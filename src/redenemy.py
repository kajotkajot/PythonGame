from settings import *
from random import randint
from hp import Hp


class RedEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_cords, enemy_group, dead_enemy_group, attack_group, health_group, player):
        super().__init__(enemy_group)
        self.enemy_group = enemy_group
        self.attack_group = attack_group
        self.health_group = health_group
        self.dead_enemy_group = dead_enemy_group
        self.player = player
        self.speed = red_enemy_speed
        self.image = red_enemy_right
        self.rect = self.image.get_rect().move(enemy_cords[0], enemy_cords[1])
        self.enemy_left_sprites = []
        self.enemy_left_sprites.append(pygame.image.load('res/enemy_move_left1.png'))
        self.enemy_left_sprites.append(pygame.image.load('res/enemy_move_left2.png'))
        self.enemy_right_sprites = []
        self.enemy_right_sprites.append(pygame.image.load('res/enemy_move_right1.png'))
        self.enemy_right_sprites.append(pygame.image.load('res/enemy_move_right2.png'))
        self.red_enemy_left_death_sprites = []
        self.red_enemy_left_death_sprites.append(pygame.image.load('res/red_enemy_left_death1.png'))
        self.red_enemy_left_death_sprites.append(pygame.image.load('res/red_enemy_left_death2.png'))
        self.red_enemy_left_death_sprites.append(pygame.image.load('res/red_enemy_left_death3.png'))
        self.red_enemy_left_death_sprites.append(pygame.image.load('res/red_enemy_left_death4.png'))
        self.red_enemy_right_death_sprites = []
        self.red_enemy_right_death_sprites.append(pygame.image.load('res/red_enemy_right_death1.png'))
        self.red_enemy_right_death_sprites.append(pygame.image.load('res/red_enemy_right_death2.png'))
        self.red_enemy_right_death_sprites.append(pygame.image.load('res/red_enemy_right_death3.png'))
        self.red_enemy_right_death_sprites.append(pygame.image.load('res/red_enemy_right_death4.png'))
        self.current_death_sprite = 0
        self.current_sprite = 0
        self.current_orientation = "right"
        self.hp = red_enemy_hp

    def move(self):
        if self.current_orientation == "right":
            self.move_right()
        if self.current_orientation == "left":
            self.move_left()

    def move_right(self):
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.enemy_right_sprites):
            self.current_sprite = 0
        self.image = self.enemy_right_sprites[int(self.current_sprite)]
        self.move_def()

    def move_left(self):
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.enemy_left_sprites):
            self.current_sprite = 0
        self.image = self.enemy_left_sprites[int(self.current_sprite)]
        self.move_def()

    def move_def(self):
        x_range = (abs(self.rect.right - self.player.rect.left) + abs(self.rect.left - self.player.rect.right)) / 10000
        y_range = (abs(self.rect.top - self.player.rect.bottom) + abs(self.rect.bottom - self.player.rect.top)) / 10000
        x_speed = self.speed * x_range
        y_speed = self.speed * y_range
        if self.rect.right > self.player.rect.right and self.rect.top > self.player.rect.top:
            self.rect.right -= x_speed
            self.rect.top -= y_speed
            self.current_orientation = "left"
        if self.rect.right > self.player.rect.right and self.rect.top < self.player.rect.top:
            self.rect.right -= x_speed
            self.rect.top += y_speed
            self.current_orientation = "left"
        if self.rect.right < self.player.rect.right and self.rect.top > self.player.rect.top:
            self.rect.right += x_speed
            self.rect.top -= y_speed
            self.current_orientation = "right"
        if self.rect.right < self.player.rect.right and self.rect.top < self.player.rect.top:
            self.rect.right += x_speed
            self.rect.top += y_speed
            self.current_orientation = "right"
        if self.rect.right == self.player.rect.right and self.rect.top > self.player.rect.top:
            self.rect.top -= y_speed
        if self.rect.right == self.player.rect.right and self.rect.top < self.player.rect.top:
            self.rect.top += y_speed
        if self.rect.right > self.player.rect.right and self.rect.top == self.player.rect.top:
            self.rect.right -= x_speed
            self.current_orientation = "left"
        if self.rect.right < self.player.rect.right and self.rect.top == self.player.rect.top:
            self.rect.right += x_speed
            self.current_orientation = "right"

    def detect_collision(self):
        if self.rect.colliderect(self.player.rect):
            self.player.player_hp -= red_enemy_damage
        if not self.rect.colliderect(self.player.rect):
            self.move()
        for x in self.attack_group:
            if self.rect.colliderect(x.rect):
                self.hp -= x.damage

    def right_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_right_death_sprites):
            self.kill()
            self.drop_hp()
        else:
            self.image = self.red_enemy_right_death_sprites[int(self.current_death_sprite)]

    def left_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_left_death_sprites):
            self.kill()
            self.drop_hp()
        else:
            self.image = self.red_enemy_left_death_sprites[int(self.current_death_sprite)]

    def death_check(self):
        if self.current_orientation == "right":
            self.right_death_animation()
        if self.current_orientation == "left":
            self.left_death_animation()

    def drop_hp(self):
        if randint(0, 9) >= 7:
            Hp(self.rect, self.health_group, self.player)

    def is_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.enemy_group.remove(self)
            self.dead_enemy_group.add(self)
            self.player.player_xp += red_enemy_xp

    def update(self):
        self.is_alive()
        self.detect_collision()
