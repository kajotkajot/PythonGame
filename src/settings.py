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
font = pygame.font.Font("res/font.ttf", 35)
bigger_font = pygame.font.Font("res/font.ttf", 65)
menu_font = pygame.font.Font("res/font.ttf", 60)
skill_font = pygame.font.Font("res/font.ttf", 25)
hp_text = font.render('HP', False, 'Black')
xp_text = font.render('LEVEL', False, 'Black')
death_text = bigger_font.render('YOU DIED', False, 'Black')
death_text_rect = death_text.get_rect(center=(960, 720))
grey_pause_screen = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
grey_pause_screen.fill((50, 50, 50, 255))
pygame.mouse.set_visible(False)
boundary_radius = 5000
boundary_center = (WIDTH / 2, HEIGHT / 2)

# player settings
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100
player_max_hp = 10000
player_xp = 0
level = 1
needed_player_xp = 1000
player_speed = 10
player_gold = 0
player_skill_points = 100

# item settings
health_value = 100

# enemy settings
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 500)

# red enemy settings
red_enemy_hp = 100
red_enemy_speed = 100
red_enemy_xp = 500
red_enemy_damage = 1

# green enemy settings
green_enemy_hp = 100
green_enemy_speed = 250
green_enemy_xp = 1000
green_enemy_damage = 10
