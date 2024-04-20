#GUI Auxiliary Module

import pygame
pygame.init()

#Create Main Menu Surface
MainMenu = pygame.Surface((1280, 720))

#Store fonts for use in game
mainmenu_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 100)
button_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 64)
tip_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 38)
ingame_button_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 38)

#Main menu text rendering
title = mainmenu_text_font.render("Celestial Fight", True, (255, 255, 255))
controls1 = tip_text_font.render("Controls", True, (255, 255, 255))
controls2 = tip_text_font.render("W - Forward Thrust", True, (255, 255, 255))
controls3 = tip_text_font.render("A,D - Turn Left/Right", True, (255, 255, 255))
controls4 = tip_text_font.render("Space - Shoot", True, (255, 255, 255))
controls5 = tip_text_font.render("Use mouse to buy upgrades", True, (255, 255, 255))
controls6 = tip_text_font.render("Be aware of inertia!", True, (255, 255, 255))
controls7 = tip_text_font.render("Do not fly past the screen!", True, (255, 255, 255))

#Backgrounds for main menu and gameplay
background1 = pygame.image.load("Assets/Visual/BG1.png")
background2 = pygame.image.load("Assets/Visual/BG2.png")


#Placement of Main menu text
MainMenu.blit(background1, (0, 0))
MainMenu.blit(title, (1280/2-title.get_size()[0]/2, 100))
MainMenu.blit(controls1, (100, 180))
MainMenu.blit(controls2, (20, 240))
MainMenu.blit(controls3, (20, 300))
MainMenu.blit(controls4, (20, 360))
MainMenu.blit(controls5, (20, 420))
MainMenu.blit(controls6, (20, 480))
MainMenu.blit(controls7, (20, 540))


#Button class for in-game buttons
class Button:
    def __init__(self, text, position, bgcolor, hovercolor, action):
        #Text on button
        self.text = text
        #Center's position
        self.position = position
        #Background color
        self.bgcolor = bgcolor
        #Background color under cursor
        self.hovercolor = hovercolor
        #Button's functionality
        self.action = action
        #Rect is set later in main logic
        self.rect = (0,0,0,0)

#All buttons in main menu and game
Buttons = [
    Button("Start Game", (1280/2, 300), (255,255,255), (140, 140, 140), "start"), 
    Button("Quit", (1280/2, 400), (255,255,255), (140, 140, 140), "quit"),
    Button("Toggle Sound", (1280/2, 600), (255,255,255), (140, 140, 140), "sound")]
Ingame_Buttons = [
    Button("Extra Life (500)", (1110, 250), (255,255,255), (140, 140, 140), "upgrade_life_500"),
    Button("Fire Rate Up (300)", (1110, 320), (255,255,255), (140, 140, 140), "upgrade_rof_300"),
    Button("Thrust Up (200)", (1110, 390), (255,255,255), (140, 140, 140), "upgrade_speed_200"),
    Button("Better Dampeners (150)", (1110, 460), (255,255,255), (140, 140, 140), "upgrade_dampening_150"),
    Button("Less Difficulty (300)", (1110, 530), (255,255,255), (140, 140, 140), "upgrade_difficulty_300"),
    Button("Pause", (1030, 650), (255,255,255), (140, 140, 140), "pause"),
    Button("Sound", (1200, 650), (255,255,255), (140, 140, 140), "sound")
    ]
