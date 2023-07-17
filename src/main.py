import random
import sys
import numpy as np
from random import randint
from player import Player
from redenemy import RedEnemy
from greenenemy import GreenEnemy
from swordsmanbasicattack import SwordsmanBasicAttack
from settings import *
from assets import *
from button import Button
from spritegroups import EnemyGroup, PlayerGroup, AttacksGroup, ItemGroup, DeadEnemyGroup


class Main:
    def __init__(self, running, character):
        self.game_active = running
        self.blurred_current_state_image = blurred_current_state_image
        self.resume_pause_button = Button('RESUME', 780, 640, button_360x100_image, button_360x100_image_pressed)
        self.controls_button = Button('CONTROLS', 780, 770, button_360x100_image, button_360x100_image_pressed)
        self.quit_button = Button('QUIT', 780, 900, button_360x100_image, button_360x100_image_pressed)
        self.resume_inventory_button = Button('RESUME', 1465, 925, button_360x100_image, button_360x100_image_pressed)
        self.skill_button = Button('SKILLS', 95, 925, button_360x100_image, button_360x100_image_pressed)
        self.skill_tree_back_button = Button('BACK', 1465, 925, button_360x100_image, button_360x100_image_pressed)
        self.skill_announcement_timer = 0
        self.skill_announcement_transparency = 255
        self.player_lv = 0
        self.pop_up_active = False
        self.pause_screen = False
        self.inventory_screen = False
        self.skill_tree_screen = False
        self.pause_screen_transparency = 255
        self.clicked = False
        self.enemy_group = EnemyGroup()
        self.player_group = PlayerGroup()
        self.attack_group = AttacksGroup()
        self.item_group = ItemGroup()
        self.dead_enemy_group = DeadEnemyGroup()
        self.enemy_group.empty()
        self.player_group.empty()
        self.attack_group.empty()
        self.item_group.empty()
        self.dead_enemy_group.empty()
        self.player = Player(self.player_group, character)
        self.current_time = 0
        self.basic_attack_timer = 0
        self.basic_attack_cooldown = self.player.basic_attack_cooldown
        self.background_offset = pygame.math.Vector2()
        self.background_half_width = screen.get_size()[0] / 2
        self.background_half_height = screen.get_size()[1] / 2

    def run(self):
        # MAIN GAME LOOP:
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if self.current_time - self.basic_attack_timer > self.basic_attack_cooldown:
                                self.add_basic_attack()
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
                    if event.type == enemy_timer:
                        self.enemy_spawn()
                    self.clicked = False
                else:
                    if self.player.alive and self.pause_screen:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.game_active = True
                                self.pause_screen = False
                    if self.player.alive and self.inventory_screen:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                                self.game_active = True
                                self.inventory_screen = False
                    if self.player.alive and self.skill_tree_screen:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                                self.skill_tree_screen = False
                                self.inventory_screen = True
                            if event.key == pygame.K_q:
                                self.skill_tree_screen = False
                                self.game_active = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.clicked = False

            if self.game_active is True:
                # show background
                self.display_background()

                # save current ticks
                self.current_time = pygame.time.get_ticks()

                # update enemies on screen
                self.enemy_group.update()
                self.enemy_group.custom_draw(self.player)

                # show death animation for dead enemies
                self.dead_enemy_group.custom_draw(self.player)

                # show items on screen
                self.item_group.update()
                self.item_group.custom_draw(self.player)

                # update player on screen
                self.player_group.update()
                self.player_group.custom_draw(self.player)

                # update attacks on screen
                self.attack_group.update()
                self.attack_group.custom_draw(self.player)

                # saving current screen
                pygame.Surface.blit(current_state_image, screen, screen_rect)

                # show minimap
                self.draw_in_game_minimap()

                # show hp and xp on the screen
                if self.player.death_animation is False and self.player.alive is False:
                    self.game_active = False
                if self.game_active and self.player.player_current_hp >= 0:
                    self.display_hp()
                    self.display_xp()
                    self.display_skills()
                if self.player.player_lv % 5 == 0 and self.pop_up_active is False:
                    self.player.skill_points += 1
                    self.skill_announcement_timer = pygame.time.get_ticks()
                    self.player_lv = self.player.player_lv
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

                # show custom cursor on screen
                mouse_pos = pygame.mouse.get_pos()
                screen.blit(cursor, mouse_pos)

            # update and clock
            pygame.display.update()
            clock.tick(60)

    # FUNCTIONS:

    # adding attack to sprite group
    def add_basic_attack(self):
        if self.player.alive:
            self.basic_attack_timer = pygame.time.get_ticks()
            SwordsmanBasicAttack(self.player, self.attack_group)

    # display level up announcement
    def display_level_up(self):
        if self.current_time - self.skill_announcement_timer < 5000:
            level_text = bigger_font.render("LEVEL " + str(self.player_lv), False, 'Black')
            skill_text = font.render("+1 SKILL POINT", False, 'Black')
            level_text_width = level_text.get_width()/2
            skill_text_width = skill_text.get_width()/2
            level_text.set_alpha(self.skill_announcement_transparency)
            skill_text.set_alpha(self.skill_announcement_transparency)
            self.skill_announcement_transparency -= 1
            screen.blit(level_text, (WIDTH/2-level_text_width, 10))
            screen.blit(skill_text, (WIDTH/2-skill_text_width, 80))
        else:
            if self.player.player_lv % 5 != 0:
                self.skill_announcement_transparency = 255
                self.pop_up_active = False

    # HP definition
    def display_hp(self):
        if self.player.player_current_hp >= self.player.player_max_hp:
            self.player.player_current_hp = self.player.player_max_hp
        hp_division = self.player.player_max_hp / 500
        hp_bar = pygame.Surface([self.player.player_current_hp / hp_division, 35])
        hp_bar_under = pygame.Surface([500, 35])
        hp_bar_border = pygame.Surface([510, 45])
        hp_bar.fill("red")
        hp_bar_under.fill("grey")
        hp_bar_border.fill("black")
        screen.blit(hp_bar_border, (20, 20))
        screen.blit(hp_bar_under, (25, 25))
        screen.blit(hp_bar, (25, 25))
        screen.blit(hp_text, (30, 25))

    # XP definition
    def display_xp(self):
        if self.player.player_xp >= 1000:
            self.player.player_xp -= needed_player_xp
            self.player.player_lv += 1
        xp_division = needed_player_xp / 2000
        xp_bar = pygame.Surface([xp_division * self.player.player_xp, 35])
        xp_bar_under = pygame.Surface([500, 35])
        xp_bar_border = pygame.Surface([510, 45])
        xp_bar.fill("blue")
        xp_bar_under.fill("grey")
        xp_bar_border.fill("black")
        screen.blit(xp_bar_border, (1390, 20))
        screen.blit(xp_bar_under, (1395, 25))
        screen.blit(xp_bar, (1395, 25))
        screen.blit(xp_text, (1785, 25))
        xp = font.render(str(self.player.player_lv), False, 'Black')
        screen.blit(xp, (1402, 25))

    # skills definition
    def display_skills(self):
        skill_border = pygame.Surface([110, 110])
        skill_border.fill("black")
        screen.blit(skill_border, (20, 950))
        screen.blit(self.player.basic_attack_icon, (25, 955))
        if self.current_time - self.basic_attack_timer < self.basic_attack_cooldown:
            skill_division = self.current_time - self.basic_attack_timer
            skill1_loading = pygame.Surface([100 - (skill_division/10), 100])
            skill1_loading.fill((30, 30, 30, 255))
            skill1_loading.set_alpha(100)
            screen.blit(skill1_loading, (25, 955))

    # for slowly showing pause and inventory screen
    def screen_delay(self):
        self.blurred_current_state_image = self.greyscale(current_state_image)
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
            menu = Menu(True)
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
        screen.blit(self.player.image_right_scaled, (105, 55))
        pause_lv = bigger_font.render(f'Level:{self.player.player_lv}', False, 'Black')
        pause_lv_width = pause_lv.get_width()
        inventory_hp = font.render(f'{self.player.player_current_hp}/{self.player.player_max_hp}', False, 'Black')
        inventory_attack_damage = font.render(f'{self.player.player_attack}', False, 'Black')
        inventory_armor = font.render(f'{self.player.player_armor}', False, 'Black')
        inventory_gold = font.render(f'{self.player.player_gold}', False, 'Black')
        screen.blit(pause_lv, (115+(300-pause_lv_width)/2, 350))
        screen.blit(health, (105, 445))
        screen.blit(attack_damage, (105, 555))
        screen.blit(armor, (105, 665))
        screen.blit(gold, (105, 775))
        screen.blit(inventory_hp, (205, 480))
        screen.blit(inventory_attack_damage, (205, 590))
        screen.blit(inventory_armor, (205, 700))
        screen.blit(inventory_gold, (205, 810))
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

    # display inventory minimap
    def draw_inventory_minimap(self):
        inventory_minimap_surface.blit(inventory_minimap_background, (0, 0))
        player_minimap_x = int((self.player.rect.x + 4040) * inventory_minimap_scale_x) + 4
        player_minimap_y = int((self.player.rect.y + 4460) * inventory_minimap_scale_y) + 4
        for sprite in self.enemy_group.sprites():
            enemy_minimap_x = int((sprite.rect.x + 4040) * inventory_minimap_scale_x) + 4
            enemy_minimap_y = int((sprite.rect.y + 4460) * inventory_minimap_scale_y) + 4
            pygame.draw.circle(inventory_minimap_surface, enemy_color, (enemy_minimap_x, enemy_minimap_y), 4)
        for sprite in self.item_group.sprites():
            item_minimap_x = int((sprite.rect.x + 4040) * inventory_minimap_scale_x) + 4
            item_minimap_y = int((sprite.rect.y + 4460) * inventory_minimap_scale_y) + 4
            pygame.draw.circle(inventory_minimap_surface, item_color, (item_minimap_x, item_minimap_y), 4)
        pygame.draw.circle(inventory_minimap_surface, player_color, (player_minimap_x, player_minimap_y), 4)
        camera_rect = pygame.Rect(player_minimap_x - (960 * inventory_minimap_scale_x), player_minimap_y - (540 * inventory_minimap_scale_y), (1920 * inventory_minimap_scale_x) + 4, (1080 * inventory_minimap_scale_y) + 4)
        pygame.draw.rect(inventory_minimap_surface, (0, 0, 0, 0), camera_rect, width=2)
        pygame.draw.rect(inventory_minimap_surface, (0, 0, 0, 0), (0, 0, INV_MINIMAP_WIDTH, INV_MINIMAP_HEIGHT), width=5)
        screen.blit(inventory_minimap_surface, (475, 55))

    # display in-game minimap
    def draw_in_game_minimap(self):
        self.background_offset.x = (self.player.rect.centerx - self.background_half_width) * in_game_minimap_scale_x
        self.background_offset.y = (self.player.rect.centery - self.background_half_height) * in_game_minimap_scale_y
        in_game_minimap_surface.blit(in_game_minimap_background, ((0 - 375 - self.background_offset.x), (0 - 375 - self.background_offset.y)))
        for sprite in self.enemy_group.sprites():
            enemy_minimap_x = int((sprite.rect.x + 350) * in_game_minimap_scale_x) - self.background_offset.x
            enemy_minimap_y = int((sprite.rect.y + 750) * in_game_minimap_scale_y) - self.background_offset.y
            pygame.draw.circle(in_game_minimap_surface, enemy_color, (enemy_minimap_x, enemy_minimap_y), 4)
        for sprite in self.item_group.sprites():
            item_minimap_x = int((sprite.rect.x + 350) * in_game_minimap_scale_x) - self.background_offset.x
            item_minimap_y = int((sprite.rect.y + 750) * in_game_minimap_scale_y) - self.background_offset.y
            pygame.draw.circle(in_game_minimap_surface, item_color, (item_minimap_x, item_minimap_y), 4)
        pygame.draw.circle(in_game_minimap_surface, player_color, (IN_GAME_MINIMAP_WIDTH/2, IN_GAME_MINIMAP_HEIGHT/2), 4)
        pygame.draw.rect(in_game_minimap_surface, (0, 0, 0, 0), (0, 0, IN_GAME_MINIMAP_WIDTH, IN_GAME_MINIMAP_HEIGHT), width=5)
        screen.blit(in_game_minimap_surface, (1650, 810))

    # display skill tree
    def display_skill_tree(self):
        self.pause_screen_transparency -= 2
        screen.blit(self.blurred_current_state_image, screen_rect)
        skill_point_text = font.render(f'{self.player.skill_points} skill points', False, 'Purple')
        screen.blit(skill_point_text, (1475, 700))
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
        screen.fill("grey")
        screen.blit(death_text, death_text_rect)
        death_level = font.render(f'Level:{self.player.player_lv}', False, 'Black')
        death_level_rect = death_level.get_rect(center=(960, 800))
        screen.blit(death_level, death_level_rect)
        screen.blit(self.player.image_death_scaled, (810, 350))
        if self.quit_button.draw(screen) and self.clicked is False:
            menu = Menu(True)
            menu.run(running=True, menu_state='main')
            self.clicked = True

    # background definition
    def display_background(self):
        self.background_offset.x = self.player.rect.centerx - self.background_half_width
        self.background_offset.y = self.player.rect.centery - self.background_half_height
        offset_pos = [-4040, -4460] - self.background_offset + self.player.camera
        screen.blit(arena_background, offset_pos)

    # random enemy spawns
    def enemy_spawn(self):
        cords = [[self.player.rect.left - 1310, randint(self.player.rect.top - 850, self.player.rect.bottom + 810)],
                 [self.player.rect.right + 1210, randint(self.player.rect.top - 850, self.player.rect.bottom + 810)],
                 [randint(self.player.rect.left - 1310, self.player.rect.right + 1210), self.player.rect.top - 850],
                 [randint(self.player.rect.left - 1310, self.player.rect.right + 1210), self.player.rect.bottom + 810]]
        chosen_cords = random.choice(cords)
        if randint(0, 9) >= 3:
            RedEnemy(chosen_cords, self.enemy_group, self.dead_enemy_group, self.attack_group, self.item_group, self.player)
        else:
            GreenEnemy(chosen_cords, self.enemy_group, self.dead_enemy_group, self.attack_group, self.item_group, self.player)

    # greyscale definition
    @staticmethod
    def greyscale(step0):
        step1 = pygame.surfarray.pixels3d(step0)
        step2 = np.dot(step1[:, :, :], [0.216, 0.587, 0.144])
        step3 = step2[..., np.newaxis]
        step4 = np.repeat(step3[:, :, :], 3, axis=2)
        return pygame.surfarray.make_surface(step4)
