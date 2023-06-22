from settings import *
from random import randint
from hp import Hp


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

    def move(self, player):
        if self.current_orientation == "right":
            self.move_right(player)
        if self.current_orientation == "left":
            self.move_left(player)

    def move_right(self, player):
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.enemy_right_sprites):
            self.current_sprite = 0
        self.image = self.enemy_right_sprites[int(self.current_sprite)]
        self.move_def(player)

    def move_left(self, player):
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.enemy_left_sprites):
            self.current_sprite = 0
        self.image = self.enemy_left_sprites[int(self.current_sprite)]
        self.move_def(player)

    def move_def(self, player):
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

    def detect_collision(self, player):
        if self.pos.colliderect(player.pos):
            player.player_hp -= red_enemy_damage
        if not self.pos.colliderect(player.pos):
            self.move(player)
        for x in attacks:
            if self.pos.colliderect(x.pos):
                self.hp -= slash_attack_damage
        screen.blit(self.image, self.pos)

    def right_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_right_death_sprites):
            dead_enemies.remove(self)
            self.drop_hp()
        else:
            self.image = self.red_enemy_right_death_sprites[int(self.current_death_sprite)]

    def left_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.red_enemy_left_death_sprites):
            dead_enemies.remove(self)
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
            new_hp = Hp(self.pos)
            hp_list.append(new_hp)

    def is_alive(self, player):
        if self.hp <= 0:
            enemies.remove(self)
            dead_enemies.append(self)
            player.player_xp += red_enemy_xp

    def display_hp(self):
        hp_division = red_enemy_hp / (abs(self.pos.left - self.pos.right) - 10)
        hp_bar = pygame.Surface([(self.hp / hp_division), 5])
        hp_bar_under = pygame.Surface([abs(self.pos.left - self.pos.right) - 10, 5])
        hp_bar.fill("red")
        hp_bar_under.fill("black")
        screen.blit(hp_bar_under, (self.pos.left + 5, self.pos.top - 15))
        screen.blit(hp_bar, (self.pos.left + 5, self.pos.top - 15))

    def update(self, player):
        self.is_alive(player)
        self.display_hp()
        self.detect_collision(player)
