import pygame
import menu
import player

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Fight")
clock = pygame.time.Clock()

end = False

in_menu = True

Ship = player.Player(0.1, 1, 5)

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        
        if in_menu:
            if event.type == pygame.MOUSEBUTTONUP:
                for x in menu.Buttons:
                    if x.rect.collidepoint(pygame.mouse.get_pos()):
                        match x.action:
                            case "quit":
                                end = True
                            case "start":
                                in_menu = False
                    


    if in_menu:
        screen.fill((0,0,0))
        screen.blit(menu.MainMenu, (0,0))

        for x in menu.Buttons:
            text = menu.button_text_font.render(x.text, True, (0,0,0))
            button = pygame.Surface((text.get_size()[0]+10, text.get_size()[1]+10))
            r = button.get_rect()
            r.center = x.position

            if r.collidepoint(pygame.mouse.get_pos()):
                button.fill(x.hovercolor)
            else:
                button.fill(x.bgcolor)
            button.blit(text, (5,5))
            x.rect = r
            menu.MainMenu.blit(button, r)
    else:
        screen.fill((50,50,50))
        Ship.process()
        screen.blit(Ship.image, Ship.rect)
        
    pygame.display.flip()
    clock.tick(FPS)
    