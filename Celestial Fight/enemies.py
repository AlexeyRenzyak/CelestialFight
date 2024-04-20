#Enemies Module
import pygame
import math

pygame.init()

#Ordinary asteroid with high HP and medium speed
class Asteroid1(pygame.sprite.Sprite):
    def __init__(self, position, speed, health, rotationspeed, worth):
        super().__init__() 
        #Needed to differentiate from enemy bullets
        self.type = "Asteroid"
        #Original image
        self.imageorigin = pygame.image.load("Assets/Visual/Asteroid1.png")
        #Current image (it will be rotated, so it is different from original)
        self.image = self.imageorigin
        #Image rect for drawing
        self.rect = self.image.get_rect()
        #Smaller Hitbox for collisions, to make evasion easier for player
        self.hitbox = pygame.Rect(32, 32, 32, 32)
        self.hitbox.center = self.rect.center
        #Cosmetical Rotation and its speed
        self.rotation = 0
        self.rotationspeed = rotationspeed
        #Speed of movement
        self.speed = speed
        #How many shots to be destroyed
        self.health = health
        #Coordinates in space from spawn position (position argument)
        self.x = position[0]
        self.y = position[1]
        #Velocity movement
        self.velocity = [0, 0]
        #Price in points for kill
        self.worth = worth
        #Effect after destruction
        self.deatheffect = "None"
    
    def process(self, point):
        #Constant rotation
        self.rotation += self.rotationspeed
        self.image = pygame.transform.rotate(self.imageorigin, self.rotation)
        #Constantly move towards point argument (Player position)
        pos = pygame.math.Vector2(self.x, self.y)
        pos.move_towards_ip(point, self.speed)
        self.x = pos.x
        self.y = pos.y
        #Centrify Rect in accordance to position and rotation and hitbox
        self.rect.center = (round(self.x), round(self.y))
        self.rect = self.image.get_rect(center = self.imageorigin.get_rect(center = self.rect.center).center)
        self.hitbox.center = self.rect.center

#Small fast asteroid with low HP and high speed
class Asteroid2(pygame.sprite.Sprite):
    def __init__(self, position, speed, health, rotationspeed, worth):
        super().__init__() 
        #Needed to differentiate from enemy bullets
        self.type = "Asteroid"
        #Original image
        self.imageorigin = pygame.image.load("Assets/Visual/Asteroid2.png")
        #Current image (it will be rotated, so it is different from original)
        self.image = self.imageorigin
        #Image rect for drawing
        self.rect = self.image.get_rect()
        #Smaller Hitbox for collisions, to make evasion easier for player
        self.hitbox = pygame.Rect(32, 32, 32, 32)
        self.hitbox.center = self.rect.center
        #Cosmetical Rotation and its speed
        self.rotation = 0
        self.rotationspeed = rotationspeed
        #Speed of movement
        self.speed = speed
        #How many shots to be destroyed
        self.health = health
        #Coordinates in space from spawn position (position argument)
        self.x = position[0]
        self.y = position[1]
        #Velocity movement
        self.velocity = [0, 0]
        #Price in points for kill
        self.worth = worth
        #Effect after destruction
        self.deatheffect = "None"
    
    def process(self, point):
        #Constant rotation
        self.rotation += self.rotationspeed
        self.image = pygame.transform.rotate(self.imageorigin, self.rotation)
        #Constantly move towards point argument (Player position)
        pos = pygame.math.Vector2(self.x, self.y)
        pos.move_towards_ip(point, self.speed)
        self.x = pos.x
        self.y = pos.y
        #Centrify Rect in accordance to position and rotation and hitbox
        self.rect.center = (round(self.x), round(self.y))
        self.rect = self.image.get_rect(center = self.imageorigin.get_rect(center = self.rect.center).center)
        self.hitbox.center = self.rect.center 

#Volatile asteroid, similar to Asteroid 1, but shoots 16 bullets in a circle after death
class Asteroid3(pygame.sprite.Sprite):
    def __init__(self, position, speed, health, rotationspeed, worth):
        super().__init__() 
        #Needed to differentiate from enemy bullets
        self.type = "Asteroid"
        #Original image
        self.imageorigin = pygame.image.load("Assets/Visual/Asteroid3.png")
        #Current image (it will be rotated, so it is different from original)
        self.image = self.imageorigin
        #Image rect for drawing
        self.rect = self.image.get_rect()
        #Smaller Hitbox for collisions, to make evasion easier for player
        self.hitbox = pygame.Rect(20, 20, 20, 20)
        self.hitbox.center = self.rect.center
        #Cosmetical Rotation and its speed
        self.rotation = 0
        self.rotationspeed = rotationspeed
        #Speed of movement
        self.speed = speed
        #How many shots to be destroyed
        self.health = health
        #Coordinates in space from spawn position (position argument)
        self.x = position[0]
        self.y = position[1]
        #Velocity movement
        self.velocity = [0, 0]
        #Price in points for kill
        self.worth = worth
        #Effect after destruction
        self.deatheffect = "Explosion"
    
    def process(self, point):
        #Constant rotation
        self.rotation += self.rotationspeed
        self.image = pygame.transform.rotate(self.imageorigin, self.rotation)
        #Constantly move towards point argument (Player position)
        pos = pygame.math.Vector2(self.x, self.y)
        pos.move_towards_ip(point, self.speed)
        self.x = pos.x
        self.y = pos.y
        #Centrify Rect in accordance to position and rotation and hitbox
        self.rect.center = (round(self.x), round(self.y))
        self.rect = self.image.get_rect(center = self.imageorigin.get_rect(center = self.rect.center).center)
        self.hitbox.center = self.rect.center
