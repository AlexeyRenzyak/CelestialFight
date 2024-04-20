#Bullets Module
import pygame
import math

pygame.init()

#Player bullet class, processed in Bullets Group
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, point, speed, direction, lifetime):
        super().__init__()
        #Image
        self.image = pygame.image.load("Assets/Visual/PlayerBullet.png")
        #Rect of Image for collisions and drawing
        self.rect = self.image.get_rect()
        #Move the new bullet to point position (point argument)
        self.rect.center = point
        self.x = self.rect.centerx
        self.y = self.rect.centery
        #Bullet's speed
        self.speed = speed
        #Bullet's movement direction in degrees
        self.direction = direction
        #Velocity of movement
        self.velocity = [0,0]
        #Bullet's lifetime, it is destroyed after expiration to prevent memomry leaks
        self.lifetime = lifetime
        #Passed lifetime tracker
        self.timer = 0
        #Velocity assignment derived from direction and speed by using trigonometrical functions
        self.velocity[0] = math.cos(math.radians(self.direction))*self.speed
        self.velocity[1] = -math.sin(math.radians(self.direction))*self.speed
    #Processing function, called every frame
    def process(self):
        #Change position in accordance with velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        #One frame of lifetime has passed, record to timer
        self.timer += 1
        #Centrify the rect to coordinates in space (done not directly due to rect accepting only integer numbers)
        self.rect.center = (round(self.x), round(self.y))

#Enemy bullet class, processed in Asteroids Group
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, point, speed, direction, lifetime):
        super().__init__()
        #Needed to differentiate from asteroids with complex behavior
        self.type = "Bullet"
        #Image
        self.image = pygame.image.load("Assets/Visual/EnemyBullet.png")
        #Rect of Image for drawing
        self.rect = self.image.get_rect()
        #Move the new bullet to point position (point argument)
        self.rect.center = point
        self.x = self.rect.centerx
        self.y = self.rect.centery
        #Smaller Hitbox for collisions, to make evasion easier for player
        self.hitbox = pygame.Rect(3, 3, 3, 3)
        self.hitbox.center = self.rect.center
        #Bullet's speed
        self.speed = speed
        #Bullet's movement direction in degrees
        self.direction = direction
        #Velocity of movement
        self.velocity = [0,0]
        #Bullet's lifetime, it is destroyed after expiration to prevent memomry leaks
        self.lifetime = lifetime
        #Passed lifetime tracker
        self.timer = 0
        #Velocity assignment derived from direction and speed by using trigonometrical functions
        self.velocity[0] = math.cos(math.radians(self.direction))*self.speed
        self.velocity[1] = -math.sin(math.radians(self.direction))*self.speed

    def process(self):
        #Change position in accordance with velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        #One frame of lifetime has passed, record to timer
        self.timer += 1
        #Centrify the rect and hitbox to coordinates in space (done not directly due to rect accepting only integer numbers)
        self.rect.center = (round(self.x), round(self.y))
        self.hitbox.center = self.rect.center
