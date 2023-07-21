import pygame

# game assets
current_state_image = pygame.image.load('res/background.png').convert_alpha()
blurred_current_state_image = pygame.image.load('res/background.png').convert_alpha()
arena_background = pygame.image.load('res/arena_background.png').convert_alpha()
cursor = pygame.transform.scale(pygame.image.load('res/cursor.png').convert_alpha(), (48, 48))
ghost_sprites = [pygame.image.load('res/ghost1.png').convert_alpha(),
                 pygame.image.load('res/ghost2.png').convert_alpha()]
sprite_width, sprite_height = 200, 200

# minimap assets
inventory_minimap_background = pygame.transform.scale(arena_background, (970, 970))
in_game_minimap_background = pygame.transform.scale(arena_background, (1000, 1000))

# knight assets
knight_right = pygame.image.load('res/knight_stand_right1.png').convert_alpha()
knight_right_scaled = pygame.transform.scale(knight_right, (300, 300))
knight_right_menu = pygame.transform.scale(knight_right, (400, 400))
knight_death = pygame.image.load('res/knight_death.png').convert_alpha()
knight_death_scaled = pygame.transform.scale(knight_death, (300, 300))
knight_left_sprites = [pygame.image.load('res/knight_move_left1.png').convert_alpha(),
                       pygame.image.load('res/knight_move_left2.png').convert_alpha(),
                       pygame.image.load('res/knight_move_left3.png').convert_alpha(),
                       pygame.image.load('res/knight_move_left4.png').convert_alpha(),
                       pygame.image.load('res/knight_move_left5.png').convert_alpha(),
                       pygame.image.load('res/knight_move_left6.png').convert_alpha()]
knight_right_sprites = [pygame.image.load('res/knight_move_right1.png').convert_alpha(),
                        pygame.image.load('res/knight_move_right2.png').convert_alpha(),
                        pygame.image.load('res/knight_move_right3.png').convert_alpha(),
                        pygame.image.load('res/knight_move_right4.png').convert_alpha(),
                        pygame.image.load('res/knight_move_right5.png').convert_alpha(),
                        pygame.image.load('res/knight_move_right6.png').convert_alpha()]
knight_left_death_sprites = [pygame.image.load('res/knight_death_left1.png').convert_alpha(),
                             pygame.image.load('res/knight_death_left2.png').convert_alpha(),
                             pygame.image.load('res/knight_death_left3.png').convert_alpha(),
                             pygame.image.load('res/knight_death_left4.png').convert_alpha(),
                             pygame.image.load('res/knight_death_left5.png').convert_alpha()]
knight_right_death_sprites = [pygame.image.load('res/knight_death_right1.png').convert_alpha(),
                              pygame.image.load('res/knight_death_right2.png').convert_alpha(),
                              pygame.image.load('res/knight_death_right3.png').convert_alpha(),
                              pygame.image.load('res/knight_death_right4.png').convert_alpha(),
                              pygame.image.load('res/knight_death_right5.png').convert_alpha()]
knight_left_stand_sprites = [pygame.image.load('res/knight_stand_left1.png').convert_alpha(),
                             pygame.image.load('res/knight_stand_left2.png').convert_alpha()]
knight_right_stand_sprites = [pygame.image.load('res/knight_stand_right1.png').convert_alpha(),
                              pygame.image.load('res/knight_stand_right2.png').convert_alpha()]

