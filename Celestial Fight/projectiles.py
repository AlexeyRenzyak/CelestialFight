import pygame
import math

pygame.init()

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, point, speed, direction, lifetime):
        super().__init__()
        self.image = pygame.image.load("Assets/Visual/PlayerBullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = point
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.speed = speed
        self.direction = direction
        self.velocity = [0,0]
        self.lifetime = lifetime
        self.timer = 0
        self.velocity[0] = math.cos(math.radians(self.direction))*self.speed
        self.velocity[1] = -math.sin(math.radians(self.direction))*self.speed

    def process(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.timer += 1
        self.rect.center = (round(self.x), round(self.y))