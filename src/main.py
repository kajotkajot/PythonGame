import random
import sys
import pygame
import numpy as np
from random import randint

"""
IDEAS:
- starting menu screen
- different characters
- better animation for slash attack
- another forward attack
- hp packages dropped by enemies
- ghost on death screen coming out of dead player body
- hp display for individual enemies
"""

# window settings
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect(center=(960, 540))
pygame.display.set_caption("Hemorrhoid Fighter")

# player settings
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100
player_right = pygame.image.load('res/player_right.png').convert()
player_right_scaled = pygame.transform.scale(player_right, (300, 300))
player_left = pygame.image.load('res/player_left.png').convert()
player_death = pygame.image.load('res/player_death.png').convert()
player_death_scaled = pygame.transform.scale(player_death, (300, 300))
player_hp = 10000
player_xp = 0
level = 0
needed_player_xp = 1000
player_speed = 10

# attacks settings
attacks = []
slash_attack_damage = 10

# game settings
game_active = True
clock = pygame.time.Clock()
pygame.init()
background = pygame.image.load('res/background.png').convert()
current_state_image = pygame.image.load('res/background.png').convert()
font = pygame.font.Font("res/font.ttf", 35)
bigger_font = pygame.font.Font("res/font.ttf", 65)
hp_text = font.render('HP', False, 'Black')
level_text = font.render('LEVEL', False, 'Black')
death_text = bigger_font.render('YOU DIED', False, 'Black')
death_text_rect = death_text.get_rect(center=(960, 720))
blurred_current_state_image = pygame.image.load('res/background.png').convert()

# enemy settings
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)
enemies = []
dead_enemies = []

# red enemy settings
red_enemy_hp = 100
red_enemy_speed = 100
red_enemy_xp = 500
red_enemy_damage = 1
red_enemy_right = pygame.image.load('res/enemy_move_right1.png').convert()
red_enemy_left = pygame.image.load('res/enemy_move_left1.png').convert()

# green enemy settings
green_enemy_hp = 100
green_enemy_speed = 250
green_enemy_xp = 1000
green_enemy_damage = 10
green_enemy_right = pygame.image.load('res/green_enemy_move_right1.png').convert()
green_enemy_left = pygame.image.load('res/green_enemy_move_left1.png').convert()


# CLASSES:

