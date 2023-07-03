import pygame

# game assets
current_state_image = pygame.image.load('res/background.png').convert_alpha()
blurred_current_state_image = pygame.image.load('res/background.png').convert_alpha()

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

# angel assets
angel_right = pygame.image.load('res/angel_move_right3.png').convert_alpha()
angel_right_scaled = pygame.transform.scale(angel_right, (300, 300))
angel_right_menu = pygame.transform.scale(angel_right, (400, 400))
angel_death = pygame.image.load('res/angel_death.png').convert_alpha()
angel_death_scaled = pygame.transform.scale(angel_death, (300, 300))
angel_left_sprites = [pygame.image.load('res/angel_move_left1.png').convert_alpha(),
                      pygame.image.load('res/angel_move_left2.png').convert_alpha(),
                      pygame.image.load('res/angel_move_left3.png').convert_alpha(),
                      pygame.image.load('res/angel_move_left4.png').convert_alpha()]
angel_right_sprites = [pygame.image.load('res/angel_move_right1.png').convert_alpha(),
                       pygame.image.load('res/angel_move_right2.png').convert_alpha(),
                       pygame.image.load('res/angel_move_right3.png').convert_alpha(),
                       pygame.image.load('res/angel_move_right4.png').convert_alpha()]
angel_left_death_sprites = [pygame.image.load('res/angel_death_left1.png').convert_alpha(),
                            pygame.image.load('res/angel_death_left2.png').convert_alpha(),
                            pygame.image.load('res/angel_death_left3.png').convert_alpha(),
                            pygame.image.load('res/angel_death_left4.png').convert_alpha(),
                            pygame.image.load('res/angel_death_left5.png').convert_alpha(),
                            pygame.image.load('res/angel_death_left6.png').convert_alpha()]
angel_right_death_sprites = [pygame.image.load('res/angel_death_right1.png').convert_alpha(),
                             pygame.image.load('res/angel_death_right2.png').convert_alpha(),
                             pygame.image.load('res/angel_death_right3.png').convert_alpha(),
                             pygame.image.load('res/angel_death_right4.png').convert_alpha(),
                             pygame.image.load('res/angel_death_right5.png').convert_alpha(),
                             pygame.image.load('res/angel_death_right6.png').convert_alpha()]
angel_left_stand_sprites = angel_left_sprites
angel_right_stand_sprites = angel_right_sprites

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

# slash attack assets
slash_attack_animation_sprites = [pygame.image.load('res/slash_attack_animation1.png').convert_alpha(),
                                  pygame.image.load('res/slash_attack_animation2.png').convert_alpha(),
                                  pygame.image.load('res/slash_attack_animation3.png').convert_alpha(),
                                  pygame.image.load('res/slash_attack_animation4.png').convert_alpha(),
                                  pygame.image.load('res/slash_attack_animation5.png').convert_alpha()]

# hp assets
hp_heart = pygame.image.load('res/hp_heart.png').convert_alpha()
hp_heart_shadow = pygame.image.load('res/hp_heart_shadow.png').convert_alpha()

# buttons assets
start_button_image = pygame.Surface([750, 100])
settings_button_image = pygame.Surface([750, 100])
credits_button = pygame.Surface([360, 100])
exit_button_image = pygame.Surface([360, 100])
character_button_image = pygame.Surface([540, 540])
play_button_image = pygame.Surface([360, 100])
back_button_image = pygame.Surface([360, 100])
