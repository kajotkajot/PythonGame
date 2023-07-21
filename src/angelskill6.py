from assets import *
from settings import *


class AngelSkill6(pygame.sprite.Sprite):
    def __init__(self, player, group, timer):
        super().__init__(group)
        self.player = player
        self.timer = timer
        self.current_time = pygame.time.get_ticks()
        self.player.player_left_stand_sprites = angel_divine_left_stand_sprites
        self.player.player_right_stand_sprites = angel_divine_right_stand_sprites
        self.player.player_left_sprites = angel_divine_left_move_sprites
        self.player.player_right_sprites = angel_divine_right_move_sprites
        self.player.player_left_basic_attack_sprites = angel_divine_left_basic_attack_sprites
        self.player.player_right_basic_attack_sprites = angel_divine_right_basic_attack_sprites
        self.player.player_left_explosion_sprites = angel_divine_left_explosion_sprites
        self.player.player_right_explosion_sprites = angel_divine_right_explosion_sprites
        self.active = True

    def action(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > self.player.skill6_duration:
            self.player.player_left_stand_sprites = angel_left_stand_sprites
            self.player.player_right_stand_sprites = angel_right_stand_sprites
            self.player.player_left_sprites = angel_left_move_sprites
            self.player.player_right_sprites = angel_right_move_sprites
            self.player.player_left_basic_attack_sprites = angel_left_basic_attack_sprites
            self.player.player_right_basic_attack_sprites = angel_right_basic_attack_sprites
            self.player.player_left_explosion_sprites = angel_left_explosion_sprites
            self.player.player_right_explosion_sprites = angel_right_explosion_sprites
            self.kill()

    def update(self):
        self.action()
