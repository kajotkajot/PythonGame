import pygame
from settings import menu_font


class Button:
    def __init__(self, text, x, y, image, image_pressed):
        self.current_image = image
        self.saved_image_not_pressed = image
        self.saved_image_pressed = image_pressed
        self.image_not_pressed = image
        self.image_pressed = image_pressed
        self.text = menu_font.render(text, False, 'Black')
        self.text_width = menu_font.size(text)[0]/2
        self.text_height = menu_font.size(text)[1]/2
        self.rect = self.current_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_image = self.image_pressed
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True
        else:
            self.current_image = self.image_not_pressed
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.current_image, (self.rect.x, self.rect.y))
        screen.blit(self.text, (self.rect.center[0] - self.text_width, self.rect.center[1] - self.text_height - 2))

        return action
