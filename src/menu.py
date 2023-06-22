from settings import *
from button import Button
from main import Main
import sys


class Menu:
    def __init__(self):
        self.game_active = game_active
        self.start_button = Button(300, 100, start_button_image)
        self.settings_button = Button(300, 400, settings_button_image)
        self.exit_button = Button(300, 700, exit_button_image)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            screen.fill("orange")
            if self.start_button.draw(screen):
                main = Main(activation=True)
                main.run()

            if self.settings_button.draw(screen):
                pass

            if self.exit_button.draw(screen):
                self.running = False

            pygame.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.run()
