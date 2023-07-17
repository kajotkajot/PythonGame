from assets import *
from button import Button


class Skill(pygame.sprite.Sprite):
    def __init__(self, num, position, image, group, player, skill_availability):
        super().__init__(group)
        self.id = num
        self.position = position
        self.image = image
        self.player = player
        self.skill_availability_bool = skill_availability
        self.skill_border = pygame.Surface([220, 250])
        self.skill_border.fill("black")
        self.skill_description = skill_description
        self.skill_point1 = pygame.Surface([60, 20])
        self.skill_point1.fill("grey")
        self.skill_point2 = pygame.Surface([60, 20])
        self.skill_point2.fill("grey")
        self.skill_point3 = pygame.Surface([60, 20])
        self.skill_point3.fill("grey")
        self.added_skill_point1 = False
        self.added_skill_point2 = False
        self.added_skill_point3 = False
        self.add_skill_button = Button('+1 POINT', 1465, 770, button_360x100_image, button_360x100_image_pressed)
        self.action = False
        self.clicked = False
        self.skill_availability = pygame.Surface([200, 200])
        self.skill_availability.fill((0, 0, 0, 255))
        self.skill_availability.set_alpha(150)
