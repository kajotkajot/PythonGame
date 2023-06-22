from settings import *


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