# test angel assets
angel_sprite_sheet_left = pygame.image.load('res/angel_sprite_sheet_left.png').convert_alpha()
angel_sprite_sheet_right = pygame.image.load('res/angel_sprite_sheet_right.png').convert_alpha()
angel_left_stand_sprites, angel_right_stand_sprites = [], []
angel_left_move_sprites, angel_right_move_sprites = [], []
angel_left_death_sprites, angel_right_death_sprites = [], []
angel_left_game_start_sprites, angel_right_game_start_sprites = [], []
angel_left_basic_attack_sprites, angel_right_basic_attack_sprites = [], []
angel_divine_left_stand_sprites, angel_divine_right_stand_sprites = [], []
angel_divine_left_move_sprites, angel_divine_right_move_sprites = [], []
angel_divine_left_basic_attack_sprites, angel_divine_right_basic_attack_sprites = [], []
angel_left_resurrect_sprites, angel_right_resurrect_sprites = [], []
angel_left_explosion_sprites, angel_right_explosion_sprites = [], []
angel_divine_left_explosion_sprites, angel_divine_right_explosion_sprites = [], []
for row in range(4):
    sprite_rect = pygame.Rect(row * sprite_width, 0 * sprite_height, sprite_width, sprite_height)
    angel_left_stand_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_stand_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(3):
    sprite_rect = pygame.Rect(row * sprite_width, 1 * sprite_height, sprite_width, sprite_height)
    angel_left_move_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_move_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(6):
    sprite_rect = pygame.Rect(row * sprite_width, 2 * sprite_height, sprite_width, sprite_height)
    angel_left_death_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_death_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(7):
    sprite_rect = pygame.Rect(row * sprite_width, 3 * sprite_height, sprite_width, sprite_height)
    angel_left_game_start_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_game_start_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(3):
    sprite_rect = pygame.Rect(row * sprite_width, 4 * sprite_height, sprite_width, sprite_height)
    angel_left_basic_attack_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_basic_attack_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(4):
    sprite_rect = pygame.Rect(row * sprite_width, 5 * sprite_height, sprite_width, sprite_height)
    angel_divine_left_stand_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_divine_right_stand_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(3):
    sprite_rect = pygame.Rect(row * sprite_width, 6 * sprite_height, sprite_width, sprite_height)
    angel_divine_left_move_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_divine_right_move_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(3):
    sprite_rect = pygame.Rect(row * sprite_width, 7 * sprite_height, sprite_width, sprite_height)
    angel_divine_left_basic_attack_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_divine_right_basic_attack_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(4):
    sprite_rect = pygame.Rect(row * sprite_width, 8 * sprite_height, sprite_width, sprite_height)
    angel_left_resurrect_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_resurrect_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
angel_left_resurrect_sprites.append(angel_left_game_start_sprites)
angel_right_resurrect_sprites.append(angel_right_game_start_sprites)
for row in range(6):
    sprite_rect = pygame.Rect(row * sprite_width, 9 * sprite_height, sprite_width, sprite_height)
    angel_left_explosion_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_right_explosion_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
for row in range(6):
    sprite_rect = pygame.Rect(row * sprite_width, 10 * sprite_height, sprite_width, sprite_height)
    angel_divine_left_explosion_sprites.append(angel_sprite_sheet_left.subsurface(sprite_rect))
    angel_divine_right_explosion_sprites.append(angel_sprite_sheet_right.subsurface(sprite_rect))
angel_right = angel_right_game_start_sprites[2]
angel_right_scaled = pygame.transform.scale(angel_right, (300, 300))
angel_right_menu = pygame.transform.scale(angel_right, (400, 400))
angel_death = angel_right_death_sprites[5]
angel_death_scaled = pygame.transform.scale(angel_death, (300, 300))

# assassin assets
assassin_right = pygame.image.load('res/assassin_stand_right1.png').convert_alpha()
assassin_right_scaled = pygame.transform.scale(assassin_right, (300, 300))
assassin_right_menu = pygame.transform.scale(assassin_right, (400, 400))
assassin_death = pygame.image.load('res/assassin_death.png').convert_alpha()
assassin_death_scaled = pygame.transform.scale(assassin_death, (300, 300))
assassin_left_sprites = [pygame.image.load('res/assassin_move_left1.png').convert_alpha(),
                         pygame.image.load('res/assassin_move_left2.png').convert_alpha(),
                         pygame.image.load('res/assassin_move_left3.png').convert_alpha(),
                         pygame.image.load('res/assassin_move_left4.png').convert_alpha(),
                         pygame.image.load('res/assassin_move_left5.png').convert_alpha(),
                         pygame.image.load('res/assassin_move_left6.png').convert_alpha()]
assassin_right_sprites = [pygame.image.load('res/assassin_move_right1.png').convert_alpha(),
                          pygame.image.load('res/assassin_move_right2.png').convert_alpha(),
                          pygame.image.load('res/assassin_move_right3.png').convert_alpha(),
                          pygame.image.load('res/assassin_move_right4.png').convert_alpha(),
                          pygame.image.load('res/assassin_move_right5.png').convert_alpha(),
                          pygame.image.load('res/assassin_move_right6.png').convert_alpha()]
