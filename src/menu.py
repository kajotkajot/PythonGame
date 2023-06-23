from settings import *
from button import Button
import sys


class Menu:
    def __init__(self):
        self.start_button = Button(300, 100, start_button_image)
        self.exit_button = Button(300, 700, exit_button_image)
        self.settings_button = Button(300, 400, settings_button_image)
        self.character_choice_menu = CharacterChoiceMenu()
        self.settings_menu = SettingsMenu()

    def run(self, running):
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill("orange")
            if self.start_button.draw(screen):
                self.character_choice_menu.run(running=True)
                running = False

            if self.settings_button.draw(screen):
                self.settings_menu.run(running=True)
                running = False

            if self.exit_button.draw(screen):
                sys.exit()

            pygame.display.update()


class SettingsMenu:
    def __init__(self):
        self.resolution1280x720_button = Button(300, 500, settings_button_image)
        self.resolution1920x1080_button = Button(700, 500, settings_button_image)
        self.back_button = Button(600, 700, settings_button_image)

    def run(self, running):
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill("grey")
            if self.resolution1280x720_button.draw(screen):
                pass

            if self.resolution1920x1080_button.draw(screen):
                pass

            if self.back_button.draw(screen):
                menu.run(running=True)
                running = False

            pygame.display.update()


class CharacterChoiceMenu:
    def __init__(self):
        self.knight_button = Button(400, 400, character_button_image)
        self.character2_button = Button(800, 400, character_button_image)
        self.character3_button = Button(1200, 400, character_button_image)
        self.back_button = Button(600, 800, settings_button_image)

    def run(self, running):
        from main import Main
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill("blue")
            if self.knight_button.draw(screen):
                main = Main(running=True)
                main.run()
                running = False

            if self.character2_button.draw(screen):
                pass

            if self.character3_button.draw(screen):
                pass

            if self.back_button.draw(screen):
                menu.run(running=True)
                running = False

            pygame.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.run(running=True)