# player class
class Player:
    def __init__(self):
        self.speed = player_speed
        self.image = player_right
        self.pos = self.image.get_rect().move(WIDTH / 2 - PLAYER_WIDTH / 2, HEIGHT / 2 - PLAYER_HEIGHT / 2)
        self.player_left_sprites = []
        self.player_left_sprites.append(pygame.image.load('res/player_move_left1.png'))
        self.player_left_sprites.append(pygame.image.load('res/player_move_left2.png'))
        self.player_left_sprites.append(pygame.image.load('res/player_move_left3.png'))
        self.player_left_sprites.append(pygame.image.load('res/player_move_left4.png'))
        self.player_left_sprites.append(pygame.image.load('res/player_move_left5.png'))
        self.player_left_sprites.append(pygame.image.load('res/player_move_left6.png'))
        self.player_right_sprites = []
        self.player_right_sprites.append(pygame.image.load('res/player_move_right1.png'))
        self.player_right_sprites.append(pygame.image.load('res/player_move_right2.png'))
        self.player_right_sprites.append(pygame.image.load('res/player_move_right3.png'))
        self.player_right_sprites.append(pygame.image.load('res/player_move_right4.png'))
        self.player_right_sprites.append(pygame.image.load('res/player_move_right5.png'))
        self.player_right_sprites.append(pygame.image.load('res/player_move_right6.png'))
        self.player_left_death_sprites = []
        self.player_left_death_sprites.append(pygame.image.load('res/player_left_death1.png'))
        self.player_left_death_sprites.append(pygame.image.load('res/player_left_death2.png'))
        self.player_left_death_sprites.append(pygame.image.load('res/player_left_death3.png'))
        self.player_left_death_sprites.append(pygame.image.load('res/player_left_death4.png'))
        self.player_left_death_sprites.append(pygame.image.load('res/player_left_death5.png'))
        self.player_right_death_sprites = []
        self.player_right_death_sprites.append(pygame.image.load('res/player_right_death1.png'))
        self.player_right_death_sprites.append(pygame.image.load('res/player_right_death2.png'))
        self.player_right_death_sprites.append(pygame.image.load('res/player_right_death3.png'))
        self.player_right_death_sprites.append(pygame.image.load('res/player_right_death4.png'))
        self.player_right_death_sprites.append(pygame.image.load('res/player_right_death5.png'))
        self.current_death_sprite = 0
        self.current_sprite = 0
        self.current_orientation = "right"
        self.player_hp = player_hp
        self.player_xp = player_xp
        self.player_lv = level
        self.alive = True
        self.death_animation = False

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
            self.current_orientation = "right"
            self.animation_right()
        if left:
            self.pos.right -= self.speed
            self.current_orientation = "left"
            self.animation_left()
        if down:
            self.pos.top += self.speed
            if self.current_orientation == "right":
                self.animation_right()
            if self.current_orientation == "left":
                self.animation_left()
        if up:
            self.pos.top -= self.speed
            if self.current_orientation == "right":
                self.animation_right()
            if self.current_orientation == "left":
                self.animation_left()
        if self.pos.right > WIDTH + PLAYER_WIDTH / 2:
            self.pos.left = 0 - PLAYER_WIDTH / 2
        if self.pos.top > HEIGHT + PLAYER_HEIGHT / 2:
            self.pos.top = 0 - PLAYER_HEIGHT / 2
        if self.pos.right < 0 - PLAYER_WIDTH / 2:
            self.pos.right = WIDTH + PLAYER_WIDTH / 2
        if self.pos.top < 0 - PLAYER_HEIGHT / 2:
            self.pos.top = HEIGHT - PLAYER_HEIGHT / 2

    def animation_right(self):
        self.current_sprite += 0.01 * self.speed
        if self.current_sprite >= len(self.player_right_sprites):
            self.current_sprite = 0
        self.image = self.player_right_sprites[int(self.current_sprite)]

    def animation_left(self):
        self.current_sprite += 0.01 * self.speed
        if self.current_sprite >= len(self.player_left_sprites):
            self.current_sprite = 0
        self.image = self.player_left_sprites[int(self.current_sprite)]

    def right_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.player_right_death_sprites) + 5:
            self.death_animation = False
        if self.current_death_sprite <= len(self.player_right_death_sprites):
            self.image = self.player_right_death_sprites[int(self.current_death_sprite)]

    def left_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.player_left_death_sprites) + 5:
            self.death_animation = False
        if self.current_death_sprite <= len(self.player_left_death_sprites):
            self.image = self.player_left_death_sprites[int(self.current_death_sprite)]

    def death_check(self):
        if self.current_orientation == "right":
            self.right_death_animation()
        if self.current_orientation == "left":
            self.left_death_animation()

    def player_alive(self):
        if self.player_hp <= 0:
            self.player_hp = 0
            self.death_animation = True
            self.death_check()
            self.alive = False


# red enemy class
class RedEnemy:
    def __init__(self, enemy_cords):
        self.speed = red_enemy_speed
        self.image = red_enemy_right
        self.pos = self.image.get_rect().move(enemy_cords[0], enemy_cords[1])
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
        x_range = (abs(self.pos.right - player.pos.left) + abs(self.pos.left - player.pos.right)) / 10000
        y_range = (abs(self.pos.top - player.pos.bottom) + abs(self.pos.bottom - player.pos.top)) / 10000
        x_speed = self.speed * x_range
        y_speed = self.speed * y_range
        if self.pos.right > player.pos.right and self.pos.top > player.pos.top:
            self.pos.right -= x_speed
            self.pos.top -= y_speed
            self.current_orientation = "left"
        if self.pos.right > player.pos.right and self.pos.top < player.pos.top:
            self.pos.right -= x_speed
            self.pos.top += y_speed
            self.current_orientation = "left"
        if self.pos.right < player.pos.right and self.pos.top > player.pos.top:
            self.pos.right += x_speed
            self.pos.top -= y_speed
            self.current_orientation = "right"
        if self.pos.right < player.pos.right and self.pos.top < player.pos.top:
            self.pos.right += x_speed
            self.pos.top += y_speed
            self.current_orientation = "right"
        if self.pos.right == player.pos.right and self.pos.top > player.pos.top:
            self.pos.top -= y_speed
        if self.pos.right == player.pos.right and self.pos.top < player.pos.top:
            self.pos.top += y_speed
        if self.pos.right > player.pos.right and self.pos.top == player.pos.top:
            self.pos.right -= x_speed
            self.current_orientation = "left"
        if self.pos.right < player.pos.right and self.pos.top == player.pos.top:
            self.pos.right += x_speed
            self.current_orientation = "right"

    def detect_collision(self):
        if self.pos.colliderect(player.pos):
            player.player_hp -= red_enemy_damage
        if not self.pos.colliderect(player.pos):
            self.move()
        for x in attacks:
            if self.pos.colliderect(x.pos):
                self.hp -= slash_attack_damage
        screen.blit(enemy.image, enemy.pos)

    def right_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_right_death_sprites):
            dead_enemies.remove(self)
        else:
            self.image = self.red_enemy_right_death_sprites[int(self.current_death_sprite)]

    def left_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_left_death_sprites):
            dead_enemies.remove(self)
        else:
            self.image = self.red_enemy_left_death_sprites[int(self.current_death_sprite)]

    def death_check(self):
        if self.current_orientation == "right":
            self.right_death_animation()
        if self.current_orientation == "left":
            self.left_death_animation()

    def is_alive(self):
        if self.hp <= 0:
            enemies.remove(self)
            dead_enemies.append(self)
            player.player_xp += red_enemy_xp