assassin_left_death_sprites = [pygame.image.load('res/assassin_death_left1.png').convert_alpha(),
                               pygame.image.load('res/assassin_death_left2.png').convert_alpha(),
                               pygame.image.load('res/assassin_death_left3.png').convert_alpha(),
                               pygame.image.load('res/assassin_death_left4.png').convert_alpha(),
                               pygame.image.load('res/assassin_death_left5.png').convert_alpha()]
assassin_right_death_sprites = [pygame.image.load('res/assassin_death_right1.png').convert_alpha(),
                                pygame.image.load('res/assassin_death_right2.png').convert_alpha(),
                                pygame.image.load('res/assassin_death_right3.png').convert_alpha(),
                                pygame.image.load('res/assassin_death_right4.png').convert_alpha(),
                                pygame.image.load('res/assassin_death_right5.png').convert_alpha()]
assassin_left_stand_sprites = [pygame.image.load('res/assassin_stand_left1.png').convert_alpha(),
                               pygame.image.load('res/assassin_stand_left2.png').convert_alpha(),
                               pygame.image.load('res/assassin_stand_left3.png').convert_alpha(),
                               pygame.image.load('res/assassin_stand_left4.png').convert_alpha()]
assassin_right_stand_sprites = [pygame.image.load('res/assassin_stand_right1.png').convert_alpha(),
                                pygame.image.load('res/assassin_stand_right2.png').convert_alpha(),
                                pygame.image.load('res/assassin_stand_right3.png').convert_alpha(),
                                pygame.image.load('res/assassin_stand_right4.png').convert_alpha()]

# mage assets
mage_right = pygame.image.load('res/mage_stand_right1.png').convert_alpha()
mage_right_scaled = pygame.transform.scale(mage_right, (300, 300))
mage_right_menu = pygame.transform.scale(mage_right, (400, 400))
mage_death = pygame.image.load('res/mage_death.png').convert_alpha()
mage_death_scaled = pygame.transform.scale(mage_death, (300, 300))
mage_left_sprites = [pygame.image.load('res/mage_move_left1.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left2.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left3.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left4.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left5.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left6.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left7.png').convert_alpha(),
                     pygame.image.load('res/mage_move_left8.png').convert_alpha()]
mage_right_sprites = [pygame.image.load('res/mage_move_right1.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right2.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right3.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right4.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right5.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right6.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right7.png').convert_alpha(),
                      pygame.image.load('res/mage_move_right8.png').convert_alpha()]
mage_left_death_sprites = [pygame.image.load('res/mage_death_left1.png').convert_alpha(),
                           pygame.image.load('res/mage_death_left2.png').convert_alpha(),
                           pygame.image.load('res/mage_death_left3.png').convert_alpha(),
                           pygame.image.load('res/mage_death_left4.png').convert_alpha(),
                           pygame.image.load('res/mage_death_left5.png').convert_alpha()]
mage_right_death_sprites = [pygame.image.load('res/mage_death_right1.png').convert_alpha(),
                            pygame.image.load('res/mage_death_right2.png').convert_alpha(),
                            pygame.image.load('res/mage_death_right3.png').convert_alpha(),
                            pygame.image.load('res/mage_death_right4.png').convert_alpha(),
                            pygame.image.load('res/mage_death_right5.png').convert_alpha()]
mage_left_stand_sprites = [pygame.image.load('res/mage_stand_left1.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left2.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left3.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left4.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left5.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left6.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left7.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left8.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left9.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left10.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left11.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left12.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left13.png').convert_alpha(),
                           pygame.image.load('res/mage_stand_left14.png').convert_alpha()]
mage_right_stand_sprites = [pygame.image.load('res/mage_stand_right1.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right2.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right3.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right4.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right5.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right6.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right7.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right8.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right9.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right10.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right11.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right12.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right13.png').convert_alpha(),
                            pygame.image.load('res/mage_stand_right14.png').convert_alpha()]

# necromancer assets
necromancer_right = pygame.image.load('res/necromancer_stand_right1.png').convert_alpha()
necromancer_right_scaled = pygame.transform.scale(necromancer_right, (300, 300))
necromancer_right_menu = pygame.transform.scale(necromancer_right, (400, 400))
necromancer_death = pygame.image.load('res/necromancer_death.png').convert_alpha()
necromancer_death_scaled = pygame.transform.scale(necromancer_death, (300, 300))
necromancer_left_sprites = [pygame.image.load('res/necromancer_move_left1.png').convert_alpha(),
                            pygame.image.load('res/necromancer_move_left2.png').convert_alpha(),
                            pygame.image.load('res/necromancer_move_left3.png').convert_alpha(),
                            pygame.image.load('res/necromancer_move_left4.png').convert_alpha()]
