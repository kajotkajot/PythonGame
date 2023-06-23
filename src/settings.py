import pygame

# window settings
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = screen.get_rect(center=(WIDTH/2, HEIGHT/2))
pygame.display.set_caption("Hemorrhoid Fighter")

# player settings
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100
player_right = pygame.image.load('res/player_right.png').convert()
player_right_scaled = pygame.transform.scale(player_right, (300, 300))
player_left = pygame.image.load('res/player_left.png').convert()
player_death = pygame.image.load('res/player_death.png').convert()
player_death_scaled = pygame.transform.scale(player_death, (300, 300))
player_hp = 10000
player_xp = 0
level = 0
needed_player_xp = 1000
player_speed = 10

# attacks settings
attacks = []
slash_attack_damage = 10

# game settings
start_button_image = pygame.Surface([300, 100])
settings_button_image = pygame.Surface([300, 100])
exit_button_image = pygame.Surface([300, 100])
character_button_image = pygame.Surface([300, 300])
game_active = False
pygame.init()
clock = pygame.time.Clock()
background = pygame.image.load('res/background.png').convert()
current_state_image = pygame.image.load('res/background.png').convert()
font = pygame.font.Font("res/font.ttf", 35)
bigger_font = pygame.font.Font("res/font.ttf", 65)
hp_text = font.render('HP', False, 'Black')
level_text = font.render('LEVEL', False, 'Black')
death_text = bigger_font.render('YOU DIED', False, 'Black')
death_text_rect = death_text.get_rect(center=(960, 720))
blurred_current_state_image = pygame.image.load('res/background.png').convert()
square = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
square.fill((50, 50, 50, 255))

# enemy settings
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)
enemies = []
dead_enemies = []

# hp settings
hp_heart = pygame.image.load('res/hp_heart.png')
hp_heart_shadow = pygame.image.load('res/hp_heart_shadow.png')
hp_value = 100
hp_list = []

# red enemy settings
red_enemy_hp = 100
red_enemy_speed = 100
red_enemy_xp = 500
red_enemy_damage = 1
red_enemy_right = pygame.image.load('res/enemy_move_right1.png').convert()
red_enemy_left = pygame.image.load('res/enemy_move_left1.png').convert()

# green enemy settings
green_enemy_hp = 100
green_enemy_speed = 250
green_enemy_xp = 1000
green_enemy_damage = 10
green_enemy_right = pygame.image.load('res/green_enemy_move_right1.png').convert()
green_enemy_left = pygame.image.load('res/green_enemy_move_left1.png').convert()