# green enemy class
class GreenEnemy:
    def __init__(self, enemy_cords):
        self.speed = green_enemy_speed
        self.image = green_enemy_right
        self.pos = self.image.get_rect().move(enemy_cords[0], enemy_cords[1])
        self.enemy_left_sprites = []
        self.enemy_left_sprites.append(pygame.image.load('res/green_enemy_move_left1.png'))
        self.enemy_left_sprites.append(pygame.image.load('res/green_enemy_move_left2.png'))
        self.enemy_right_sprites = []
        self.enemy_right_sprites.append(pygame.image.load('res/green_enemy_move_right1.png'))
        self.enemy_right_sprites.append(pygame.image.load('res/green_enemy_move_right2.png'))
        self.green_enemy_left_death_sprites = []
        self.green_enemy_left_death_sprites.append(pygame.image.load('res/green_enemy_left_death1.png'))
        self.green_enemy_left_death_sprites.append(pygame.image.load('res/green_enemy_left_death2.png'))
        self.green_enemy_left_death_sprites.append(pygame.image.load('res/green_enemy_left_death3.png'))
        self.green_enemy_left_death_sprites.append(pygame.image.load('res/green_enemy_left_death4.png'))
        self.green_enemy_right_death_sprites = []
        self.green_enemy_right_death_sprites.append(pygame.image.load('res/green_enemy_right_death1.png'))
        self.green_enemy_right_death_sprites.append(pygame.image.load('res/green_enemy_right_death2.png'))
        self.green_enemy_right_death_sprites.append(pygame.image.load('res/green_enemy_right_death3.png'))
        self.green_enemy_right_death_sprites.append(pygame.image.load('res/green_enemy_right_death4.png'))
        self.green_enemy_left_blow_sprites = []
        self.green_enemy_left_blow_sprites.append(pygame.image.load('res/green_enemy_left_blow1.png'))
        self.green_enemy_left_blow_sprites.append(pygame.image.load('res/green_enemy_left_blow2.png'))
        self.green_enemy_left_blow_sprites.append(pygame.image.load('res/green_enemy_left_blow3.png'))
        self.green_enemy_left_blow_sprites.append(pygame.image.load('res/green_enemy_left_blow4.png'))
        self.green_enemy_left_blow_sprites.append(pygame.image.load('res/green_enemy_left_blow5.png'))
        self.green_enemy_right_blow_sprites = []
        self.green_enemy_right_blow_sprites.append(pygame.image.load('res/green_enemy_right_blow1.png'))
        self.green_enemy_right_blow_sprites.append(pygame.image.load('res/green_enemy_right_blow2.png'))
        self.green_enemy_right_blow_sprites.append(pygame.image.load('res/green_enemy_right_blow3.png'))
        self.green_enemy_right_blow_sprites.append(pygame.image.load('res/green_enemy_right_blow4.png'))
        self.green_enemy_right_blow_sprites.append(pygame.image.load('res/green_enemy_right_blow5.png'))
        self.current_sprite = 0
        self.current_orientation = "right"
        self.current_direction = "none"
        self.hp = green_enemy_hp
        self.timer = 0
        self.x_range = 0.3
        self.y_range = 0.3

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
            self.pos.right -= x_speed
            self.pos.top -= y_speed
            self.current_orientation = "left"
        if self.current_direction == "bottom-left":
            self.pos.right -= x_speed
            self.pos.top += y_speed
            self.current_orientation = "left"
        if self.current_direction == "top-right":
            self.pos.right += x_speed
            self.pos.top -= y_speed
            self.current_orientation = "right"
        if self.current_direction == "bottom-right":
            self.pos.right += x_speed
            self.pos.top += y_speed
            self.current_orientation = "right"
        if self.current_direction == "top":
            self.pos.top -= y_speed
        if self.current_direction == "bottom":
            self.pos.top += y_speed
        if self.current_direction == "left":
            self.pos.right -= x_speed
            self.current_orientation = "left"
        if self.current_direction == "right":
            self.pos.right += x_speed
            self.current_orientation = "right"

    def stand_right(self):
        self.speed = 0
        self.image = self.enemy_right_sprites[0]

    def stand_left(self):
        self.speed = 0
        self.image = self.enemy_left_sprites[0]

    def detect_collision(self):
        if self.pos.colliderect(player.pos) and not self.speed == 0:
            player.player_hp -= green_enemy_damage
            enemies.remove(self)
            dead_enemies.append(self)
            self.pos.top -= 20
        if not self.pos.colliderect(player.pos):
            self.move()
        for x in attacks:
            if self.pos.colliderect(x.pos):
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
        screen.blit(enemy.image, enemy.pos)

    def check_direction(self):
        self.x_range = (abs(self.pos.right - player.pos.left) + abs(self.pos.left - player.pos.right)) / 2000
        if self.x_range >= 0.6:
            self.x_range = 0.6
        self.y_range = (abs(self.pos.top - player.pos.bottom) + abs(self.pos.bottom - player.pos.top)) / 2000
        if self.y_range >= 0.6:
            self.y_range = 0.6
        self.speed = green_enemy_speed
        if self.pos.right > player.pos.right and self.pos.top > player.pos.top:
            self.current_direction = "top-left"
        if self.pos.right > player.pos.right and self.pos.top < player.pos.top:
            self.current_direction = "bottom-left"
        if self.pos.right < player.pos.right and self.pos.top > player.pos.top:
            self.current_direction = "top-right"
        if self.pos.right < player.pos.right and self.pos.top < player.pos.top:
            self.current_direction = "bottom-right"
        if self.pos.right == player.pos.right and self.pos.top > player.pos.top:
            self.current_direction = "top"
        if self.pos.right == player.pos.right and self.pos.top < player.pos.top:
            self.current_direction = "bottom"
        if self.pos.right > player.pos.right and self.pos.top == player.pos.top:
            self.current_direction = "left"
        if self.pos.right < player.pos.right and self.pos.top == player.pos.top:
            self.current_direction = "right"

    def right_death_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.green_enemy_right_death_sprites):
            dead_enemies.remove(self)
        else:
            self.image = self.green_enemy_right_death_sprites[int(self.current_sprite)]

    def left_death_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.green_enemy_left_death_sprites):
            dead_enemies.remove(self)
        else:
            self.image = self.green_enemy_left_death_sprites[int(self.current_sprite)]

    def right_blow_animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.green_enemy_right_blow_sprites):
            dead_enemies.remove(self)
        else:
            self.image = self.green_enemy_right_blow_sprites[int(self.current_sprite)]

    def left_blow_animation(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.green_enemy_left_blow_sprites):
            dead_enemies.remove(self)
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

    def is_alive(self):
        if self.hp <= 0:
            enemies.remove(self)
            dead_enemies.append(self)
            player.player_xp += green_enemy_xp


