import math
import numpy as np
from settings import *
from assets import *
from src.angelfiles.angelskills import AngelSkill
from src.angelfiles.angelskill8 import AngelSkill8
from src.angelfiles.angelskill10 import AngelSkill10
from spritegroups import SkillGroup


class Player(pygame.sprite.Sprite):
    def __init__(self, group, character, passive_group, attack_group, enemy_group):
        super().__init__(group)
        self.direction = pygame.math.Vector2()
        self.current_death_sprite = 0
        self.current_sprite = 0
        self.current_orientation = "right"
        self.xp = player_xp
        self.level = level
        self.gold = player_gold
        self.max_hp = angel_stats["health"]
        self.current_hp = angel_stats["health"]
        self.speed = angel_stats["speed"]
        self.armor = angel_stats["armor"]
        self.attack = angel_stats["attack"]
        self.damage_bounce = 0
        self.armor_reduction = 1
        self.damage_reduction = 1
        self.regeneration = 0
        self.resurrections = 0
        self.resurrection_value = 0
        self.explosion_on_death = False
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
        self.skill_points = player_skill_points
        self.skill_group = SkillGroup()
        self.skill_group.empty()
        self.basic_attack_animation = False
        self.resurrect_animation = False
        self.channeling = False
        self.can_fly = False
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
            self.player_left_sprites = angel_left_move_sprites
            self.player_right_sprites = angel_right_move_sprites
            self.player_left_death_sprites = angel_left_death_sprites
            self.player_right_death_sprites = angel_right_death_sprites
            self.player_left_basic_attack_sprites = angel_left_basic_attack_sprites
            self.player_right_basic_attack_sprites = angel_right_basic_attack_sprites
            self.player_left_explosion_sprites = angel_left_explosion_sprites
            self.player_right_explosion_sprites = angel_right_explosion_sprites
            self.animation_timer = 0.1
            self.basic_attack_icon = angel_basic_attack_icon
            self.in_game_skill3 = in_game_angel_skill3_icon
            self.in_game_skill6 = in_game_angel_skill6_icon
            self.in_game_skill9 = in_game_angel_skill9_icon
            self.in_game_skill12 = in_game_angel_skill12_icon
            self.basic_attack_cooldown = 1000
            self.skill3_cooldown = 5000
            self.skill6_cooldown = 15000
            self.skill9_cooldown = 30000
            self.skill12_cooldown = 10000
            self.skill3_duration = 3000
            self.skill6_duration = 4000
            self.skill9_duration = 1000
            self.skill12_duration = 3000
            self.skill1 = AngelSkill(1, (75, 75), tree_angel_skill1_icon, self.skill_group, self, True, "WINGS OF LIGHT", angel_skill1_description, 1, 2, 3)
            self.skill2 = AngelSkill(2, (75, 430), tree_angel_skill2_icon, self.skill_group, self, True, "DIVINE LEAD", angel_skill2_description, 1.1, 1.25, 1.5)
            self.skill3 = AngelSkill(3, (75, 785), tree_angel_skill3_icon, self.skill_group, self, True, "RAY OF LIGHT", angel_skill3_description, 1, 1.25, 1.5)
            self.skill4 = AngelSkill(4, (430, 75), tree_angel_skill4_icon, self.skill_group, self, False, "HOLY SWORD", angel_skill4_description, 1.1, 1.2, 1.3)
            self.skill5 = AngelSkill(5, (430, 430), tree_angel_skill5_icon, self.skill_group, self, False, "DIVINE PUNISHMENT", angel_skill5_description, 0.5, 0.75, 1)
            self.skill6 = AngelSkill(6, (430, 785), tree_angel_skill6_icon, self.skill_group, self, False, "DIVINE STRENGTH", angel_skill6_description, 0.8, 0.7, 0.6)
            self.skill7 = AngelSkill(7, (785, 75), tree_angel_skill7_icon, self.skill_group, self, False, "LIGHT BARRIER", angel_skill7_description, 0.95, 0.9, 0.85)
            self.skill8 = AngelSkill(8, (785, 430), tree_angel_skill8_icon, self.skill_group, self, False, "GUARDIAN ANGEL", angel_skill8_description, 0.3, 0.3, 0.3)
            self.skill9 = AngelSkill(9, (785, 785), tree_angel_skill9_icon, self.skill_group, self, False, "EXPLOSION", angel_skill9_description, 3, 4, 5)
            self.skill10 = AngelSkill(10, (1140, 75), tree_angel_skill10_icon, self.skill_group, self, False, "INNER PEACE", angel_skill10_description, 0.01, 0.02, 0.03)
            self.skill11 = AngelSkill(11, (1140, 430), tree_angel_skill11_icon, self.skill_group, self, False, "BACK FROM THE DEAD", angel_skill11_description, 0.4, 0.5, 0.6)
            self.skill12 = AngelSkill(12, (1140, 785), tree_angel_skill12_icon, self.skill_group, self, False, "GOD'S WRATH", angel_skill12_description, 2, 2.5, 3)
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
            self.basic_attack_icon = assassin_basic_attack_icon
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
            self.basic_attack_icon = mage_basic_attack_icon
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
            self.basic_attack_icon = necromancer_basic_attack_icon
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(WIDTH / 2 - PLAYER_WIDTH / 2, HEIGHT / 2 - PLAYER_HEIGHT / 2)
        self.passive_skill8 = AngelSkill8(self, passive_group, attack_group, enemy_group, False)
        self.passive_skill10 = AngelSkill10(self, passive_group, False)

    def move(self, up=False, down=False, left=False, right=False):
        if up:
            self.direction.y = -1
            self.handle_camera(0, -self.camera_speed, True)
        if down:
            self.direction.y = 1
            self.handle_camera(0, self.camera_speed, True)
        if right:
            self.direction.x = 1
            self.handle_camera(self.camera_speed, 0, True)
            self.current_orientation = "right"
        if left:
            self.direction.x = -1
            self.handle_camera(-self.camera_speed, 0, True)
            self.current_orientation = "left"

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
        if self.current_hp <= 0 and self.resurrections == 0:
            self.current_hp = 0
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
        if self.alive and self.channeling is False:
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
            if self.direction.x != 0 or self.direction.y != 0:
                if self.current_orientation == "right":
                    self.animation_right()
                if self.current_orientation == "left":
                    self.animation_left()
            if self.direction.x != 0 and self.direction.y != 0:
                self.direction.x /= math.sqrt(2)
                self.direction.y /= math.sqrt(2)
            new_pos = self.rect.center + self.direction * self.speed
            if math.hypot(new_pos.x - boundary_center[0], new_pos.y - boundary_center[1]) <= boundary_radius:
                self.rect.center += self.direction * self.speed
        else:
            self.handle_camera(0, self.camera.y, False)
            self.handle_camera(self.camera.x, 0, False)

    def update(self):
        self.input()
        self.player_alive()
