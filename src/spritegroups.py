import math
import numpy as np
from settings import *
from assets import *
from random import randint
from scipy.spatial import Delaunay
from scipy.spatial.distance import euclidean
from room import Room
from loadingscreen import LoadingScreen


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
                self.ghost_offset_pos.x = offset_pos.x + 50
                self.ghost_offset_pos.y -= 1
                self.display.blit(sprite.ghost_image, self.ghost_offset_pos)
            if sprite.basic_attack_animation is False and sprite.channeling is False and sprite.resurrect_animation is False:
                self.display.blit(sprite.character.image, offset_pos)
            if sprite.current_orientation == "right" and sprite.alive is True:
                self.current_sprite += sprite.character.animation_timer
                if self.current_sprite >= len(sprite.character.player_right_stand_sprites):
                    self.current_sprite = 0
                sprite.character.image = sprite.character.player_right_stand_sprites[int(self.current_sprite)]
            if sprite.current_orientation == "left" and sprite.alive is True:
                self.current_sprite += sprite.character.animation_timer
                if self.current_sprite >= len(sprite.character.player_left_stand_sprites):
                    self.current_sprite = 0
                sprite.character.image = sprite.character.player_left_stand_sprites[int(self.current_sprite)]
            sprite.mask = pygame.mask.from_surface(sprite.character.image)


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
        relative_velocity_x = other_sprite.stats["speed"] * dx - sprite.stats["speed"] * dx
        relative_velocity_y = other_sprite.stats["speed"] * dy - sprite.stats["speed"] * dy
        bounce_factor = 0.0005
        impulse_magnitude = bounce_factor * (-(1 + sprite.restitution) * relative_velocity_x * relative_velocity_y) / (sprite.mass + other_sprite.mass)
        sprite.stats["speed"] -= impulse_magnitude * sprite.mass * dx
        sprite.rect.x += dx * sprite.stats["speed"]
        sprite.rect.y += dy * sprite.stats["speed"]
        other_sprite.stats["speed"] += impulse_magnitude * other_sprite.mass * dx
        other_sprite.rect.x += dx * other_sprite.stats["speed"]
        other_sprite.rect.y += dy * other_sprite.stats["speed"]

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
            hp_ratio = sprite.stats["health"] / sprite.stats["max_hp"]
            hp_bar = pygame.Surface([(abs(sprite.rect.left - sprite.rect.right) - 10) * hp_ratio, 5])
            hp_bar_under = pygame.Surface([abs(sprite.rect.left - sprite.rect.right) - 10, 5])
            hp_bar.fill("red")
            hp_bar_under.fill("black")
            offset_pos = sprite.rect.topleft - self.offset + player.camera
            if abs(player.rect.centerx - sprite.rect.centerx) < 1200 and abs(player.rect.centery - sprite.rect.centery) < 800:
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
            if player.alive:
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
            if abs(player.rect.centerx - sprite.rect.centerx) < 1200 and abs(player.rect.centery - sprite.rect.centery) < 800:
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
                    text_to_surface = font.render(line, True, black_color)
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


class RoomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.starting_offset = pygame.math.Vector2()
        self.half_width = self.display.get_size()[0] / 2
        self.half_height = self.display.get_size()[1] / 2
        self.center_points = [(0, 0) for _ in range(main_count)]
        self.counter = 0
        self.mst = None
        self.points_array = None
        self.edges = None
        self.square_positions = []
        self.area = None
        self.temp_area = None
        self.area_rect = None
        self.area_mask = None
        self.in_game_minimap_area = None
        self.in_game_minimap_scale = None
        self.inventory_minimap_area = None
        self.inventory_minimap_scale = None
        self.temp_minimap_area = None
        self.minimap_shift = None
        self.minimap_shift_x = None
        self.minimap_shift_y = None
        self.loading_screen = LoadingScreen()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def create_map(self):
        if self.counter < steps_count:
            self.steering_behaviour()
        elif self.counter == steps_count:
            self.inflate()
        elif self.counter == steps_count + 1:
            self.add_edges()
        elif self.counter == steps_count + 2:
            self.draw_corridors()
        elif self.counter == steps_count + 3:
            self.remove_squares()
        elif self.counter == steps_count + 4:
            self.find_area_size()
        elif self.counter == steps_count + 5:
            self.draw_texture()
        elif self.counter == steps_count + 6:
            self.choose_starting_room()
        elif self.counter == steps_count + 7:
            self.prepare_minimap_info()

    def steering_behaviour(self):
        for sprite in self.sprites():
            separation_force = pygame.Vector2(0, 0)
            for another_sprite in self.sprites():
                if sprite != another_sprite and sprite.rect.colliderect(another_sprite.rect):
                    distance = sprite.position.distance_to(another_sprite.position)
                    diff = sprite.position - another_sprite.position
                    if diff[0] != 0 and diff[1] != 0:
                        diff = diff.normalize() / distance
                    separation_force += diff
                    if separation_force.length() > 0:
                        separation_force = separation_force.normalize() * 2
                        sprite.velocity += separation_force
                    sprite.position += sprite.velocity
                    sprite.rect.center = sprite.position
            if sprite.main:
                self.center_points[sprite.id] = sprite.rect.center
        self.delaunay_triangulation()

    def delaunay_triangulation(self):
        self.points_array = np.array(self.center_points)
        triangulation = Delaunay(self.points_array)
        self.edges = []
        for simplex in triangulation.simplices:
            for i in range(3):
                u, v = simplex[i], simplex[(i + 1) % 3]
                dist = euclidean(self.points_array[u], self.points_array[v])
                self.edges.append((u, v, dist))
        num_vertices = len(self.center_points)
        self.mst = self.kruskal_mst(self.edges, num_vertices)
        self.counter += 1

    @staticmethod
    def kruskal_mst(edges, num_vertices):
        edges = sorted(edges, key=lambda z: z[2])
        parent = list(range(num_vertices))
        mst = []

        def find_root(node):
            while parent[node] != node:
                node = parent[node]
            return node

        for u, v, weight in edges:
            root_u = find_root(u)
            root_v = find_root(v)
            if root_u != root_v:
                mst.append((u, v, weight))
                parent[root_u] = root_v

        return mst

    def inflate(self):
        for sprite in self.sprites():
            sprite.width = sprite.width * 1.5
            sprite.height = sprite.height * 1.5
            sprite.image = pygame.Surface([sprite.width, sprite.height])
            sprite.rect = sprite.image.get_rect().move(sprite.rect.x, sprite.rect.y)
        self.counter += 1

    def add_edges(self):
        result_list = [y for y in self.edges if y not in self.mst]
        for i in range(int(len(result_list) * 0.15)):
            num = randint(0, int(len(result_list)) - 1)
            self.mst.append(result_list[num])
            result_list.remove(result_list[num])
        self.counter += 1

    def draw_corridors(self):
        lines = []
        for u, v, _ in self.mst:
            if randint(0, 1) == 0:
                lines.append((self.points_array[u], (self.points_array[u][0], self.points_array[v][1])))
                lines.append((self.points_array[v], (self.points_array[u][0], self.points_array[v][1])))
            else:
                lines.append((self.points_array[u], (self.points_array[v][0], self.points_array[u][1])))
                lines.append((self.points_array[v], (self.points_array[v][0], self.points_array[u][1])))
        for line in lines:
            for sprite in self.sprites():
                clipped_line = sprite.rect.clipline(line)
                if clipped_line:
                    if not sprite.main:
                        sprite.corridor = True
            if abs(line[0][0]-line[1][0]) == 0:
                area = Room(self, corridor_size, abs(line[0][1] - line[1][1]) + corridor_size, False, True, False, None)
                self.move_corridor(area, line)
            elif abs(line[0][1]-line[1][1]) == 0:
                area = Room(self, abs(line[0][0] - line[1][0]) + corridor_size, corridor_size, False, True, False, None)
                self.move_corridor(area, line)
        self.counter += 1

    @staticmethod
    def move_corridor(area, line):
        if line[0][0] < line[1][0]:
            if line[0][1] < line[1][1]:
                area.rect = area.image.get_rect().move((line[0][0], line[0][1]))
            else:
                area.rect = area.image.get_rect().move((line[0][0], line[1][1]))
        else:
            if line[0][1] < line[1][1]:
                area.rect = area.image.get_rect().move((line[1][0], line[0][1]))
            else:
                area.rect = area.image.get_rect().move((line[1][0], line[1][1]))

    def remove_squares(self):
        for sprite in self.sprites():
            if not sprite.main and not sprite.corridor:
                self.remove(sprite)
        self.counter += 1

    def find_area_size(self):
        for sprite in self.sprites():
            self.square_positions.append((sprite.rect.x, sprite.rect.y))
        left = min(x for x, _ in self.square_positions)
        top = min(x for _, x in self.square_positions)
        right = max(x for x, _ in self.square_positions)
        bottom = max(x for _, x in self.square_positions)
        self.temp_area = pygame.Surface([right - left + stddev, bottom - top + stddev], pygame.SRCALPHA)
        self.temp_area.fill((0, 0, 0, 0))
        self.area_rect = self.temp_area.get_rect().move((left, top))
        for sprite in self.sprites():
            self.temp_area.blit(sprite.image, (sprite.rect.x - left, sprite.rect.y - top))
        self.area_mask = pygame.mask.from_surface(self.temp_area).to_surface()
        self.temp_area.set_colorkey((0, 0, 0))
        self.counter += 1

    def draw_texture(self):
        for x in range(0, self.temp_area.get_width(), floor_texture.get_width()):
            for y in range(0, self.temp_area.get_height(), floor_texture.get_height()):
                self.temp_area.blit(floor_texture, (x, y))
        self.temp_area.blit(self.area_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.area = self.temp_area.copy()
        self.counter += 1

    def choose_starting_room(self):
        random_room = randint(0, len(self.center_points) - 1)
        for sprite in self.sprites():
            if sprite.main and sprite.id == random_room:
                sprite.spawn_point = True
                random_point = sprite.rect.center
                self.starting_offset = (960 - random_point[0], 540 - random_point[1])
        self.area_rect.x += self.starting_offset[0]
        self.area_rect.y += self.starting_offset[1]
        for sprite in self.sprites():
            sprite.rect.x += self.starting_offset[0]
            sprite.rect.y += self.starting_offset[1]
        self.minimap_shift = self.area_rect
        self.counter += 1

    def prepare_minimap_info(self):
        area_width = self.area.get_width()
        area_height = self.area.get_height()
        if area_width >= area_height:
            self.minimap_shift_x = 0
            self.minimap_shift_y = (area_width - area_height) / 2
            self.temp_minimap_area = pygame.Surface((area_width, area_width))
            self.temp_minimap_area.blit(self.area, (0, 0 + self.minimap_shift_y))
            self.inventory_minimap_scale = INV_MINIMAP_WIDTH / area_width
            self.in_game_minimap_scale = 1000 / area_width
        else:
            self.minimap_shift_x = (area_height - area_width) / 2
            self.minimap_shift_y = 0
            self.temp_minimap_area = pygame.Surface((area_height, area_height))
            self.temp_minimap_area.blit(self.area, (0 + self.minimap_shift_x, 0))
            self.inventory_minimap_scale = INV_MINIMAP_HEIGHT / area_height
            self.in_game_minimap_scale = 1000 / area_height
        self.temp_minimap_area.set_colorkey((0, 0, 0))
        self.inventory_minimap_area = self.temp_minimap_area.copy()
        self.inventory_minimap_area = pygame.transform.scale(self.inventory_minimap_area, (970, 970))
        self.in_game_minimap_area = self.temp_minimap_area.copy()
        self.in_game_minimap_area = pygame.transform.scale(self.in_game_minimap_area, (1000, 1000))
        self.counter += 1

    def custom_draw(self, player):
        if self.area is None:
            self.loading_screen.run()
        else:
            self.display.fill((50, 50, 50))
            self.center_target_camera(player)
            offset_pos = self.area_rect.topleft - self.offset + player.camera
            screen.blit(self.area, offset_pos)
