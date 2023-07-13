import math
from settings import *
from assets import *


class PlayerGroup(pygame.sprite.GroupSingle):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.ghost_offset_pos = pygame.math.Vector2()
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
            if sprite.alive and sprite.death_animation is False:
                self.ghost_offset_pos.x = offset_pos.x
                self.ghost_offset_pos.y = offset_pos.y
            if sprite.alive is False and sprite.death_animation:
                self.ghost_offset_pos.y -= 1
                self.display.blit(sprite.ghost_image, self.ghost_offset_pos)
            self.display.blit(sprite.image, offset_pos)
            if sprite.current_orientation == "right" and sprite.alive is True:
                self.current_sprite += sprite.animation_timer
                if self.current_sprite >= len(sprite.player_right_stand_sprites):
                    self.current_sprite = 0
                sprite.image = sprite.player_right_stand_sprites[int(self.current_sprite)]
            if sprite.current_orientation == "left" and sprite.alive is True:
                self.current_sprite += sprite.animation_timer
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

    @staticmethod
    def handle_enemy_collision(sprite, other_sprite):
        dx = other_sprite.rect.centerx - sprite.rect.centerx
        dy = other_sprite.rect.centery - sprite.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance*20
            dy /= distance*20
        relative_velocity_x = other_sprite.speed * dx - sprite.speed * dx
        relative_velocity_y = other_sprite.speed * dy - sprite.speed * dy
        bounce_factor = 0.0005
        impulse_magnitude = bounce_factor * (-(1 + sprite.restitution) * relative_velocity_x * relative_velocity_y) / (sprite.mass + other_sprite.mass)
        sprite.speed -= impulse_magnitude * sprite.mass * dx
        sprite.rect.x += dx * sprite.speed
        sprite.rect.y += dy * sprite.speed
        other_sprite.speed += impulse_magnitude * other_sprite.mass * dx
        other_sprite.rect.x += dx * other_sprite.speed
        other_sprite.rect.y += dy * other_sprite.speed

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            dx = sprite.rect.centerx - player.rect.centerx
            dy = sprite.rect.centery - player.rect.centery
            distance = math.hypot(dx, dy)
            sorted_enemies = sorted(self.sprites(), key=lambda sprites: distance)
            for other_sprite in sorted_enemies:
                if other_sprite != sprite:
                    if sprite.hit_box.colliderect(other_sprite.hit_box):
                        self.handle_enemy_collision(sprite, other_sprite)
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


class ItemGroup(pygame.sprite.Group):
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
            if sprite.attracted is False:
                self.display.blit(sprite.shadow, shadow_offset_pos)
            self.display.blit(sprite.image, offset_pos)