necromancer_right_sprites = [pygame.image.load('res/necromancer_move_right1.png').convert_alpha(),
                             pygame.image.load('res/necromancer_move_right2.png').convert_alpha(),
                             pygame.image.load('res/necromancer_move_right3.png').convert_alpha(),
                             pygame.image.load('res/necromancer_move_right4.png').convert_alpha()]
necromancer_left_death_sprites = [pygame.image.load('res/necromancer_death_left1.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_death_left2.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_death_left3.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_death_left4.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_death_left5.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_death_left6.png').convert_alpha()]
necromancer_right_death_sprites = [pygame.image.load('res/necromancer_death_right1.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_death_right2.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_death_right3.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_death_right4.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_death_right5.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_death_right6.png').convert_alpha()]
necromancer_left_stand_sprites = [pygame.image.load('res/necromancer_stand_left1.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_stand_left2.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_stand_left3.png').convert_alpha(),
                                  pygame.image.load('res/necromancer_stand_left4.png').convert_alpha()]
necromancer_right_stand_sprites = [pygame.image.load('res/necromancer_stand_right1.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_stand_right2.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_stand_right3.png').convert_alpha(),
                                   pygame.image.load('res/necromancer_stand_right4.png').convert_alpha()]

# swordsman assets
swordsman_right = pygame.image.load('res/swordsman_stand_right1.png').convert_alpha()
swordsman_right_scaled = pygame.transform.scale(swordsman_right, (300, 300))
swordsman_right_menu = pygame.transform.scale(swordsman_right, (400, 400))
swordsman_death = pygame.image.load('res/swordsman_death.png').convert_alpha()
swordsman_death_scaled = pygame.transform.scale(swordsman_death, (300, 300))
swordsman_left_sprites = [pygame.image.load('res/swordsman_move_left1.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left2.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left3.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left4.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left5.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left6.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left7.png').convert_alpha(),
                          pygame.image.load('res/swordsman_move_left8.png').convert_alpha()]
swordsman_right_sprites = [pygame.image.load('res/swordsman_move_right1.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right2.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right3.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right4.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right5.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right6.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right7.png').convert_alpha(),
                           pygame.image.load('res/swordsman_move_right8.png').convert_alpha()]
swordsman_left_death_sprites = [pygame.image.load('res/swordsman_death_left1.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left2.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left3.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left4.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left5.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left6.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left7.png').convert_alpha(),
                                pygame.image.load('res/swordsman_death_left8.png').convert_alpha()]
swordsman_right_death_sprites = [pygame.image.load('res/swordsman_death_right1.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right2.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right3.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right4.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right5.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right6.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right7.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_death_right8.png').convert_alpha()]
swordsman_left_stand_sprites = [pygame.image.load('res/swordsman_stand_left1.png').convert_alpha(),
                                pygame.image.load('res/swordsman_stand_left2.png').convert_alpha(),
                                pygame.image.load('res/swordsman_stand_left3.png').convert_alpha(),
                                pygame.image.load('res/swordsman_stand_left4.png').convert_alpha()]
swordsman_right_stand_sprites = [pygame.image.load('res/swordsman_stand_right1.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_stand_right2.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_stand_right3.png').convert_alpha(),
                                 pygame.image.load('res/swordsman_stand_right4.png').convert_alpha()]

# red enemy assets
red_enemy_right = pygame.image.load('res/red_enemy_move_right1.png').convert_alpha()
red_enemy_left = pygame.image.load('res/red_enemy_move_left1.png').convert_alpha()
red_enemy_left_sprites = [pygame.image.load('res/red_enemy_move_left1.png').convert_alpha(),
                          pygame.image.load('res/red_enemy_move_left2.png').convert_alpha()]
red_enemy_right_sprites = [pygame.image.load('res/red_enemy_move_right1.png').convert_alpha(),
                           pygame.image.load('res/red_enemy_move_right2.png').convert_alpha()]
red_enemy_left_death_sprites = [pygame.image.load('res/red_enemy_death_left1.png').convert_alpha(),
                                pygame.image.load('res/red_enemy_death_left2.png').convert_alpha(),
                                pygame.image.load('res/red_enemy_death_left3.png').convert_alpha(),
                                pygame.image.load('res/red_enemy_death_left4.png').convert_alpha()]
