import numpy as np
from settings import *
from assets import *


class Player(pygame.sprite.Sprite):
    def __init__(self, group, character):
        super().__init__(group)
        self.speed = player_speed
        self.direction = pygame.math.Vector2()
        self.current_death_sprite = 0
        self.current_sprite = 0
        self.current_orientation = "right"
        self.player_hp = player_hp
        self.player_xp = player_xp
        self.player_lv = level
        self.player_gold = player_gold
        self.camera = pygame.math.Vector2(0, 0)
        self.current_camera_position = pygame.math.Vector2(0, 0)
        self.camera_speed = self.speed/5
        self.camera_range = self.speed*10
        self.ghost_timer = 0
        self.ghost_transparency = 0
        self.ghost_current_sprite = 0
        self.ghost_image = ghost_sprites[0]
        self.alive = True
        self.death_animation = False
        self.skill_points = 0
        self.basic_attack_cooldown = 1000
        if character == 'Knight':
            self.image = knight_right
            self.image_right = knight_right
            self.image_right_scaled = knight_right_scaled
            self.image_death = knight_death
            self.image_death_scaled = knight_death_scaled
            self.player_left_stand_sprites = knight_left_stand_sprites
            self.player_right_stand_sprites = knight_right_stand_sprites
            self.player_left_sprites = knight_left_sprites
            self.player_right_sprites = knight_right_sprites
            self.player_left_death_sprites = knight_left_death_sprites
            self.player_right_death_sprites = knight_right_death_sprites
            self.animation_timer = 0.05
            self.basic_attack_icon = knight_basic_attack_icon
        if character == 'Angel':
            self.image = angel_right
            self.image_right = angel_right
            self.image_right_scaled = angel_right_scaled
            self.image_death = angel_death
            self.image_death_scaled = angel_death_scaled
            self.player_left_stand_sprites = angel_left_stand_sprites
            self.player_right_stand_sprites = angel_right_stand_sprites
            self.player_left_sprites = angel_left_sprites
            self.player_right_sprites = angel_right_sprites
            self.player_left_death_sprites = angel_left_death_sprites
            self.player_right_death_sprites = angel_right_death_sprites
            self.animation_timer = 0.1
            self.basic_attack_icon = swordsman_basic_attack_icon
        if character == 'Assassin':
            self.image = assassin_right
            self.image_right = assassin_right
            self.image_right_scaled = assassin_right_scaled
            self.image_death = assassin_death
            self.image_death_scaled = assassin_death_scaled
            self.player_left_stand_sprites = assassin_left_stand_sprites
            self.player_right_stand_sprites = assassin_right_stand_sprites
            self.player_left_sprites = assassin_left_sprites
            self.player_right_sprites = assassin_right_sprites
            self.player_left_death_sprites = assassin_left_death_sprites
            self.player_right_death_sprites = assassin_right_death_sprites
            self.animation_timer = 0.1
            self.basic_attack_icon = swordsman_basic_attack_icon
        if character == 'Mage':
            self.image = mage_right
            self.image_right = mage_right
            self.image_right_scaled = mage_right_scaled
            self.image_death = mage_death
            self.image_death_scaled = mage_death_scaled
            self.player_left_stand_sprites = mage_left_stand_sprites
            self.player_right_stand_sprites = mage_right_stand_sprites
            self.player_left_sprites = mage_left_sprites
            self.player_right_sprites = mage_right_sprites
            self.player_left_death_sprites = mage_left_death_sprites
            self.player_right_death_sprites = mage_right_death_sprites
            self.animation_timer = 0.15
            self.basic_attack_icon = swordsman_basic_attack_icon
        if character == 'Necromancer':
            self.image = necromancer_right
            self.image_right = necromancer_right
            self.image_right_scaled = necromancer_right_scaled
            self.image_death = necromancer_death
            self.image_death_scaled = necromancer_death_scaled
            self.player_left_stand_sprites = necromancer_left_stand_sprites
            self.player_right_stand_sprites = necromancer_right_stand_sprites
            self.player_left_sprites = necromancer_left_sprites
            self.player_right_sprites = necromancer_right_sprites
            self.player_left_death_sprites = necromancer_left_death_sprites
            self.player_right_death_sprites = necromancer_right_death_sprites
            self.animation_timer = 0.1
            self.basic_attack_icon = swordsman_basic_attack_icon
        if character == 'Swordsman':
            self.image = swordsman_right
            self.image_right = swordsman_right
            self.image_right_scaled = swordsman_right_scaled
            self.image_death = swordsman_death
            self.image_death_scaled = swordsman_death_scaled
            self.player_left_stand_sprites = swordsman_left_stand_sprites
            self.player_right_stand_sprites = swordsman_right_stand_sprites
            self.player_left_sprites = swordsman_left_sprites
            self.player_right_sprites = swordsman_right_sprites
            self.player_left_death_sprites = swordsman_left_death_sprites
            self.player_right_death_sprites = swordsman_right_death_sprites
            self.animation_timer = 0.1
            self.basic_attack_icon = swordsman_basic_attack_icon
        self.rect = self.image.get_rect().move(WIDTH / 2 - PLAYER_WIDTH / 2, HEIGHT / 2 - PLAYER_HEIGHT / 2)

    def move(self, up=False, down=False, left=False, right=False):
        if up:
            self.direction.y = -1
            self.handle_camera(0, -self.camera_speed, True)
            if self.current_orientation == "right":
                self.animation_right()
            if self.current_orientation == "left":
                self.animation_left()
        if down:
            self.direction.y = 1
            self.handle_camera(0, self.camera_speed, True)
            if self.current_orientation == "right":
                self.animation_right()
            if self.current_orientation == "left":
                self.animation_left()
        if right:
            self.direction.x = 1
            self.handle_camera(self.camera_speed, 0, True)
            self.current_orientation = "right"
            self.animation_right()
        if left:
            self.direction.x = -1
            self.handle_camera(-self.camera_speed, 0, True)
            self.current_orientation = "left"
            self.animation_left()

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
        if self.current_death_sprite >= len(self.player_right_death_sprites) + 8:
            self.death_animation = False
        if self.current_death_sprite <= len(self.player_right_death_sprites):
            self.image = self.player_right_death_sprites[int(self.current_death_sprite)]

    def left_death_animation(self):
        self.current_death_sprite += 0.1
        if self.current_death_sprite >= len(self.player_left_death_sprites) + 8:
            self.death_animation = False
        if self.current_death_sprite <= len(self.player_left_death_sprites):
            self.image = self.player_left_death_sprites[int(self.current_death_sprite)]

    def ghost_animation(self):
        self.ghost_current_sprite += 0.05
        if self.ghost_current_sprite >= len(ghost_sprites):
            self.ghost_current_sprite = 0
        self.ghost_image = ghost_sprites[int(self.ghost_current_sprite)]
        self.ghost_timer += 0.04
        self.ghost_transparency = np.sin(self.ghost_timer * 0.7) * 255
        self.ghost_image.set_alpha(self.ghost_transparency)

    def death_check(self):
        if self.current_orientation == "right":
            self.right_death_animation()
            self.ghost_animation()
        if self.current_orientation == "left":
            self.left_death_animation()
            self.ghost_animation()

    def player_alive(self):
        if self.player_hp <= 0:
            self.player_hp = 0
            self.death_animation = True
            self.death_check()
            self.alive = False

    def handle_camera(self, direction_x, direction_y, movement):
        if movement:
            if direction_x > 0:
                if self.camera.x < self.camera_range:
                    self.camera.x += direction_x
            if direction_x < 0:
                if self.camera.x > -self.camera_range:
                    self.camera.x += direction_x
            if direction_y > 0:
                if self.camera.y < self.camera_range:
                    self.camera.y += direction_y
            if direction_y < 0:
                if self.camera.y > -self.camera_range:
                    self.camera.y += direction_y
            self.current_camera_position = self.camera
        else:
            if direction_x > 0:
                self.camera.x -= abs(self.current_camera_position.x)/20
            if direction_x < 0:
                self.camera.x += abs(self.current_camera_position.x)/20
            if direction_y > 0:
                self.camera.y -= abs(self.current_camera_position.y)/20
            if direction_y < 0:
                self.camera.y += abs(self.current_camera_position.y)/20

    def input(self):
        if self.alive:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and keys[pygame.K_s]:
                self.direction.y = 0
                self.handle_camera(0, self.camera.y, False)
            elif keys[pygame.K_w]:
                self.move(up=True)
            elif keys[pygame.K_s]:
                self.move(down=True)
            else:
                self.direction.y = 0
                self.handle_camera(0, self.camera.y, False)
            if keys[pygame.K_a] and keys[pygame.K_d]:
                self.direction.x = 0
                self.handle_camera(self.camera.x, 0, False)
            elif keys[pygame.K_a]:
                self.move(left=True)
            elif keys[pygame.K_d]:
                self.move(right=True)
            else:
                self.direction.x = 0
                self.handle_camera(self.camera.x, 0, False)
            self.rect.center += self.direction * self.speed

    def update(self):
        self.input()
        self.player_alive()
