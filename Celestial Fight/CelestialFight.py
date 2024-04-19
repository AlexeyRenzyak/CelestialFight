import pygame
import menu
import player
import projectiles

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Fight")
clock = pygame.time.Clock()

end = False

in_menu = True

Ship = player.Player(0.1, 1, 1.005, 10)
reloading_time = Ship.rof

Bullets = pygame.sprite.Group()

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
        if reloading_time < Ship.rof:
            reloading_time += 1
        Ship.process()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if reloading_time == Ship.rof:
                Bullets.add(projectiles.PlayerBullet(Ship.rect.center, 15, Ship.rotation, 300))
                reloading_time = 0
        for x in Bullets:
            x.process()
            screen.blit(x.image, x.rect)
            if x.timer >= x.lifetime:
                Bullets.remove(x)
        screen.blit(Ship.image, Ship.rect)
        
        
    pygame.display.flip()
    clock.tick(FPS)
    