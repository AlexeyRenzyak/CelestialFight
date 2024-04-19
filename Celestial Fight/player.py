import pygame
import math

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, speed, damage, dampening, rof):
        super().__init__() 
        self.imageorigin = pygame.image.load("Assets/Visual/Player.png")
        self.image = self.imageorigin
        self.rect = self.image.get_rect()
        self.rect.center = (1280/2, 720/2)
        self.rotation = 0
        self.speed = speed
        self.damage = damage
        self.rotation = 0
        self.dampening = dampening
        self.x = 1280/2
        self.y = 720/2
        self.rof = rof
        self.velocity = [0, 0]
    
    def process(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotation += 3
        elif keys[pygame.K_d]:
            self.rotation -= 3
        if keys[pygame.K_w]:
            self.velocity[0] += math.cos(math.radians(self.rotation))*self.speed
            self.velocity[1] += -math.sin(math.radians(self.rotation))*self.speed
        else:
            self.velocity[0] /= self.dampening
            self.velocity[1] /= self.dampening
        self.image = pygame.transform.rotate(self.imageorigin, self.rotation)
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect.center = (round(self.x), round(self.y))
        self.rect = self.image.get_rect(center = self.imageorigin.get_rect(center = self.rect.center).center)

    
    
     