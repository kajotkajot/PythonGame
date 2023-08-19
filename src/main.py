import sys
import time
import math
import numpy as np
from random import randint
from player import Player
from src.enemyfiles.redenemy import RedEnemy
from src.enemyfiles.greenenemy import GreenEnemy
from src.angelfiles.angelbasic import AngelBasic
from src.angelfiles.angelskill3 import AngelSkill3
from src.angelfiles.angelskill6 import AngelSkill6
from src.angelfiles.angelskill9 import AngelSkill9
from src.angelfiles.angelskill12 import AngelSkill12
from settings import *
from assets import *
from button import Button
from spritegroups import PlayerGroup, EnemyGroup, DeadEnemyGroup, AttacksGroup, PassivesGroup, ItemGroup
from map import Map


class Main:
    def __init__(self, character, fps):
        # important variables
        self.game_active = False
        self.game_start = True
        self.pop_up_active = False
        self.pause_screen = False
        self.inventory_screen = False
        self.skill_tree_screen = False
        self.clicked = False
        self.fps_counter = fps

        # grey screen
        self.blurred_current_state_image = None
        self.current_state_image = current_state_image

        # buttons
        self.resume_pause_button = Button('RESUME', 780, 640, button_360x100_image, button_360x100_image_pressed)
        self.controls_button = Button('CONTROLS', 780, 770, button_360x100_image, button_360x100_image_pressed)
        self.quit_button = Button('QUIT', 780, 900, button_360x100_image, button_360x100_image_pressed)
        self.resume_inventory_button = Button('RESUME', 1465, 925, button_360x100_image, button_360x100_image_pressed)
        self.skill_button = Button('SKILLS', 95, 925, button_360x100_image, button_360x100_image_pressed)
        self.skill_tree_back_button = Button('BACK', 1465, 925, button_360x100_image, button_360x100_image_pressed)

        # transparencies and timers
        self.fps_timer = time.time()
        self.fps_count = 0
        self.fps = 0
        self.skill_announcement_timer = 0
        self.skill_announcement_transparency = 255
        self.pause_screen_transparency = 255

        # preparing groups and player
        self.enemy_group = EnemyGroup()
        self.player_group = PlayerGroup()
        self.attack_group = AttacksGroup()
        self.passive_group = PassivesGroup()
        self.item_group = ItemGroup()
        self.dead_enemy_group = DeadEnemyGroup()
        self.enemy_group.empty()
        self.player_group.empty()
        self.attack_group.empty()
        self.passive_group.empty()
        self.item_group.empty()
        self.dead_enemy_group.empty()
        self.player = Player(self.player_group, character, self.passive_group, self.attack_group, self.enemy_group)

        # enemy stats
        self.red_enemy_stats = {key: value for key, value in red_enemy_stats.items()}
        self.green_enemy_stats = {key: value for key, value in green_enemy_stats.items()}

        # skills
        self.player_lv = 0
        self.current_time, self.saved_time, self.mouse_angle = 0, 0, 0
        self.basic_timer, self.skill3_timer, self.skill6_timer, self.skill9_timer, self.skill12_timer = 0, 0, 0, 0, 0
        self.skill3, self.skill6, self.skill9, self.skill12 = None, None, None, None
        self.basic_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill3_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill6_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill9_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill12_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]

        # map and minimap
        self.map = Map()
        self.map.create_map()
        self.background_offset = pygame.math.Vector2()
        self.background_half_width = screen.get_size()[0] / 2
        self.background_half_height = screen.get_size()[1] / 2
        self.player_minimap_x = 0
        self.player_minimap_y = 0
        self.inventory_fog_of_war = pygame.Surface((970, 970), pygame.SRCALPHA)
        self.inventory_fog_of_war.fill((15, 15, 15, 0))
        self.inventory_minimap_area = None
        self.fog_surface = pygame.Surface((WIDTH+600, HEIGHT+600), pygame.SRCALPHA)
        self.prepare_fog_of_war()

        # start animation
        self.start_current_sprite = 0
        self.start_sprites = angel_right_game_start_sprites
        self.start_image = self.start_sprites[0]
        self.start_rect = self.start_image.get_rect().move(860, 440)

    def run(self):
        # MAIN GAME LOOP:
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if self.player.channeling is False:
                            if event.key == pygame.K_SPACE:
                                if self.current_time - self.basic_timer > self.player.character.basic_cooldown:
                                    self.add_attack('basic')
                            if event.key == pygame.K_e and self.player.character.skill3.added_skill_point1:
                                if self.current_time - self.skill3_timer > self.player.character.skill3_cooldown:
                                    self.add_attack('skill3')
                            if event.key == pygame.K_z and self.player.character.skill6.added_skill_point1:
                                if self.current_time - self.skill6_timer > self.player.character.skill6_cooldown:
                                    self.add_attack('skill6')
                            if event.key == pygame.K_x and self.player.character.skill9.added_skill_point1:
                                if self.current_time - self.skill9_timer > self.player.character.skill9_cooldown:
                                    self.add_attack('skill9')
                            if event.key == pygame.K_c and self.player.character.skill12.added_skill_point1:
                                if self.current_time - self.skill12_timer > self.player.character.skill12_cooldown:
                                    self.add_attack('skill12')
                        if event.key == pygame.K_ESCAPE:
                            # pause screen
                            self.screen_delay()
                            self.game_active = False
                            self.pause_screen = True
                        if event.key == pygame.K_TAB:
                            # inventory screen
                            self.screen_delay()
                            self.game_active = False
                            self.inventory_screen = True
                        if event.key == pygame.K_q:
                            # skill tree screen
                            self.screen_delay()
                            self.game_active = False
                            self.skill_tree_screen = True
                    self.clicked = False
                    self.saved_time = pygame.time.get_ticks()
                else:
                    if self.player.alive and self.pause_screen:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.game_active = True
                                self.pause_screen = False
                                self.update_timers()
                    if self.player.alive and self.inventory_screen:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                                self.game_active = True
                                self.inventory_screen = False
                                self.update_timers()
                    if self.player.alive and self.skill_tree_screen:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                                self.skill_tree_screen = False
                                self.inventory_screen = True
                            if event.key == pygame.K_q:
                                self.skill_tree_screen = False
                                self.game_active = True
                                self.update_timers()
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.clicked = False

            if self.game_active:
                # show background
                self.map.update(self.player)

                # save current ticks
                self.current_time = pygame.time.get_ticks()

                # update enemies on screen
                self.enemy_group.update()
                self.enemy_group.custom_draw(self.player)

                # show death animation for dead enemies
                self.dead_enemy_group.custom_draw(self.player)

                # update fog of war in game
                self.fog_of_war_in_game()

                # show items on screen
                self.item_group.update()
                self.item_group.custom_draw(self.player)

                # update attacks on screen
                self.attack_group.update()
                self.attack_group.custom_draw(self.player)

                # update passives of characters
                self.passive_group.update()
                self.passive_group.custom_draw(self.player)

                # update player on screen
                self.player_group.update()
                self.player_group.custom_draw(self.player)

                # saving current screen
                pygame.Surface.blit(self.current_state_image, screen, screen_rect)

                # show minimap
                self.draw_in_game_minimap()

                # update fog of war
                self.update_fog_of_war_in_inventory()

                # show fps counter
                self.draw_fps()

                # show hp and xp on the screen
                if self.player.death_animation is False and self.player.alive is False:
                    self.game_active = False
                if self.game_active and self.player.stats["health"] >= 0:
                    self.display_hp()
                    self.display_xp()
                    self.display_skills()
                if self.player.level % 5 == 0 and self.pop_up_active is False:
                    self.player.skill_points += 1
                    self.skill_announcement_timer = pygame.time.get_ticks()
                    self.player_lv = self.player.level
                    self.pop_up_active = True
                if self.pop_up_active:
                    self.display_level_up()
            else:
                # show pause screen
                if self.player.alive and self.pause_screen:
                    self.display_pause_screen()
                elif self.player.alive and self.inventory_screen:
                    self.display_inventory_screen()
                elif self.player.alive and self.skill_tree_screen:
                    self.display_skill_tree()
                else:
                    self.display_death_screen()

            if self.game_start:
                self.map.update(self.player)
                if self.map.room_group.counter >= steps_count + 7:
                    self.start_animation()

            # show custom cursor on screen
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(cursor, mouse_pos)

            # update and clock
            pygame.display.update()
            clock.tick(60)

    # FUNCTIONS:

    # adding attack to sprite group
    def add_attack(self, type_of_attack):
        if self.player.alive:
            if type_of_attack == 'basic':
                self.basic_timer = pygame.time.get_ticks()
                AngelBasic(self.player, self.attack_group, self.enemy_group)
            if type_of_attack == 'skill3':
                self.skill3_timer = pygame.time.get_ticks()
                self.skill3 = AngelSkill3(self.player, self.attack_group, self.enemy_group, self.skill3_timer)
            if type_of_attack == 'skill6':
                self.skill6_timer = pygame.time.get_ticks()
                self.skill6 = AngelSkill6(self.player, self.passive_group, self.skill6_timer)
            if type_of_attack == 'skill9':
                self.skill9_timer = pygame.time.get_ticks()
                self.skill9 = AngelSkill9(self.player, self.attack_group, self.enemy_group, self.skill9_timer)
            if type_of_attack == 'skill12':
                self.skill12_timer = pygame.time.get_ticks()
                self.skill12 = AngelSkill12(self.player, self.attack_group, self.enemy_group, self.skill12_timer)

    # display level up announcement
    def display_level_up(self):
        if self.current_time - self.skill_announcement_timer < 5000:
            self.draw_text(bigger_font, 'LEVEL ' + str(self.player_lv), black_color, self.skill_announcement_transparency, (WIDTH / 2, 10), True)
            self.draw_text(font, '+1 SKILL POINT', black_color, self.skill_announcement_transparency, (WIDTH / 2, 80), True)
            self.skill_announcement_transparency -= 1
        else:
            if self.player.level % 5 != 0:
                self.skill_announcement_transparency = 255
                self.pop_up_active = False

    # HP definition
    def display_hp(self):
        if self.player.stats["health"] >= self.player.stats["max_hp"]:
            self.player.stats["health"] = self.player.stats["max_hp"]
        hp_ratio = self.player.stats["health"] / self.player.stats["max_hp"]
        self.draw_surface([510, 45], 'Black', (20, 20))
        self.draw_surface([500, 35], 'Grey', (25, 25))
        self.draw_surface([500 * hp_ratio, 35], 'Red', (25, 25))
        self.draw_text(font, 'HP', black_color, 255, (30, 25), False)

    # XP definition
    def display_xp(self):
        if self.player.xp >= self.player.needed_player_xp:
            self.player.xp -= self.player.needed_player_xp
            self.player.level += 1
            self.player.needed_player_xp += 100
        xp_ratio = self.player.xp / self.player.needed_player_xp
        self.draw_surface([510, 45], 'Black', (1390, 20))
        self.draw_surface([500, 35], 'Grey', (1395, 25))
        self.draw_surface([500 * xp_ratio, 35], 'Blue', (1395, 25))
        self.draw_text(font, 'LEVEL', black_color, 255, (1785, 25), False)
        self.draw_text(font, str(self.player.level), black_color, 255, (1402, 25), False)

    # display skills on screen
    def display_skills(self):
        self.skill_cooldown(True, (25, 955), self.basic_polygon_points, self.basic_timer, self.player.character.basic_cooldown, None, self.player.character.basic_attack_icon)
        if self.current_time - self.basic_timer > self.player.character.basic_cooldown:
            self.basic_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill_cooldown(self.player.character.skill3.added_skill_point1, (155, 955), self.skill3_polygon_points, self.skill3_timer,
                            self.player.character.skill3_cooldown, self.player.character.skill3_duration, self.player.character.in_game_skill3)
        if self.current_time - self.skill3_timer > self.player.character.skill3_cooldown:
            self.skill3_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill_cooldown(self.player.character.skill6.added_skill_point1, (285, 955), self.skill6_polygon_points, self.skill6_timer,
                            self.player.character.skill6_cooldown, self.player.character.skill6_duration, self.player.character.in_game_skill6)
        if self.current_time - self.skill6_timer > self.player.character.skill6_cooldown:
            self.skill6_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill_cooldown(self.player.character.skill9.added_skill_point1, (415, 955), self.skill9_polygon_points, self.skill9_timer,
                            self.player.character.skill9_cooldown, None, self.player.character.in_game_skill9)
        if self.current_time - self.skill9_timer > self.player.character.skill9_cooldown:
            self.skill9_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]
        self.skill_cooldown(self.player.character.skill12.added_skill_point1, (545, 955), self.skill12_polygon_points, self.skill12_timer,
                            self.player.character.skill12_cooldown, self.player.character.skill12_duration, self.player.character.in_game_skill12)
        if self.current_time - self.skill12_timer > self.player.character.skill12_cooldown:
            self.skill12_polygon_points = [(50, 0), (100, 0), (100, 100), (0, 100), (0, 0), (50, 0), (50, 50)]

    # polygon skill cooldown
    def skill_cooldown(self, availability, position, points, timer, cooldown, duration, icon):
        if availability:
            self.draw_surface([110, 110], 'Black', (position[0] - 5, position[1] - 5))
            screen.blit(icon, position)
            if self.current_time - timer < cooldown:
                skill_polygon_surface.fill((0, 0, 0, 0))
                ratio = 6700 / cooldown
                if 50 <= points[0][0] < 100 and points[0][1] == 0:
                    points[0] = (points[0][0] + ratio, points[0][1])
                    if points[0][0] > 100:
                        points[0] = (100, 0)
                        points.remove(points[1])
                elif points[0][0] == 100 and 0 <= points[0][1] < 100:
                    points[0] = (points[0][0], points[0][1] + ratio)
                    if points[0][1] > 100:
                        points[0] = (100, 100)
                        points.remove(points[1])
                elif 0 < points[0][0] <= 100 and points[0][1] == 100:
                    points[0] = (points[0][0] - ratio, points[0][1])
                    if points[0][0] < 0:
                        points[0] = (0, 100)
                        points.remove(points[1])
                elif points[0][0] == 0 and 0 < points[0][1] <= 100:
                    points[0] = (points[0][0], points[0][1] - ratio)
                    if points[0][1] < 0:
                        points[0] = (0, 0)
                        points.remove(points[1])
                elif 0 <= points[0][0] < 50 and points[0][1] == 0:
                    points[0] = (points[0][0] + ratio, points[0][1])
                    if points[0][0] > 50:
                        points.remove(points[1])
                if cooldown - (self.current_time - timer) > 1000:
                    self.draw_text(skill_font, str(int((cooldown - (self.current_time - timer)) / 1000)), black_color, 200, (position[0]+50, position[1]+50-22), True)
                else:
                    self.draw_text(skill_font, str(round(((cooldown - (self.current_time - timer)) / 1000), 1)), black_color, 200, (position[0]+50, position[1]+50-22), True)
                if len(points) > 2:
                    pygame.draw.polygon(skill_polygon_surface, (30, 30, 30, 120), points)
                    screen.blit(skill_polygon_surface, position)
                if duration is not None:
                    if self.current_time - timer < duration:
                        duration_ratio = 1 - ((self.current_time - timer) / duration)
                        self.draw_surface([110, 20], 'Black', (position[0] - 5, position[1] - 30))
                        self.draw_surface([100 * duration_ratio, 10], 'Red', (position[0], position[1] - 25))

    # for timers of skills not to run in menu etc.
    def update_timers(self):
        current_time = pygame.time.get_ticks()
        self.basic_timer += current_time - self.saved_time
        self.skill3_timer += current_time - self.saved_time
        self.skill6_timer += current_time - self.saved_time
        self.skill9_timer += current_time - self.saved_time
        self.skill12_timer += current_time - self.saved_time
        if self.skill3:
            self.skill3.timer += current_time - self.saved_time
        if self.skill6:
            self.skill6.timer += current_time - self.saved_time
        if self.skill9:
            self.skill9.timer += current_time - self.saved_time
        if self.skill12:
            self.skill12.timer += current_time - self.saved_time

    # for slowly showing pause and inventory screen
    def screen_delay(self):
        self.blurred_current_state_image = self.greyscale(self.current_state_image)
        self.pause_screen_transparency = 255

    # show pause screen
    def display_pause_screen(self):
        from menu import Menu
        self.pause_screen_transparency -= 2
        screen.blit(self.blurred_current_state_image, screen_rect)
        if self.resume_pause_button.draw(screen) and self.clicked is False:
            self.game_active = True
            self.pause_screen = False
            self.clicked = True
        if self.controls_button.draw(screen) and self.clicked is False:
            self.clicked = True
        if self.quit_button.draw(screen) and self.clicked is False:
            menu = Menu(True, self.fps_counter)
            menu.run(running=True, menu_state='main')
            self.clicked = True
        if self.pause_screen_transparency > 0:
            grey_pause_screen.set_alpha(self.pause_screen_transparency)
            screen.blit(grey_pause_screen, (0, 0))
        else:
            grey_pause_screen.set_alpha(self.pause_screen_transparency)

    # show inventory screen
    def display_inventory_screen(self):
        self.pause_screen_transparency -= 2
        screen.blit(self.blurred_current_state_image, screen_rect)
        screen.blit(self.player.character.icon_inventory, (155, 105))
        screen.blit(health, (105, 440))
        screen.blit(attack_damage, (105, 525))
        screen.blit(armor, (105, 610))
        screen.blit(movement_speed, (105, 695))
        screen.blit(gold, (105, 780))
        self.draw_text(bigger_font, f'Level:{self.player.level}', black_color, 255, (265, 350), True)
        self.draw_text(font, f'{round(self.player.stats["health"], 1)}/{round(self.player.stats["max_hp"], 1)}', black_color, 255, (205, 475), False)
        self.draw_text(font, f'{round(self.player.stats["attack"], 1)}', black_color, 255, (205, 560), False)
        self.draw_text(font, f'{self.player.stats["armor"]}', black_color, 255, (205, 645), False)
        self.draw_text(font, f'{self.player.stats["speed"]}', black_color, 255, (205, 730), False)
        self.draw_text(font, f'{self.player.gold}', black_color, 255, (205, 815), False)
        self.draw_inventory_minimap()
        if self.skill_button.draw(screen) and self.clicked is False:
            self.inventory_screen = False
            self.skill_tree_screen = True
            self.clicked = True
        if self.resume_inventory_button.draw(screen) and self.clicked is False:
            self.game_active = True
            self.inventory_screen = False
            self.clicked = True
        if self.pause_screen_transparency > 0:
            grey_pause_screen.set_alpha(self.pause_screen_transparency)
            screen.blit(grey_pause_screen, (0, 0))
        else:
            grey_pause_screen.set_alpha(self.pause_screen_transparency)

    # update fog of war on minimap
    def update_fog_of_war_in_inventory(self):
        self.player_minimap_x = int((self.player.rect.centerx - self.map.room_group.minimap_shift[0] + self.map.room_group.minimap_shift_x) * self.map.room_group.inventory_minimap_scale)
        self.player_minimap_y = int((self.player.rect.centery - self.map.room_group.minimap_shift[1] + self.map.room_group.minimap_shift_y) * self.map.room_group.inventory_minimap_scale)
        pygame.draw.circle(self.inventory_fog_of_war, (0, 0, 0), (self.player_minimap_x, self.player_minimap_y), 120)

    # display inventory minimap
    def draw_inventory_minimap(self):
        inventory_minimap_surface.fill((50, 50, 50))
        fog_of_war_mask = pygame.mask.from_surface(self.inventory_fog_of_war).to_surface()
        temp_area = self.map.room_group.inventory_minimap_area.copy()
        temp_area.blit(fog_of_war_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.inventory_minimap_area = temp_area.copy()
        inventory_minimap_surface.blit(self.inventory_minimap_area, (0, 0))
        for sprite in self.enemy_group.sprites():
            enemy_minimap_x = int((sprite.rect.centerx - self.map.room_group.minimap_shift[0] + self.map.room_group.minimap_shift_x) * self.map.room_group.inventory_minimap_scale)
            enemy_minimap_y = int((sprite.rect.centery - self.map.room_group.minimap_shift[1] + self.map.room_group.minimap_shift_y) * self.map.room_group.inventory_minimap_scale)
            pygame.draw.circle(inventory_minimap_surface, enemy_color, (enemy_minimap_x, enemy_minimap_y), 4)
        for sprite in self.item_group.sprites():
            item_minimap_x = int((sprite.rect.centerx - self.map.room_group.minimap_shift[0] + self.map.room_group.minimap_shift_x) * self.map.room_group.inventory_minimap_scale)
            item_minimap_y = int((sprite.rect.centery - self.map.room_group.minimap_shift[1] + self.map.room_group.minimap_shift_y) * self.map.room_group.inventory_minimap_scale)
            pygame.draw.circle(inventory_minimap_surface, item_color, (item_minimap_x, item_minimap_y), 4)
        pygame.draw.circle(inventory_minimap_surface, player_color, (self.player_minimap_x, self.player_minimap_y), 4)
        camera_rect = pygame.Rect(self.player_minimap_x - (960 * self.map.room_group.inventory_minimap_scale), self.player_minimap_y - (540 * self.map.room_group.inventory_minimap_scale), (1920 * self.map.room_group.inventory_minimap_scale), (1080 * self.map.room_group.inventory_minimap_scale))
        pygame.draw.rect(inventory_minimap_surface, (0, 0, 0, 0), camera_rect, width=2)
        pygame.draw.rect(inventory_minimap_surface, (0, 0, 0, 0), (0, 0, INV_MINIMAP_WIDTH, INV_MINIMAP_HEIGHT), width=5)
        temp_area = inventory_minimap_surface.copy()
        temp_area.blit(fog_of_war_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(temp_area, (475, 55))

    # display in-game minimap
    def draw_in_game_minimap(self):
        self.background_offset.x = (self.player.rect.centerx - self.background_half_width) * self.map.room_group.in_game_minimap_scale
        self.background_offset.y = (self.player.rect.centery - self.background_half_height) * self.map.room_group.in_game_minimap_scale
        shift_x = (self.map.room_group.area_rect.x - self.map.room_group.minimap_shift_x - self.background_half_width) * self.map.room_group.in_game_minimap_scale
        shift_y = (self.map.room_group.area_rect.y - self.map.room_group.minimap_shift_y - self.background_half_height) * self.map.room_group.in_game_minimap_scale
        in_game_minimap_surface.fill((50, 50, 50))
        in_game_minimap_surface.blit(self.map.room_group.in_game_minimap_area, (125 + shift_x - self.background_offset.x, 125 + shift_y - self.background_offset.y))
        for sprite in self.enemy_group.sprites():
            enemy_minimap_x = int(sprite.rect.centerx * self.map.room_group.in_game_minimap_scale) - self.background_offset.x
            enemy_minimap_y = int((sprite.rect.centery + 420) * self.map.room_group.in_game_minimap_scale) - self.background_offset.y
            pygame.draw.circle(in_game_minimap_surface, enemy_color, (enemy_minimap_x, enemy_minimap_y), 4)
        for sprite in self.item_group.sprites():
            item_minimap_x = int(sprite.rect.centerx * self.map.room_group.in_game_minimap_scale) - self.background_offset.x
            item_minimap_y = int((sprite.rect.centery + 420) * self.map.room_group.in_game_minimap_scale) - self.background_offset.y
            pygame.draw.circle(in_game_minimap_surface, item_color, (item_minimap_x, item_minimap_y), 4)
        pygame.draw.circle(in_game_minimap_surface, player_color, (IN_GAME_MINIMAP_WIDTH/2, IN_GAME_MINIMAP_HEIGHT/2), 4)
        pygame.draw.rect(in_game_minimap_surface, (0, 0, 0, 0), (0, 0, IN_GAME_MINIMAP_WIDTH, IN_GAME_MINIMAP_HEIGHT), width=5)
        screen.blit(in_game_minimap_surface, (1650, 810))

    # display skill tree
    def display_skill_tree(self):
        self.pause_screen_transparency -= 2
        screen.blit(self.blurred_current_state_image, screen_rect)
        self.draw_text(font, f'{self.player.skill_points} skill points', 'Purple', 255, (1475, 700), False)
        for x in range(3):
            for y in range(3):
                screen.blit(arrow_right, (x*355+305, y*355+140))
        screen.blit(arrow_bottom_right, (305, 675))
        screen.blit(arrow_top_right, (1015, 675))
        screen.blit(arrow_top_right, (1015, 320))
        self.player.skill_group.custom_draw()
        if self.skill_tree_back_button.draw(screen) and self.clicked is False:
            self.inventory_screen = True
            self.skill_tree_screen = False
            self.clicked = True
        if self.pause_screen_transparency > 0:
            grey_pause_screen.set_alpha(self.pause_screen_transparency)
            screen.blit(grey_pause_screen, (0, 0))
        else:
            grey_pause_screen.set_alpha(self.pause_screen_transparency)

    # show death screen
    def display_death_screen(self):
        from menu import Menu
        screen.fill('Grey')
        self.draw_text(bigger_font, 'YOU DIED', black_color, 255, (960, 700), True)
        self.draw_text(font, f'Level:{self.player.level}', black_color, 255, (960, 810), True)
        screen.blit(self.player.character.image_death_scaled, (810, 350))
        if self.quit_button.draw(screen) and self.clicked is False:
            menu = Menu(True, self.fps_counter)
            menu.run(running=True, menu_state='main')
            self.clicked = True

    # random enemy spawns
    def enemy_spawn(self):
        for sprite in self.map.room_group.sprites():
            if sprite.main and not sprite.spawn_point:
                for i in range(randint(3, 5)):
                    cords = (randint(-200, 200) + sprite.rect.centerx, randint(-200, 200) + sprite.rect.centery)
                    if randint(0, 9) >= 3:
                        RedEnemy(cords, self.enemy_group, self.dead_enemy_group, self.attack_group, self.item_group, self.player, self.red_enemy_stats)
                    else:
                        GreenEnemy(cords, self.enemy_group, self.dead_enemy_group, self.attack_group, self.item_group, self.player, self.green_enemy_stats)

    # show start animation
    def start_animation(self):
        self.start_current_sprite += 0.1
        if self.start_current_sprite >= len(self.start_sprites):
            self.enemy_spawn()
            self.game_start = False
            self.game_active = True
        else:
            self.start_image = self.start_sprites[int(self.start_current_sprite)]
            self.start_rect = self.start_image.get_rect().move(860, 440)
        screen.blit(self.start_image, self.start_rect)

    # draw fps counter
    def draw_fps(self):
        if self.fps_counter:
            elapsed_time = time.time() - self.fps_timer
            self.fps_count += 1
            if elapsed_time >= 1:
                self.fps = self.fps_count / elapsed_time
                self.fps_count = 0
                self.fps_timer = time.time()
            self.draw_text(fps_font, f'FPS: {round(self.fps)}', white_color, 255, (1855, 0), False)

    # prepare fog of war surface
    def prepare_fog_of_war(self):
        for x in range(0, WIDTH + 600):
            for y in range(0, HEIGHT+600):
                distance = math.sqrt((x - 1260) ** 2 + (y - 840) ** 2)
                if distance <= fog_radius:
                    alpha = 0
                elif distance <= fog_radius + fog_distance:
                    alpha = int((distance - fog_radius) / fog_distance * 255)
                else:
                    alpha = 255
                self.fog_surface.set_at((x, y), (15, 15, 15, alpha))

    # draw fog of war in game
    def fog_of_war_in_game(self):
        screen.blit(self.fog_surface, (self.player.camera[0] - 300, self.player.camera[1] - 300))

    # draw surface on screen
    @staticmethod
    def draw_surface(size, color, position):
        surface = pygame.Surface(size)
        surface.fill(color)
        screen.blit(surface, position)

    # draw text on screen
    @staticmethod
    def draw_text(text_font, text, color, transparency, position, center):
        img = text_font.render(text, True, color)
        img.set_alpha(transparency)
        if center:
            img_width = img.get_width() / 2
            screen.blit(img, (position[0] - img_width, position[1]))
        else:
            screen.blit(img, position)

    # greyscale definition
    @staticmethod
    def greyscale(step0):
        step1 = pygame.surfarray.pixels3d(step0)
        step2 = np.dot(step1[:, :, :], [0.216, 0.587, 0.144])
        step3 = step2[..., np.newaxis]
        step4 = np.repeat(step3[:, :, :], 3, axis=2)
        return pygame.surfarray.make_surface(step4)