# slash attack class
class SlashAttack:
    def __init__(self):
        self.animation_sprites = []
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation1.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation2.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation3.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation4.png'))
        self.animation_sprites.append(pygame.image.load('res/slash_attack_animation5.png'))
        self.current_sprite = 0
        self.image = self.animation_sprites[0]
        self.pos = self.image.get_rect().move(player.pos.right - 150, player.pos.top - 70)
        self.damage = slash_attack_damage

    def animation(self):
        self.current_sprite += 0.5
        if self.current_sprite >= len(self.animation_sprites):
            attacks.remove(self)
        else:
            self.image = self.animation_sprites[int(self.current_sprite)]
            self.pos = self.image.get_rect().move(player.pos.right - 150, player.pos.top - 70)
        screen.blit(attack.image, attack.pos)


# FUNCTIONS:

# random enemy spawns
def enemy_spawn():
    cords = [[-100, randint(-60, 1080)], [1920, randint(-60, 1080)], [randint(-100, 1920), -60], [randint(-100, 1920), 1080]]
    chosen_cords = random.choice(cords)
    if randint(0, 1) == 0:
        spawned_enemy = RedEnemy(chosen_cords)
    else:
        spawned_enemy = GreenEnemy(chosen_cords)
    enemies.append(spawned_enemy)


