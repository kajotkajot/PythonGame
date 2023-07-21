import math
from assets import *


class AngelSkill3(pygame.sprite.Sprite):
    def __init__(self, player, group, enemy_group, timer):
        super().__init__(group)
        self.player = player
        self.enemy_group = enemy_group
        self.image = angel_skill3_animation
        self.rect = self.image.get_rect().move(self.player.rect.centerx, self.player.rect.centery - 50)
        self.damage = 20
        self.current_time = pygame.time.get_ticks()
        self.offset = pygame.Vector2(650, 0)
        self.timer = timer
        self.mask = pygame.mask.from_surface(self.image)

    def check_state(self):
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - (960 + self.player.current_camera_position.x)
        dy = -(mouse_pos[1] - (540 + self.player.current_camera_position.y))
        angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(angel_skill3_animation, angle - 180)
        rotated_offset = self.offset.rotate(-angle)
        self.rect = self.image.get_rect(center=self.player.rect.center + rotated_offset)
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.timer > self.player.skill3_duration:
            self.kill()

    def check_collision(self):
        for enemy in self.enemy_group:
            if self.rect.colliderect(enemy.rect):
                if self.mask.overlap(enemy.mask, (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)):
                    enemy.hp -= self.damage

    def update(self):
        self.check_state()
        self.check_collision()
