from src.assets import *
from src.angelfiles.angelskills import AngelSkill


class Angel:
    def __init__(self, player, skill_group):
        self.image = angel_right
        self.image_right = angel_right
        self.icon_inventory = angel_icon_inventory
        self.image_death = angel_death
        self.image_death_scaled = angel_death_scaled
        self.player_left_stand_sprites = angel_left_stand_sprites
        self.player_right_stand_sprites = angel_right_stand_sprites
        self.player_left_sprites = angel_left_move_sprites
        self.player_right_sprites = angel_right_move_sprites
        self.player_left_death_sprites = angel_left_death_sprites
        self.player_right_death_sprites = angel_right_death_sprites
        self.player_left_basic_attack_sprites = angel_left_basic_attack_sprites
        self.player_right_basic_attack_sprites = angel_right_basic_attack_sprites
        self.player_left_explosion_sprites = angel_left_explosion_sprites
        self.player_right_explosion_sprites = angel_right_explosion_sprites
        self.animation_timer = 0.1
        self.basic_attack_icon = angel_basic_attack_icon
        self.in_game_skill3 = in_game_angel_skill3_icon
        self.in_game_skill6 = in_game_angel_skill6_icon
        self.in_game_skill9 = in_game_angel_skill9_icon
        self.in_game_skill12 = in_game_angel_skill12_icon
        self.basic_cooldown = 1000
        self.skill3_cooldown = 5000
        self.skill6_cooldown = 15000
        self.skill9_cooldown = 30000
        self.skill12_cooldown = 10000
        self.skill3_duration = 3000
        self.skill6_duration = 4000
        self.skill9_duration = 1000
        self.skill12_duration = 3000
        self.skill1 = AngelSkill(1, (75, 75), tree_angel_skill1_icon, skill_group, player, True, "WINGS OF LIGHT", angel_skill1_description, 1, 2, 3)
        self.skill2 = AngelSkill(2, (75, 430), tree_angel_skill2_icon, skill_group, player, True, "DIVINE LEAD", angel_skill2_description, 1.1, 1.25, 1.5)
        self.skill3 = AngelSkill(3, (75, 785), tree_angel_skill3_icon, skill_group, player, True, "RAY OF LIGHT", angel_skill3_description, 1, 1.25, 1.5)
        self.skill4 = AngelSkill(4, (430, 75), tree_angel_skill4_icon, skill_group, player, False, "HOLY SWORD", angel_skill4_description, 1.1, 1.2, 1.3)
        self.skill5 = AngelSkill(5, (430, 430), tree_angel_skill5_icon, skill_group, player, False, "DIVINE PUNISHMENT", angel_skill5_description, 0.5, 0.75, 1)
        self.skill6 = AngelSkill(6, (430, 785), tree_angel_skill6_icon, skill_group, player, False, "DIVINE STRENGTH", angel_skill6_description, 0.8, 0.7, 0.6)
        self.skill7 = AngelSkill(7, (785, 75), tree_angel_skill7_icon, skill_group, player, False, "LIGHT BARRIER", angel_skill7_description, 0.95, 0.9, 0.85)
        self.skill8 = AngelSkill(8, (785, 430), tree_angel_skill8_icon, skill_group, player, False, "GUARDIAN ANGEL", angel_skill8_description, 0.3, 0.3, 0.3)
        self.skill9 = AngelSkill(9, (785, 785), tree_angel_skill9_icon, skill_group, player, False, "EXPLOSION", angel_skill9_description, 3, 4, 5)
        self.skill10 = AngelSkill(10, (1140, 75), tree_angel_skill10_icon, skill_group, player, False, "INNER PEACE", angel_skill10_description, 0.01, 0.02, 0.03)
        self.skill11 = AngelSkill(11, (1140, 430), tree_angel_skill11_icon, skill_group, player, False, "BACK FROM THE DEAD", angel_skill11_description, 0.4, 0.5, 0.6)
        self.skill12 = AngelSkill(12, (1140, 785), tree_angel_skill12_icon, skill_group, player, False, "GOD'S WRATH", angel_skill12_description, 2, 2.5, 3)
