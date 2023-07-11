import sys
from settings import *
from assets import *
from button import Button


class Menu:
    def __init__(self, clicked):
        # main menu buttons
        self.start_button = Button('START', 585, 650, button_750x100_image, button_750x100_image_pressed)
        self.settings_button = Button('SETTINGS', 585, 780, button_750x100_image, button_750x100_image_pressed)
        self.credits_button = Button('CREDITS', 585, 910, button_360x100_image, button_360x100_image_pressed)
        self.exit_button = Button('EXIT', 975, 910, button_360x100_image, button_360x100_image_pressed)

        # settings buttons
        self.resolution1920x1080_button = Button('1920x1080', 585, 650, button_750x100_image, button_750x100_image_pressed)
        self.resolution1280x720_button = Button('1280x720', 585, 780, button_750x100_image, button_750x100_image_pressed)
        self.settings_back_button = Button('BACK', 585, 910, button_750x100_image, button_750x100_image_pressed)

        # character choice buttons
        self.knight_button = Button('', 75, 75, button_540x540_image, button_540x540_image_pressed)
        self.angel_button = Button('', 690, 75, button_540x540_image, button_540x540_image_pressed)
        self.assassin_button = Button('', 1305, 75, button_540x540_image, button_540x540_image_pressed)
        self.mage_button = Button('', 1920, 75, button_540x540_image, button_540x540_image_pressed)
        self.necromancer_button = Button('', 2535, 75, button_540x540_image, button_540x540_image_pressed)
        self.swordsman_button = Button('', 3150, 75, button_540x540_image, button_540x540_image_pressed)
        self.left_arrow_button = Button('', 75, 635, button_arrow_image_left, button_arrow_image_left_pressed)
        self.right_arrow_button = Button('', 1745, 635, button_arrow_image_right, button_arrow_image_right_pressed)
        self.play_button = Button('PLAY', 1485, 905, button_360x100_image, button_360x100_image_pressed)
        self.character_back_button = Button('BACK', 75, 905, button_360x100_image, button_360x100_image_pressed)

        # buttons settings
        self.character_button_list = [self.knight_button, self.angel_button, self.assassin_button, self.mage_button, self.necromancer_button, self.swordsman_button]
        self.characters_image_origin_positions = [145, 760, 1375, 1990, 2605, 3220]
        self.characters_image_positions = [145, 760, 1375, 1990, 2605, 3220]
        self.characters_buttons_positions = [75, 690, 1305, 1920, 2535, 3150]
        self.character_menu_position = 0

        # important variables
        self.clicked = clicked
        self.chosen_character = ''
        self.chose_made = False

    def run(self, running, menu_state):
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = False
                if event.type == pygame.KEYDOWN:
                    if menu_state == 'character_choice':
                        if event.key == pygame.K_d:
                            self.character_menu_position += 1
                            self.character_choice('right')
                        if event.key == pygame.K_a:
                            self.character_menu_position -= 1
                            self.character_choice('left')

            if menu_state == 'main':
                screen.fill((85, 75, 62))
                if self.start_button.draw(screen) and self.clicked is False:
                    menu_state = 'character_choice'
                    self.clicked = True

                if self.settings_button.draw(screen) and self.clicked is False:
                    menu_state = 'settings'
                    self.clicked = True

                if self.credits_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.exit_button.draw(screen) and self.clicked is False:
                    sys.exit()

            if menu_state == 'settings':
                screen.fill((85, 75, 62))
                if self.resolution1280x720_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.resolution1920x1080_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.settings_back_button.draw(screen) and self.clicked is False:
                    menu_state = 'main'
                    self.clicked = True

            if menu_state == 'character_choice':
                from main import Main
                screen.fill((85, 75, 62))
                if self.knight_button.draw(screen) and self.clicked is False:
                    self.chosen_character = 'Knight'
                    for button in self.character_button_list:
                        button.image_not_pressed = button.saved_image_not_pressed
                    self.knight_button.image_not_pressed = self.knight_button.saved_image_pressed
                    self.chose_made = True
                    self.clicked = True
                screen.blit(knight_right_menu, (self.characters_image_positions[0], 135))

                if self.angel_button.draw(screen) and self.clicked is False:
                    self.chosen_character = 'Angel'
                    for button in self.character_button_list:
                        button.image_not_pressed = button.saved_image_not_pressed
                    self.angel_button.image_not_pressed = self.angel_button.saved_image_pressed
                    self.chose_made = True
                    self.clicked = True
                screen.blit(angel_right_menu, (self.characters_image_positions[1], 135))

                if self.assassin_button.draw(screen) and self.clicked is False:
                    self.chosen_character = 'Assassin'
                    for button in self.character_button_list:
                        button.image_not_pressed = button.saved_image_not_pressed
                    self.assassin_button.image_not_pressed = self.assassin_button.saved_image_pressed
                    self.chose_made = True
                    self.clicked = True
                screen.blit(assassin_right_menu, (self.characters_image_positions[2], 135))

                if self.mage_button.draw(screen) and self.clicked is False:
                    self.chosen_character = 'Mage'
                    for button in self.character_button_list:
                        button.image_not_pressed = button.saved_image_not_pressed
                    self.mage_button.image_not_pressed = self.mage_button.saved_image_pressed
                    self.chose_made = True
                    self.clicked = True
                screen.blit(mage_right_menu, (self.characters_image_positions[3], 135))

                if self.necromancer_button.draw(screen) and self.clicked is False:
                    self.chosen_character = 'Necromancer'
                    for button in self.character_button_list:
                        button.image_not_pressed = button.saved_image_not_pressed
                    self.necromancer_button.image_not_pressed = self.necromancer_button.saved_image_pressed
                    self.chose_made = True
                    self.clicked = True
                screen.blit(necromancer_right_menu, (self.characters_image_positions[4], 135))

                if self.swordsman_button.draw(screen) and self.clicked is False:
                    self.chosen_character = 'Swordsman'
                    for button in self.character_button_list:
                        button.image_not_pressed = button.saved_image_not_pressed
                    self.swordsman_button.image_not_pressed = self.swordsman_button.saved_image_pressed
                    self.chose_made = True
                    self.clicked = True
                screen.blit(swordsman_right_menu, (self.characters_image_positions[5], 135))

                if self.character_menu_position > 0:
                    if self.left_arrow_button.draw(screen) and self.clicked is False:
                        self.character_menu_position -= 1
                        self.character_choice('left')
                        self.clicked = True

                if self.character_menu_position < len(self.characters_image_positions) - 3:
                    if self.right_arrow_button.draw(screen) and self.clicked is False:
                        self.character_menu_position += 1
                        self.character_choice('right')
                        self.clicked = True

                if self.play_button.draw(screen) and self.clicked is False and self.chose_made is True:
                    main = Main(True, self.chosen_character)
                    main.run()
                    self.clicked = True

                if self.character_back_button.draw(screen) and self.clicked is False:
                    menu_state = 'main'
                    self.character_menu_position = 0
                    self.characters_image_positions = self.characters_image_origin_positions
                    for button, x in zip(self.character_button_list, range(6)):
                        button.image_not_pressed = button.saved_image_not_pressed
                        button.rect.x = self.characters_buttons_positions[x]
                    self.chose_made = False
                    self.clicked = True

            # show custom cursor on screen
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(cursor, mouse_pos)

            pygame.display.update()

    def character_choice(self, direction):
        if self.character_menu_position < 0:
            self.character_menu_position = 0
        elif self.character_menu_position > len(self.characters_image_positions) - 3:
            self.character_menu_position = len(self.characters_image_positions) - 3
        else:
            if direction == 'left':
                self.characters_image_positions = [position + 615 for position in self.characters_image_positions]
                for button in self.character_button_list:
                    button.rect.x += 615
            if direction == 'right':
                self.characters_image_positions = [position - 615 for position in self.characters_image_positions]
                for button in self.character_button_list:
                    button.rect.x -= 615


if __name__ == '__main__':
    menu = Menu(False)
    menu.run(running=True, menu_state='main')
