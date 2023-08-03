import pygame

# window settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect(center=(WIDTH/2, HEIGHT/2))
pygame.display.set_caption("Hemorrhoid Fighter")

# inventory minimap settings
MAP_WIDTH, MAP_HEIGHT = 10000, 10000
INV_MINIMAP_WIDTH, INV_MINIMAP_HEIGHT = 970, 970
inventory_minimap_scale_x = INV_MINIMAP_WIDTH / MAP_WIDTH
inventory_minimap_scale_y = INV_MINIMAP_HEIGHT / MAP_HEIGHT
inventory_minimap_surface = pygame.Surface((INV_MINIMAP_WIDTH, INV_MINIMAP_HEIGHT))
inventory_minimap_surface.set_alpha(255)
player_color = (0, 255, 255)
enemy_color = (255, 0, 0)
item_color = (0, 255, 0)

# in-game minimap settings
IN_GAME_MINIMAP_WIDTH, IN_GAME_MINIMAP_HEIGHT = 250, 250
in_game_minimap_scale_x = IN_GAME_MINIMAP_WIDTH / MAP_WIDTH * 4
in_game_minimap_scale_y = IN_GAME_MINIMAP_HEIGHT / MAP_HEIGHT * 4
in_game_minimap_surface = pygame.Surface((IN_GAME_MINIMAP_WIDTH, IN_GAME_MINIMAP_HEIGHT))
in_game_minimap_surface.set_alpha(255)

# game settings
game_active = False
pygame.init()
clock = pygame.time.Clock()
bigger_font = pygame.font.Font("res/font.ttf", 65)
menu_font = pygame.font.Font("res/font.ttf", 60)
skill_font = pygame.font.Font("res/font.ttf", 50)
title_font = pygame.font.Font("res/font.ttf", 40)
font = pygame.font.Font("res/font.ttf", 35)
grey_pause_screen = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
grey_pause_screen.fill((50, 50, 50, 255))
pygame.mouse.set_visible(False)
boundary_radius = 5000
boundary_center = (WIDTH / 2, HEIGHT / 2)
skill_polygon_surface = pygame.Surface((100, 100), pygame.SRCALPHA)

# player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 200, 200
player_xp = 0
level = 1
needed_player_xp = 1000
player_gold = 0
player_skill_points = 100

# enemy settings
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 500)

# character settings
knight_stats = {
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

angel_stats = {
    "health": 100,
    "speed": 10,
    "attack": 5,
    "armor": 0
}

assassin_stats = {
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

mage_stats = {
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

necromancer_stats = {
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

swordsman_stats = {
    "health": 0,
    "speed": 0,
    "attack": 0,
    "armor": 0
}

# red enemy settings
red_enemy_stats = {
    "health": 10,
    "speed": 100,
    "attack": 0.1,
    "armor": 10,
    "xp": 500
}

# green enemy settings
green_enemy_stats = {
    "health": 10,
    "speed": 250,
    "attack": 10,
    "armor": 10,
    "xp": 1000
}
