#Player Logic Module
import pygame
import math

pygame.init()

#Player ship class
class Player(pygame.sprite.Sprite):
    def __init__(self, speed, dampening, rof):
        super().__init__() 
        #Original image of the ship
        self.imageorigin = pygame.image.load("Assets/Visual/Player.png")
        #Current image of the ship (it will be rotated, so it is different from original)
        self.image = self.imageorigin
        #Player's rectangle setup from image
        self.rect = self.image.get_rect()
        #Small hitbox setup for easier evasion (6x6 pixels rectangle)
        self.hitbox = pygame.Rect(3, 3, 3, 3)
        self.hitbox.center = self.rect.center
        #Initial rotation in degrees
        self.rotation = 0
        #Power of forward thrust
        self.speed = speed
        #Inertia dampening coefficient
        self.dampening = dampening
        #Coordinates in space
        self.x = 950/2
        self.y = 720/2
        #Rate of Fire
        self.rof = rof
        #Velocity, used in movement logic
        self.velocity = [0, 0]
    #Processing function, called every frame
    def process(self):
        #Rotate if A or D are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotation += 3
        elif keys[pygame.K_d]:
            self.rotation -= 3

        #Change the velocity in accordance to rotation by using trigonomertical functions
        if keys[pygame.K_w]:
            self.velocity[0] += math.cos(math.radians(self.rotation))*self.speed
            self.velocity[1] += -math.sin(math.radians(self.rotation))*self.speed
        #Without thrust, slowly stops the inertial movement
        else:
            self.velocity[0] /= self.dampening
            self.velocity[1] /= self.dampening
        #Rotation of image in accordance to in-game rotation
        self.image = pygame.transform.rotate(self.imageorigin, self.rotation)
        #Change the position in accordance with velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        #Centrify the rect to coordinates in space (done not directly due to rect accepting only integer numbers)
        self.rect.center = (round(self.x), round(self.y))
        #Adapt the rect to rotated image and centrify it around original image's center
        self.rect = self.image.get_rect(center = self.imageorigin.get_rect(center = self.rect.center).center)
        #Move the hitbox to center
        self.hitbox.center = self.rect.center

    
    
     
