from settings import *
from assets import *


class PlayerGroup(pygame.sprite.GroupSingle):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display.get_size()[0] / 2
        self.half_height = self.display.get_size()[1] / 2
        self.current_sprite = 0

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            self.display.blit(sprite.image, offset_pos)
            if sprite.current_orientation == "right" and sprite.alive is True:
                self.current_sprite += 0.05
                if self.current_sprite >= len(sprite.player_right_stand_sprites):
                    self.current_sprite = 0
                sprite.image = sprite.player_right_stand_sprites[int(self.current_sprite)]
            if sprite.current_orientation == "left" and sprite.alive is True:
                self.current_sprite += 0.05
                if self.current_sprite >= len(sprite.player_left_stand_sprites):
                    self.current_sprite = 0
                sprite.image = sprite.player_left_stand_sprites[int(self.current_sprite)]


class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display.get_size()[0] / 2
        self.half_height = self.display.get_size()[1] / 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            hp_division = red_enemy_hp / (abs(sprite.rect.left - sprite.rect.right) - 10)
            hp_bar = pygame.Surface([(sprite.hp / hp_division), 5])
            hp_bar_under = pygame.Surface([abs(sprite.rect.left - sprite.rect.right) - 10, 5])
            hp_bar.fill("red")
            hp_bar_under.fill("black")
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            self.display.blit(hp_bar_under, (offset_pos.x + 5, offset_pos.y - 15))
            self.display.blit(hp_bar, (offset_pos.x + 5, offset_pos.y - 15))
            self.display.blit(sprite.image, offset_pos)


class DeadEnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display.get_size()[0] / 2
        self.half_height = self.display.get_size()[1] / 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            sprite.death_check()
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            self.display.blit(sprite.image, offset_pos)


class AttacksGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display.get_size()[0] / 2
        self.half_height = self.display.get_size()[1] / 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            self.display.blit(sprite.image, offset_pos)


class HealthGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display.get_size()[0] / 2
        self.half_height = self.display.get_size()[1] / 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            shadow_offset_pos = sprite.origin.topleft - self.offset + player.camera
            self.display.blit(sprite.shadow, shadow_offset_pos)
            self.display.blit(sprite.image, offset_pos)