red_enemy_right_death_sprites = [pygame.image.load('res/red_enemy_death_right1.png').convert_alpha(),
                                 pygame.image.load('res/red_enemy_death_right2.png').convert_alpha(),
                                 pygame.image.load('res/red_enemy_death_right3.png').convert_alpha(),
                                 pygame.image.load('res/red_enemy_death_right4.png').convert_alpha()]
red_enemy_left_attack_sprites = [pygame.image.load('res/red_enemy_attack_left1.png').convert_alpha(),
                                 pygame.image.load('res/red_enemy_attack_left2.png').convert_alpha(),
                                 pygame.image.load('res/red_enemy_attack_left3.png').convert_alpha(),
                                 pygame.image.load('res/red_enemy_attack_left4.png').convert_alpha()]
red_enemy_right_attack_sprites = [pygame.image.load('res/red_enemy_attack_right1.png').convert_alpha(),
                                  pygame.image.load('res/red_enemy_attack_right2.png').convert_alpha(),
                                  pygame.image.load('res/red_enemy_attack_right3.png').convert_alpha(),
                                  pygame.image.load('res/red_enemy_attack_right4.png').convert_alpha()]


# green enemy assets
green_enemy_right = pygame.image.load('res/green_enemy_move_right1.png').convert_alpha()
green_enemy_left = pygame.image.load('res/green_enemy_move_left1.png').convert_alpha()
green_enemy_left_sprites = [pygame.image.load('res/green_enemy_move_left1.png').convert_alpha(),
                            pygame.image.load('res/green_enemy_move_left2.png').convert_alpha()]
green_enemy_right_sprites = [pygame.image.load('res/green_enemy_move_right1.png').convert_alpha(),
                             pygame.image.load('res/green_enemy_move_right2.png').convert_alpha()]
green_enemy_left_death_sprites = [pygame.image.load('res/green_enemy_death_left1.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_death_left2.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_death_left3.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_death_left4.png').convert_alpha()]
green_enemy_right_death_sprites = [pygame.image.load('res/green_enemy_death_right1.png').convert_alpha(),
                                   pygame.image.load('res/green_enemy_death_right2.png').convert_alpha(),
                                   pygame.image.load('res/green_enemy_death_right3.png').convert_alpha(),
                                   pygame.image.load('res/green_enemy_death_right4.png').convert_alpha()]
green_enemy_left_blow_sprites = [pygame.image.load('res/green_enemy_blow_left1.png').convert_alpha(),
                                 pygame.image.load('res/green_enemy_blow_left2.png').convert_alpha(),
                                 pygame.image.load('res/green_enemy_blow_left3.png').convert_alpha(),
                                 pygame.image.load('res/green_enemy_blow_left4.png').convert_alpha(),
                                 pygame.image.load('res/green_enemy_blow_left5.png').convert_alpha()]
green_enemy_right_blow_sprites = [pygame.image.load('res/green_enemy_blow_right1.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_blow_right2.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_blow_right3.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_blow_right4.png').convert_alpha(),
                                  pygame.image.load('res/green_enemy_blow_right5.png').convert_alpha()]

# skills arrows
arrow_right = pygame.image.load('res/arrow_right.png').convert_alpha()
arrow_top_right = pygame.image.load('res/arrow_top_right.png').convert_alpha()
arrow_bottom_right = pygame.image.load('res/arrow_bottom_right.png').convert_alpha()

# knight skills assets
knight_basic_attack_icon = pygame.image.load('res/knight_basic_attack_icon.png').convert_alpha()

