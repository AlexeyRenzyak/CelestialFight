import pygame

pygame.init()

MainMenu = pygame.Surface((1280, 720))

mainmenu_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 100)
button_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 64)

title = mainmenu_text_font.render("Celestial Fight", True, (255, 255, 255))

MainMenu.blit(title, (1280/2-title.get_size()[0]/2, 100))

class Button:
    def __init__(self, text, position, bgcolor, hovercolor, action):
        self.text = text
        self.position = position
        self.bgcolor = bgcolor
        self.hovercolor = hovercolor
        self.action = action
        self.rect = (0,0,0,0)

Buttons = [Button("Start Game", (1280/2, 300), (255,255,255), (140, 140, 140), "start"), Button("Quit", (1280/2, 400), (255,255,255), (140, 140, 140), "quit")]





""" while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True """