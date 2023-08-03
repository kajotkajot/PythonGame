from src.settings import *


class AngelSkill10(pygame.sprite.Sprite):
    def __init__(self, player, group, active):
        super().__init__(group)
        self.type = "passive"
        self.player = player
        self.active = active
        self.current_time = pygame.time.get_ticks()
        self.timer = self.current_time

    def check_state(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > 5000:
            self.player.current_hp += self.player.max_hp * self.player.character.skill10.current_value
            self.timer = pygame.time.get_ticks()

    def update(self):
        if self.active:
            self.check_state()
