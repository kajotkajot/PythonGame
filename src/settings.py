import pygame

# window settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect(center=(WIDTH/2, HEIGHT/2))
pygame.display.set_caption("Hemorrhoid Fighter")

# game settings
game_active = False
pygame.init()
clock = pygame.time.Clock()
bigger_font = pygame.font.Font("res/font.ttf", 65)
menu_font = pygame.font.Font("res/font.ttf", 60)
skill_font = pygame.font.Font("res/font.ttf", 50)
title_font = pygame.font.Font("res/font.ttf", 40)
font = pygame.font.Font("res/font.ttf", 35)
fps_font = pygame.font.Font("res/font.ttf", 15)
grey_pause_screen = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
grey_pause_screen.fill((50, 50, 50, 255))
pygame.mouse.set_visible(False)
skill_polygon_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
current_state_image = pygame.Surface([WIDTH, HEIGHT])
black_color = (15, 15, 15)
white_color = (220, 220, 220)
fog_radius = 800
fog_distance = 200

# procedural generation settings
steps_count = 10
square_count = 300
main_count = 10
mean_size = 5000 * 15
stddev = 125 * 15
corridor_size = 75 * 10

# inventory minimap settings
INV_MINIMAP_WIDTH, INV_MINIMAP_HEIGHT = 970, 970
inventory_minimap_surface = pygame.Surface((INV_MINIMAP_WIDTH, INV_MINIMAP_HEIGHT))
inventory_minimap_surface.set_alpha(255)
player_color = (0, 255, 255)
enemy_color = (255, 0, 0)
item_color = (0, 255, 0)

# in-game minimap settings
IN_GAME_MINIMAP_WIDTH, IN_GAME_MINIMAP_HEIGHT = 250, 250
in_game_minimap_surface = pygame.Surface((IN_GAME_MINIMAP_WIDTH, IN_GAME_MINIMAP_HEIGHT))
in_game_minimap_surface.set_alpha(255)

# player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 200, 200
needed_player_xp = 1000
player_xp = 0
player_skill_points = 100
player_gold = 0
level = 1

# character settings
knight_stats = {
    "max_hp": 0,
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

angel_stats = {
    "max_hp": 100,
    "health": 100,
    "speed": 10,
    "attack": 5,
    "armor": 0,
    "damage_bounce": 0,
    "armor_reduction": 1,
    "damage_reduction": 1,
    "regeneration": 0,
    "resurrections": 0,
    "resurrection_value": 0
}

assassin_stats = {
    "max_hp": 0,
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

mage_stats = {
    "max_hp": 0,
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

necromancer_stats = {
    "max_hp": 0,
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

swordsman_stats = {
    "max_hp": 0,
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

# red enemy settings
red_enemy_stats = {
    "max_hp": 10,
    "health": 10,
    "speed": 100,
    "attack": 1,
    "armor": 10,
    "xp": 500
}

# green enemy settings
green_enemy_stats = {
    "max_hp": 10,
    "health": 10,
    "speed": 250,
    "attack": 10,
    "armor": 10,
    "xp": 1000
}
