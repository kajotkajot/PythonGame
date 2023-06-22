from settings import *
from hp import Hp


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

    def detect_collision(self, player):
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
            self.check_direction(player)
            self.timer = 0
        screen.blit(self.image, self.pos)

    def check_direction(self, player):
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
            self.drop_hp()
        else:
            self.image = self.green_enemy_right_death_sprites[int(self.current_sprite)]

    def left_death_animation(self):
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.green_enemy_left_death_sprites):
            dead_enemies.remove(self)
            self.drop_hp()
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

    def drop_hp(self):
        new_hp = Hp(self.pos)
        hp_list.append(new_hp)

    def is_alive(self, player):
        if self.hp <= 0:
            enemies.remove(self)
            dead_enemies.append(self)
            player.player_xp += green_enemy_xp

    def display_hp(self):
        hp_division = green_enemy_hp / (abs(self.pos.left - self.pos.right) - 10)
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
