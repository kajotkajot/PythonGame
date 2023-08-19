from settings import *


class LoadingSquare:
    def __init__(self, position):
        self.position = position
        self.image = pygame.Surface((59, 26), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect().move(self.position)
        pygame.draw.polygon(self.image, white_color, [(16, 0), (58, 0), (42, 26), (0, 26)])


class LoadingScreen:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.loading_text = bigger_font.render('LOADING', True, white_color)
        self.loading_surface = pygame.Surface((self.loading_text.get_width() + 50, 50))
        self.square_surface = pygame.Surface((self.loading_text.get_width() + 26, 30))
        self.squares = []
        for i in range(10):
            square = LoadingSquare((-80 + i * 51, 2))
            self.squares.append(square)

    def run(self):
        self.display.fill((15, 15, 15))
        self.display.blit(self.loading_text, (960 - self.loading_text.get_width() / 2, 540 - self.loading_text.get_height() / 2))
        pygame.draw.rect(self.loading_surface, white_color, (0, 0, self.loading_text.get_width() + 50, 50), width=5)
        self.square_surface.fill(black_color)
        for i in range(10):
            self.squares[i].rect.x += 1
            self.square_surface.blit(self.squares[i].image, self.squares[i].rect)
            if self.squares[i].rect.x >= 380:
                self.squares[i].rect.x = -80
        self.display.blit(self.loading_surface, (960 - self.loading_surface.get_width() / 2, 600))
        self.loading_surface.blit(self.square_surface, (12, 10))
