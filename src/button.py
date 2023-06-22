import pygame


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.pos = self.image.get_rect()
        self.pos.x = x
        self.pos.y = y
        self.clicked = False

    def draw(self, screen):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.pos.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.pos.x, self.pos.y))

        return action
