import pygame

# window settings
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect(center=(WIDTH/2, HEIGHT/2))
pygame.display.set_caption("Hemorrhoid Fighter")

# game settings
game_active = False
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font("res/font.ttf", 35)
bigger_font = pygame.font.Font("res/font.ttf", 65)
menu_font = pygame.font.Font("res/font.ttf", 60)
hp_text = font.render('HP', False, 'Black')
xp_text = font.render('LEVEL', False, 'Black')
death_text = bigger_font.render('YOU DIED', False, 'Black')
death_text_rect = death_text.get_rect(center=(960, 720))
grey_pause_screen = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
grey_pause_screen.fill((50, 50, 50, 255))
pygame.mouse.set_visible(False)

# player settings
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100
player_hp = 10000
player_xp = 0
level = 1
needed_player_xp = 1000
player_speed = 10
player_gold = 0

# item settings
hp_value = 100

# enemy settings
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

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
