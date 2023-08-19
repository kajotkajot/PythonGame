from src.assets import *
from src.settings import *
from src.button import Button


class AngelSkill(pygame.sprite.Sprite):
    def __init__(self, num, position, image, group, player, skill_availability, title, description, point1_value, point2_value, point3_value):
        super().__init__(group)
        self.id = num
        self.position = position
        self.image = image
        self.player = player
        self.skill_availability_bool = skill_availability
        self.title = title_font.render(title, True, "Black")
        self.title_width = self.title.get_width()/2
        self.description = description
        self.skill_border = pygame.Surface([220, 250])
        self.skill_border.fill("black")
        self.skill_description_background = skill_description
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
        self.current_value = 1
        self.point1_value = point1_value
        self.point2_value = point2_value
        self.point3_value = point3_value

    def level_up(self):
        if self.id == 1:
            self.skill1()
        if self.id == 2:
            self.skill2()
        if self.id == 4:
            self.skill4()
        if self.id == 5:
            self.skill5()
        if self.id == 6:
            self.skill6()
        if self.id == 7:
            self.skill7()
        if self.id == 8:
            self.skill8()
        if self.id == 10:
            self.skill10()
        if self.id == 11:
            self.skill11()

    def skill1(self):
        self.player.stats["speed"] = int(angel_stats["speed"] + self.current_value)
        self.player.can_fly = True

    def skill2(self):
        self.player.stats["health"] += (int(angel_stats["health"]) * self.current_value) - self.player.stats["max_hp"]
        self.player.stats["max_hp"] = int(angel_stats["health"] * self.current_value)

    def skill4(self):
        self.player.stats["attack"] = int(angel_stats["attack"] * self.current_value)

    def skill5(self):
        self.player.stats["damage_bounce"] = self.current_value

    def skill6(self):
        self.player.character.skill6_duration += 2000

    def skill7(self):
        self.player.stats["damage_reduction"] = self.current_value

    def skill8(self):
        self.player.passive_skill8.active = True
        if self.player.stats["resurrection_value"] < 0.3:
            self.player.stats["resurrection_value"] = self.current_value
        self.player.stats["resurrections"] += 1

    def skill10(self):
        self.player.passive_skill10.active = True
        self.player.stats["regeneration"] = self.current_value

    def skill11(self):
        self.player.stats["resurrection_value"] = self.current_value
        self.player.explosion_on_death = True
