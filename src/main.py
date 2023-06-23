import random
import sys
import numpy as np
from random import randint
from player import Player
from redenemy import RedEnemy
from greenenemy import GreenEnemy
from slashattack import SlashAttack
from settings import *
from button import Button
from time import *


class Main:
    def __init__(self, running):
        self.player = Player()
        self.game_active = running
        self.blurred_current_state_image = blurred_current_state_image
        self.back_button = Button(810, 900, exit_button_image)
        self.transparency = 255
        attacks.clear()
        enemies.clear()
        dead_enemies.clear()
        hp_list.clear()

    def run(self):
        # MAIN GAME LOOP:
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if self.game_active is True:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.add_slash_attack()
                        if event.key == pygame.K_ESCAPE:
                            # creating blurred image for pause menu
                            screen.blit(current_state_image, (0, 0))
                            screen.blit(player_right_scaled, (810, 350))
                            pause_lv = bigger_font.render(f'Level:{self.player.player_lv}', False, 'Black')
                            pause_lv_rect = pause_lv.get_rect(center=(960, 700))
                            screen.blit(pause_lv, pause_lv_rect)
                            screen.blit(square, (0, 0))
                            pygame.display.update()
                            self.blurred_current_state_image = self.greyscale(current_state_image)
                            self.transparency = 255
                            self.game_active = False
                    if event.type == enemy_timer:
                        self.enemy_spawn()
                else:
                    if self.player.alive is True:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.game_active = True

            if self.game_active is True:
                # show background
                screen.blit(background, (0, 0))

                # controls
                if self.player.alive is True:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_w]:
                        self.player.move(up=True)
                    if keys[pygame.K_s]:
                        self.player.move(down=True)
                    if keys[pygame.K_a]:
                        self.player.move(left=True)
                    if keys[pygame.K_d]:
                        self.player.move(right=True)

                # show dropped hp on screen
                for hp in hp_list:
                    hp.update(self.player)

                # show enemies on screen
                for enemy in enemies:
                    enemy.update(self.player)

                # show death animation for dead enemies
                for dead_enemy in dead_enemies:
                    dead_enemy.death_check()
                    screen.blit(dead_enemy.image, dead_enemy.pos)

                # show player on screen
                screen.blit(self.player.image, self.player.pos)
                if self.player.current_orientation == "right" and self.player.alive is True:
                    self.player.image = player_right
                if self.player.current_orientation == "left" and self.player.alive is True:
                    self.player.image = player_left
                self.player.player_alive()

                # saving current screen
                pygame.Surface.blit(current_state_image, screen, screen_rect)

                # show hp and xp on the screen
                if self.player.death_animation is False and self.player.alive is False:
                    self.game_active = False
                if self.game_active is True and self.player.player_hp >= 0:
                    self.display_hp()
                    self.display_xp()

                # show attacks
                for attack in attacks:
                    attack.update(self.player)
            else:
                # show pause screen
                if self.player.alive is True:
                    self.transparency -= 2
                    self.pause_screen(self.transparency)
                else:
                    self.death_screen()

            # update and clock
            pygame.display.update()
            clock.tick(60)

    # FUNCTIONS:

    # adding attack to array
    def add_slash_attack(self):
        if self.player.alive is True:
            new_attack = SlashAttack(self.player)
            attacks.append(new_attack)

    # HP definition
    def display_hp(self):
        if self.player.player_hp >= player_hp:
            self.player.player_hp = player_hp
        hp_division = player_hp / 500
        hp_bar = pygame.Surface([self.player.player_hp / hp_division, 35])
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
        screen.blit(level_text, (1785, 25))
        xp = font.render(str(self.player.player_lv), False, 'Black')
        screen.blit(xp, (1402, 25))

    # show pause screen
    def pause_screen(self, transparency):
        from menu import Menu
        screen.blit(self.blurred_current_state_image, screen_rect)
        screen.blit(player_right_scaled, (810, 350))
        pause_lv = bigger_font.render(f'Level:{self.player.player_lv}', False, 'Black')
        pause_lv_rect = pause_lv.get_rect(center=(960, 700))
        screen.blit(pause_lv, pause_lv_rect)
        if self.back_button.draw(screen):
            menu = Menu()
            menu.run(running=True)

        if transparency > 100:

            square.set_alpha(transparency)
            screen.blit(square, (0, 0))
        else:
            square.set_alpha(255)


    # show death screen
    def death_screen(self):
        screen.fill("grey")
        screen.blit(player_death_scaled, (810, 350))
        screen.blit(death_text, death_text_rect)
        death_level = font.render(f'Level:{self.player.player_lv}', False, 'Black')
        death_level_rect = death_level.get_rect(center=(960, 800))
        screen.blit(death_level, death_level_rect)

    # random enemy spawns
    @staticmethod
    def enemy_spawn():
        cords = [[-100, randint(-60, 1100)], [1920, randint(-60, 1100)], [randint(-100, 1920), -60], [randint(-100, 1920), 1100]]
        chosen_cords = random.choice(cords)
        if randint(0, 9) >= 3:
            spawned_enemy = RedEnemy(chosen_cords)
        else:
            spawned_enemy = GreenEnemy(chosen_cords)
        enemies.append(spawned_enemy)

    # greyscale definition
    @staticmethod
    def greyscale(step0):
        step1 = pygame.surfarray.pixels3d(step0)
        step2 = np.dot(step1[:, :, :], [0.216, 0.587, 0.144])
        step3 = step2[..., np.newaxis]
        step4 = np.repeat(step3[:, :, :], 3, axis=2)
        return pygame.surfarray.make_surface(step4)
