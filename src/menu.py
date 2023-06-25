from settings import *
from button import Button
import sys


class Menu:
    def __init__(self, clicked):
        # main menu buttons
        self.start_button = Button(585, 650, start_button_image)
        self.settings_button = Button(585, 780, settings_button_image)
        self.credits_button = Button(585, 910, credits_button)
        self.exit_button = Button(975, 910, exit_button_image)

        # settings buttons
        self.resolution1280x720_button = Button(585, 650, settings_button_image)
        self.resolution1920x1080_button = Button(585, 780, settings_button_image)
        self.settings_back_button = Button(585, 910, settings_button_image)

        # character choice buttons
        self.knight_button = Button(75, 75, character_button_image)
        self.character2_button = Button(690, 75, character_button_image)
        self.character3_button = Button(1305, 75, character_button_image)
        self.play_button = Button(75, 905, play_button_image)
        self.character_back_button = Button(1485, 905, back_button_image)

        # important variables
        self.clicked = clicked

    def run(self, running, menu_state):
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicked = False

            if menu_state == 'main':
                screen.fill("orange")
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
                screen.fill("grey")
                if self.resolution1280x720_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.resolution1920x1080_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.settings_back_button.draw(screen) and self.clicked is False:
                    menu_state = 'main'
                    self.clicked = True

            if menu_state == 'character_choice':
                from main import Main
                screen.fill("blue")
                if self.knight_button.draw(screen) and self.clicked is False:
                    main = Main(running=True)
                    main.run()
                    self.clicked = True

                if self.character2_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.character3_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.play_button.draw(screen) and self.clicked is False:
                    self.clicked = True

                if self.character_back_button.draw(screen) and self.clicked is False:
                    menu_state = 'main'
                    self.clicked = True

            pygame.display.update()


if __name__ == '__main__':
    menu = Menu(False)
    menu.run(running=True, menu_state='main')