# adding attack to array
def add_slash_attack():
    if player.alive is True:
        new_attack = SlashAttack()
        attacks.append(new_attack)


# HP definition
def display_hp():
    hp_division = player_hp / 500
    hp_bar = pygame.Surface([player.player_hp / hp_division, 35])
    hp_bar_under = pygame.Surface([500, 35])
    hp_bar_border = pygame.Surface([510, 45])
    hp_bar.fill("red")
    hp_bar_under.fill("grey")
    hp_bar_border.fill("black")
    screen.blit(hp_bar_border, (20, 20))
    screen.blit(hp_bar_under, (25, 25))
    screen.blit(hp_bar, (25, 25))
    screen.blit(hp_text, (30, 25))


# XP definition
def display_xp():
    if player.player_xp >= 1000:
        player.player_xp -= needed_player_xp
        player.player_lv += 1
    xp_division = needed_player_xp / 2000
    xp_bar = pygame.Surface([xp_division * player.player_xp, 35])
    xp_bar_under = pygame.Surface([500, 35])
    xp_bar_border = pygame.Surface([510, 45])
    xp_bar.fill("blue")
    xp_bar_under.fill("grey")
    xp_bar_border.fill("black")
    screen.blit(xp_bar_border, (1390, 20))
    screen.blit(xp_bar_under, (1395, 25))
    screen.blit(xp_bar, (1395, 25))
    screen.blit(level_text, (1785, 25))
    xp = font.render(str(player.player_lv), False, 'Black')
    screen.blit(xp, (1402, 25))


# greyscale definition
def greyscale(step0):
    step1 = pygame.surfarray.pixels3d(step0)
    step2 = np.dot(step1[:, :, :], [0.216, 0.587, 0.144])
    step3 = step2[..., np.newaxis]
    step4 = np.repeat(step3[:, :, :], 3, axis=2)
    return pygame.surfarray.make_surface(step4)


# show pause screen
def pause_screen():
    screen.blit(blurred_current_state_image, screen_rect)
    screen.blit(player_right_scaled, (810, 350))
    pause_lv = bigger_font.render(f'Level:{player.player_lv}', False, 'Black')
    pause_lv_rect = pause_lv.get_rect(center=(960, 700))
    screen.blit(pause_lv, pause_lv_rect)


# show death screen
def death_screen():
    screen.fill("grey")
    screen.blit(player_death_scaled, (810, 350))
    screen.blit(death_text, death_text_rect)
    death_level = font.render(f'Level:{player.player_lv}', False, 'Black')
    death_level_rect = death_level.get_rect(center=(960, 800))
    screen.blit(death_level, death_level_rect)


# create player
player = Player()

# MAIN GAME LOOP:
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if game_active is True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    add_slash_attack()
                if event.key == pygame.K_ESCAPE:
                    # creating blurred image for pause menu
                    blurred_current_state_image = greyscale(current_state_image)
                    game_active = False
            if event.type == enemy_timer:
                enemy_spawn()
        else:
            if player.alive is True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_active = True

    if game_active is True:
        # show background
        screen.blit(background, (0, 0))

        # controls
        if player.alive is True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.move(up=True)
            if keys[pygame.K_s]:
                player.move(down=True)
            if keys[pygame.K_a]:
                player.move(left=True)
            if keys[pygame.K_d]:
                player.move(right=True)

        # show enemies on screen
        for enemy in enemies:
            enemy.is_alive()
            enemy.detect_collision()

        # show death animation for dead enemies
        for dead_enemy in dead_enemies:
            dead_enemy.death_check()
            screen.blit(dead_enemy.image, dead_enemy.pos)

        # show player on screen
        screen.blit(player.image, player.pos)
        if player.current_orientation == "right" and player.alive is True:
            player.image = player_right
        if player.current_orientation == "left" and player.alive is True:
            player.image = player_left
        player.player_alive()

        # saving current screen
        pygame.Surface.blit(current_state_image, screen, screen_rect)

        # show hp and xp on the screen
        if player.death_animation is False and player.alive is False:
            game_active = False
        if game_active is True and player.player_hp >= 0:
            display_hp()
            display_xp()

        # show attacks
        for attack in attacks:
            attack.animation()

    else:
        # show pause screen
        if player.alive is True:
            pause_screen()
        else:
            death_screen()

    # update and clock
    pygame.display.update()
    clock.tick(60)
