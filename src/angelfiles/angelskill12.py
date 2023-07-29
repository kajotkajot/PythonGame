from src.assets import *


class AngelSkill12(pygame.sprite.Sprite):
    def __init__(self, player, group, enemy_group, timer):
        super().__init__(group)
        self.player = player
        self.enemy_group = enemy_group
        self.timer = timer
        self.damage = self.player.attack * self.player.skill12.current_value
        self.image = angel_skill12_animation
        self.hit_box = angel_skill12_hit_box
        self.mouse_pos = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(midbottom=(self.mouse_pos[0], self.mouse_pos[1] + 120)).move(self.player.rect.centerx - 960, self.player.rect.y - 540)
        self.hit_box_rect = self.hit_box.get_rect(center=self.mouse_pos).move(self.player.rect.centerx - 960, self.player.rect.y - 540)
        self.hit_box_mask = pygame.mask.from_surface(self.hit_box)
        self.current_time = pygame.time.get_ticks()

    def check_state(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > self.player.skill12_duration:
            self.kill()

    def check_collision(self):
        for enemy in self.enemy_group:
            if self.hit_box_rect.colliderect(enemy.rect):
                if self.hit_box_mask.overlap(enemy.mask, (enemy.rect.x - self.hit_box_rect.x, enemy.rect.y - self.hit_box_rect.y)):
                    enemy.hp -= self.damage*(1-((enemy.armor*self.player.armor_reduction)/((enemy.armor*self.player.armor_reduction)+99)))
        if self.hit_box_rect.colliderect(self.player.rect):
            if self.hit_box_mask.overlap(self.player.mask, (self.player.rect.x - self.hit_box_rect.x, self.player.rect.y - self.hit_box_rect.y)):
                self.player.current_hp -= self.damage*(1-(self.player.armor/(self.player.armor+99)))

    def update(self):
        self.check_state()
        self.check_collision()
