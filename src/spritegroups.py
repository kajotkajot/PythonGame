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
                self.ghost_offset_pos.x = offset_pos.x + 50
                self.ghost_offset_pos.y = offset_pos.y + 50
            if sprite.alive is False and sprite.death_animation:
                self.ghost_offset_pos.y -= 1
                self.display.blit(sprite.ghost_image, self.ghost_offset_pos)
            if sprite.basic_attack_animation is False and sprite.channeling is False and sprite.resurrect_animation is False:
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
            sprite.mask = pygame.mask.from_surface(sprite.image)


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
            hp_division = sprite.max_hp / (abs(sprite.rect.left - sprite.rect.right) - 10)
            hp_bar = pygame.Surface([(sprite.hp / hp_division), 5])
            hp_bar_under = pygame.Surface([abs(sprite.rect.left - sprite.rect.right) - 10, 5])
            hp_bar.fill("red")
            hp_bar_under.fill("black")
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            self.display.blit(hp_bar_under, (offset_pos.x + 5, offset_pos.y - 15))
            self.display.blit(hp_bar, (offset_pos.x + 5, offset_pos.y - 15))
            self.display.blit(sprite.image, offset_pos)
            sprite.mask = pygame.mask.from_surface(sprite.image)


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
            sprite.mask = pygame.mask.from_surface(sprite.image)


class PassivesGroup(pygame.sprite.Group):
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
            if sprite.type == "active" and player.resurrect_animation:
                offset_pos = sprite.rect.topleft - self.offset + player.camera
                self.display.blit(sprite.image, offset_pos)
                sprite.mask = pygame.mask.from_surface(sprite.image)


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
            sprite.mask = pygame.mask.from_surface(sprite.image)


class SkillGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()

    @staticmethod
    def wrap_text(text, temp_font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            test_width, _ = temp_font.size(test_line)
            if test_width > max_width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)
        return lines

    def custom_draw(self):
        for sprite in self.sprites():
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(sprite.skill_border, (sprite.position[0] - 10, sprite.position[1] - 10))
            screen.blit(sprite.image, sprite.position)
            screen.blit(sprite.skill_point1, (sprite.position[0], sprite.position[1] + 210))
            screen.blit(sprite.skill_point2, (sprite.position[0] + 70, sprite.position[1] + 210))
            screen.blit(sprite.skill_point3, (sprite.position[0] + 140, sprite.position[1] + 210))
            if sprite.skill_availability_bool is False:
                screen.blit(sprite.skill_availability, sprite.position)
            if sprite.image.get_rect().move(sprite.position).collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1 and sprite.clicked is False:
                    for other_sprite in self.sprites():
                        other_sprite.action = False
                    sprite.clicked = True
                    sprite.action = True
            if sprite.action:
                screen.blit(sprite.skill_description_background, (1420, 65))
                screen.blit(sprite.title, (1645-sprite.title_width, 85))
                lines_of_text = self.wrap_text(sprite.description, font, 400)
                y_pos = 135
                for line in lines_of_text:
                    text_to_surface = font.render(line, False, "black")
                    screen.blit(text_to_surface, (1450, y_pos))
                    height = text_to_surface.get_height() + 5
                    y_pos += height
                if sprite.skill_availability_bool and sprite.player.skill_points > 0 and sprite.added_skill_point3 is False:
                    if sprite.add_skill_button.draw(screen) and sprite.clicked is False:
                        if sprite.player.skill_points > 0:
                            if sprite.added_skill_point1 and sprite.added_skill_point2 and sprite.added_skill_point3 is False:
                                sprite.skill_point3.fill("green")
                                sprite.added_skill_point3 = True
                                sprite.current_value = sprite.point3_value
                                sprite.level_up()
                            if sprite.added_skill_point1 and sprite.added_skill_point2 is False:
                                sprite.skill_point2.fill("green")
                                sprite.added_skill_point2 = True
                                sprite.current_value = sprite.point2_value
                                sprite.level_up()
                            if sprite.added_skill_point1 is False:
                                sprite.skill_point1.fill("green")
                                sprite.added_skill_point1 = True
                                sprite.current_value = sprite.point1_value
                                sprite.level_up()
                            sprite.player.skill_points -= 1
                        sprite.clicked = True
            if sprite.added_skill_point2 and sprite.id in [1, 2, 4, 5, 6, 9]:
                for other_sprite in self.sprites():
                    if other_sprite.id == sprite.id + 3:
                        other_sprite.skill_availability_bool = True
            if sprite.added_skill_point2 and sprite.id in [3, 7, 8]:
                skills_availability = [False for _ in range(12)]
                for other_sprite, x in zip(self.sprites(), range(12)):
                    skills_availability[x] = other_sprite.added_skill_point2
                    if sprite.id == 3:
                        if skills_availability[1] is True:
                            if other_sprite.id == sprite.id + 3:
                                other_sprite.skill_availability_bool = True
                    if sprite.id == 7:
                        if skills_availability[7] is True:
                            if other_sprite.id == sprite.id + 3:
                                other_sprite.skill_availability_bool = True
                    if sprite.id == 8:
                        if skills_availability[8] is True:
                            if other_sprite.id == sprite.id + 3:
                                other_sprite.skill_availability_bool = True
            if pygame.mouse.get_pressed()[0] == 0:
                sprite.clicked = False