# angel skills assets
angel_skill3_animation = pygame.image.load('res/angel_skill3_animation.png').convert_alpha()
angel_basic_attack_icon = pygame.image.load('res/angel_basic_attack_icon.png').convert_alpha()
in_game_angel_skill3_icon = pygame.image.load('res/angel_skill3_icon.png').convert_alpha()
in_game_angel_skill6_icon = pygame.image.load('res/angel_skill6_icon.png').convert_alpha()
in_game_angel_skill9_icon = pygame.image.load('res/angel_skill9_icon.png').convert_alpha()
in_game_angel_skill12_icon = pygame.image.load('res/angel_skill12_icon.png').convert_alpha()
tree_angel_skill1_icon = pygame.transform.scale(pygame.image.load('res/angel_skill1_icon.png').convert_alpha(), (200, 200))
tree_angel_skill2_icon = pygame.transform.scale(pygame.image.load('res/angel_skill2_icon.png').convert_alpha(), (200, 200))
tree_angel_skill3_icon = pygame.transform.scale(pygame.image.load('res/angel_skill3_icon.png').convert_alpha(), (200, 200))
tree_angel_skill4_icon = pygame.transform.scale(pygame.image.load('res/angel_skill4_icon.png').convert_alpha(), (200, 200))
tree_angel_skill5_icon = pygame.transform.scale(pygame.image.load('res/angel_skill5_icon.png').convert_alpha(), (200, 200))
tree_angel_skill6_icon = pygame.transform.scale(pygame.image.load('res/angel_skill6_icon.png').convert_alpha(), (200, 200))
tree_angel_skill7_icon = pygame.transform.scale(pygame.image.load('res/angel_skill7_icon.png').convert_alpha(), (200, 200))
tree_angel_skill8_icon = pygame.transform.scale(pygame.image.load('res/angel_skill8_icon.png').convert_alpha(), (200, 200))
tree_angel_skill9_icon = pygame.transform.scale(pygame.image.load('res/angel_skill9_icon.png').convert_alpha(), (200, 200))
tree_angel_skill10_icon = pygame.transform.scale(pygame.image.load('res/angel_skill10_icon.png').convert_alpha(), (200, 200))
tree_angel_skill11_icon = pygame.transform.scale(pygame.image.load('res/angel_skill11_icon.png').convert_alpha(), (200, 200))
tree_angel_skill12_icon = pygame.transform.scale(pygame.image.load('res/angel_skill12_icon.png').convert_alpha(), (200, 200))

# assassin skills assets
assassin_basic_attack_icon = pygame.image.load('res/assassin_basic_attack_icon.png').convert_alpha()

# mage skills assets
mage_basic_attack_icon = pygame.image.load('res/mage_basic_attack_icon.png').convert_alpha()

# necromancer skills assets
necromancer_basic_attack_icon = pygame.image.load('res/necromancer_basic_attack_icon.png').convert_alpha()

# swordsman skills assets
swordsman_basic_attack_icon = pygame.image.load('res/swordsman_basic_attack_icon.png').convert_alpha()
swordsman_basic_attack_animation_sprites = [pygame.image.load('res/swordsman_basic_attack_animation1.png').convert_alpha(),
                                            pygame.image.load('res/swordsman_basic_attack_animation2.png').convert_alpha(),
                                            pygame.image.load('res/swordsman_basic_attack_animation3.png').convert_alpha(),
                                            pygame.image.load('res/swordsman_basic_attack_animation4.png').convert_alpha(),
                                            pygame.image.load('res/swordsman_basic_attack_animation5.png').convert_alpha()]

# item assets
health = pygame.image.load('res/health.png').convert_alpha()
health_potion = pygame.image.load('res/health_potion.png').convert_alpha()
gold = pygame.image.load('res/gold.png').convert_alpha()
armor = pygame.image.load('res/armor.png').convert_alpha()
attack_damage = pygame.image.load('res/attack_damage.png').convert_alpha()
item_shadow = pygame.image.load('res/item_shadow.png').convert_alpha()

# buttons assets
button_750x100_image = pygame.image.load('res/button_750x100_image_default.png').convert_alpha()
button_750x100_image_pressed = pygame.image.load('res/button_750x100_image_active.png').convert_alpha()
button_360x100_image = pygame.image.load('res/button_360x100_image_default.png').convert_alpha()
button_360x100_image_pressed = pygame.image.load('res/button_360x100_image_active.png').convert_alpha()
button_540x540_image = pygame.image.load('res/button_540x540_image_default.png').convert_alpha()
button_540x540_image_pressed = pygame.image.load('res/button_540x540_image_active.png').convert_alpha()
button_arrow_image_right = pygame.image.load('res/button_arrow_image_default_right.png').convert_alpha()
button_arrow_image_right_pressed = pygame.image.load('res/button_arrow_image_active_right.png').convert_alpha()
button_arrow_image_left = pygame.image.load('res/button_arrow_image_default_left.png').convert_alpha()
button_arrow_image_left_pressed = pygame.image.load('res/button_arrow_image_active_left.png').convert_alpha()
skill_description = pygame.transform.scale(button_540x540_image, (450, 605))
