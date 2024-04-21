#Game's Main Script
import pygame
import random
import menu
import player
import projectiles
import enemies

pygame.init()

#Screen resolution/fps
WIDTH, HEIGHT = 1280, 720
FPS = 60

#Screen initiation and caption/icon/clock set
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Fight")
pygame.display.set_icon(pygame.image.load("Assets/Visual/Asteroid1.png"))
clock = pygame.time.Clock()

#Closes the game when true
end = False

#If the player is in main menu
in_menu = True

#GUI Frame during gameplay
Frame = pygame.image.load("Assets/Visual/Frame.png")
#Instantiate a player ship with following stats for game start
Ship = player.Player(0.1, 1.005, 20)
#Shooting timer
reloading_time = Ship.rof
#If the player has lost their life and in process of respawning
dead = False
#Lives. Game ends after dying with zero
lives = 3
#Score
score = 0
#Timer for respawn
respawn_timer = 0

#Timer for enemy spawns and initial spawn number
enemy_timer = 0
enemy_spawn_number = 1

#Difficulty modifier; the game gradually becomes harder and a timer to track the time before next difficulty up
difficulty_mod = 0
difficulty_timer = 0

#Interval between difficulty ups. May be changed to alter the pace
Difficulty_Increase_Cooldown = 600

#Player bullets group
Bullets = pygame.sprite.Group()
#Asteroids and enemy bullets group
Asteroids = pygame.sprite.Group()

#Font for Celestial Fight label on the gameplay GUI Frame
ingame_label_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
#Font for gameplay GUI Elements
ingame_stats_text_font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
#Celestial Fight label
Title = ingame_label_text_font.render("Celestial Fight", True, (200, 150, 255))

#If the game is paused
pause = False
#If the sound is enabled
sound = True

#Sounds
shotsound = pygame.mixer.Sound("Assets/Sound/shot.wav")
killsound = pygame.mixer.Sound("Assets/Sound/kill.wav")

#Main menu music
pygame.mixer.music.load("Assets/Sound/m2.mp3")
pygame.mixer.music.play(-1)

#Game Loop
while not end:
    #Events
    for event in pygame.event.get():
        #Quit the game
        if event.type == pygame.QUIT:
            end = True
        #Main menu button input events
        if in_menu:
            #When the LMB is pressed, check if the cursor hovers any buttons and activate their functions if it does
            if event.type == pygame.MOUSEBUTTONUP:
                for x in menu.Buttons:
                    if x.rect.collidepoint(pygame.mouse.get_pos()):
                        match x.action:
                            #Quit game
                            case "quit":
                                end = True
                            #Game start
                            case "start":
                                in_menu = False
                                if sound:
                                    pygame.mixer.music.load("Assets/Sound/m1.mp3")
                                    pygame.mixer.music.play(-1)
                            #Turn the sound on/off
                            case "sound":
                                if sound == False:
                                    sound = True
                                    pygame.mixer.music.load("Assets/Sound/m2.mp3")
                                    pygame.mixer.music.play(-1)
                                else:
                                    pygame.mixer.music.stop()
                                    sound = False
        else:
            #Game button input events
            if event.type == pygame.MOUSEBUTTONUP:
                for x in menu.Ingame_Buttons:
                    if x.rect.collidepoint(pygame.mouse.get_pos()):
                        #Upgrade buttons
                        if "upgrade" in x.action:
                            #Upgrade actions are in format upgrade_`name of upgrade`_`price`. Split for processing
                            action = x.action.split("_")
                            #If points are sufficient, deduct them and apply boost
                            if score >= int(action[2]):
                                score -= int(action[2])
                                match action[1]:
                                    #Extra life
                                    case 'life':
                                        lives += 1
                                    #Increase rate of fire (Decrease delay, lower limit is 1 frame)
                                    case "rof":
                                        Ship.rof -= 2
                                        if Ship.rof < 1:
                                            Ship.rof = 1
                                    #Increase forward thrust
                                    case "speed": 
                                        Ship.speed += 0.03
                                    #Increase dampening 
                                    case "dampening":
                                        Ship.dampening += 0.005
                                    #Decrease difficulty, lower limit is 0
                                    case "difficulty":
                                        difficulty_mod -= 3
                                        if difficulty_mod < 0:
                                            difficulty_mod = 0
                        #Other actions
                        else:
                            match x.action:
                                #Switch pause
                                case "pause":
                                    if pause == False:
                                        pause = True
                                    else:
                                        pause = False
                                #Switch sound
                                case "sound":
                                    if sound == False:
                                        pygame.mixer.music.load("Assets/Sound/m1.mp3")
                                        pygame.mixer.music.play(-1)
                                        sound = True
                                    else:
                                        pygame.mixer.music.stop()
                                        sound = False


                    

    #Menu loop logic
    if in_menu:
        #Fill the screen with black and blit the Main menu from Menu module
        screen.fill((0,0,0))
        screen.blit(menu.MainMenu, (0,0))
        #Drawing buttons
        for x in menu.Buttons:
            #Rendering text
            text = menu.button_text_font.render(x.text, True, (0,0,0))
            #Creating button surface 
            button = pygame.Surface((text.get_size()[0]+10, text.get_size()[1]+10))
            #Getting and centering rect for cursor tracking
            r = button.get_rect()
            r.center = x.position
            #Fill the background color 
            if r.collidepoint(pygame.mouse.get_pos()):
                button.fill(x.hovercolor)
            #Change the background color when hovered
            else:
                button.fill(x.bgcolor)
            #Insert text and blit the button to menu  
            button.blit(text, (5,5))
            x.rect = r
            menu.MainMenu.blit(button, r)
    #Gameplay loop logic
    else:
        #Kill the player when they are out of screen
        if Ship.hitbox.center[0] > 1000 or Ship.hitbox.center[0] < -20 or Ship.hitbox.center[1] > 740 or Ship.hitbox.center[1] < -20:
            if not dead:
                print("Out of Bounds!")
                dead = True
                if sound:
                    killsound.play()
                #Destroy all asteroids
                for x in Asteroids:
                    Asteroids.remove(x) 
        #Every 180 frames (3 secs) spawn a wave of asteroids
        if enemy_timer >= 180:
            #Reset the timer
            enemy_timer = 0
            #Spawn rate grows with difficulty modifier
            for x in range(enemy_spawn_number + difficulty_mod//10):
                #Randomizer for deciding the spawn side
                randomizer = random.randrange(0, 100)
                #Asteroid type randomizer, more asteroid types appear as difficulty increases
                typerandomizer = 0
                if difficulty_mod >= 15:
                    typerandomizer = random.randrange(0,3)
                    print(typerandomizer)
                elif difficulty_mod >= 5:
                    typerandomizer = random.randrange(0,2)
                #25% chance for spawning up, down, left and right and 1/3 chance of spawn for each asteroid type
                #Everywhere the asteroid hp, speed, and point worth increase with difficulty increase
                if randomizer <= 25:
                    match typerandomizer:
                        case 0:
                            Asteroids.add(enemies.Asteroid1([random.randrange(0,1100),-50], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
                        case 1:
                            Asteroids.add(enemies.Asteroid2([random.randrange(0,1100),-50], 2+((difficulty_mod//5)*0.2), 1, random.uniform(-3, 3), 10+((difficulty_mod//10)*3)))
                        case 2:
                            Asteroids.add(enemies.Asteroid3([random.randrange(0,1100),-50], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
                elif randomizer <= 50:
                    match typerandomizer:
                        case 0:
                            Asteroids.add(enemies.Asteroid1([1125,random.randrange(-10,760)], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
                        case 1:
                            Asteroids.add(enemies.Asteroid2([1125,random.randrange(-10,760)], 2+((difficulty_mod//5)*0.2), 1, random.uniform(-3, 3), 10+((difficulty_mod//10)*3)))
                        case 2:
                            Asteroids.add(enemies.Asteroid3([1125,random.randrange(-10,760)], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
                elif randomizer <= 75:
                    match typerandomizer:
                        case 0:
                            Asteroids.add(enemies.Asteroid1([random.randrange(0,1100),820], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
                        case 1:
                            Asteroids.add(enemies.Asteroid2([random.randrange(0,1100),820], 2+((difficulty_mod//5)*0.2), 1, random.uniform(-3, 3), 10+((difficulty_mod//10)*3)))
                        case 2:
                            Asteroids.add(enemies.Asteroid3([random.randrange(0,1100),820], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))

                else:
                    match typerandomizer:
                        case 0:
                            Asteroids.add(enemies.Asteroid1([-30,random.randrange(-10,760)], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
                        case 1:
                            Asteroids.add(enemies.Asteroid2([-30,random.randrange(-10,760)], 2+((difficulty_mod//5)*0.2), 1, random.uniform(-3, 3), 10+((difficulty_mod//10)*3)))
                        case 2:
                            Asteroids.add(enemies.Asteroid3([-30,random.randrange(-10,760)], 1+((difficulty_mod//5)*0.1), 5+difficulty_mod//10, random.uniform(-2, 1), 20+((difficulty_mod//10)*5)))
        #Increase difficulty and reset timer after cooldown elapsed
        if difficulty_timer >= Difficulty_Increase_Cooldown:
            difficulty_mod += 1
            difficulty_timer = 0
        #Blit starry background
        screen.blit(menu.background2, (0,0))

        #Processing logic, stops during pause
        if pause == False:
            #Increase elapsed time since last shot for shooting cooldown
            if reloading_time < Ship.rof:
                reloading_time += 1
            #Process ship
            Ship.process()
            #Shooting on space button if reload time has elapsed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not dead:
                if reloading_time >= Ship.rof:
                    Bullets.add(projectiles.PlayerBullet(Ship.rect.center, 15, Ship.rotation, 300))
                    reloading_time = 0
                    #Play sound if it is enabled
                    if sound:
                        shotsound.play()
            #Process player bullets
            for x in Bullets:
                x.process()
                #Remove bullets which exceeded their lifetime
                if x.timer >= x.lifetime:
                    Bullets.remove(x)
            #Process Asteroids and Enemy bullets separately (Bullets don't have an argument)
            for x in Asteroids:
                if x.type == "Asteroid":
                    x.process(pygame.math.Vector2(Ship.hitbox.center[0], Ship.hitbox.center[1]))
                else:
                    x.process()
                    #Remove bullets which exceeded their lifetime
                    if x.timer >= x.lifetime:
                        Asteroids.remove(x)
        #Draw player bullets, separately from processing to show them during pause
        for x in Bullets:
            screen.blit(x.image, x.rect)
        
        if not dead:
            #Process timers if not dead and not in pause
            if pause == False:
                enemy_timer += 1
                difficulty_timer += 1
            #Draw the ship and its hitbox as small circle
            screen.blit(Ship.image, Ship.rect)
            pygame.draw.circle(screen, (100,100,100), Ship.hitbox.center, 3)
        else:
            #Fill the screen with red if dead before respawn
            screen.fill((120, 0, 0))
            #Respawn after a second delay if player has a life
            if respawn_timer >= 60 and lives > 0:
                #Deduct a life
                lives -= 1
                #Reset velocity and position to center of playing area
                Ship.velocity = [0,0]
                Ship.x = 950/2
                Ship.y = 720/2
                #Single extra process step for actually moving the ship to prevent this from extra trigger
                Ship.process()
                #Reset respawn timer
                respawn_timer = 0
                #Stop being dead
                dead = False
            #If the player doesn't have a life, return to main menu and reset all progress
            elif respawn_timer >= 60 and lives <= 0:
                lives = 3
                difficulty_mod = 0
                difficulty_timer = 0
                dead = False
                Ship = player.Player(0.1, 1.005, 20)
                in_menu = True
                score = 0
                respawn_timer = 0
                pygame.mixer.music.stop()
                if sound:
                    pygame.mixer.music.load("Assets/Sound/m2.mp3")
                    pygame.mixer.music.play(-1)
            #If the timer hasn't been triggered, add a frame to it
            else:
                respawn_timer += 1
        #Draw asteroids outside of processing for them to be drawn during pause
        for x in Asteroids:
            screen.blit(x.image, x.rect)
        #Process collisions of player bullets with asteroids
        for x in Asteroids:
            if x.type == "Asteroid":
                if pygame.sprite.spritecollideany(x, Bullets):
                    #Deduct health from asteroid when hit
                    x.health -= 1
                    #Delete bullet
                    Bullets.remove(pygame.sprite.spritecollide(x, Bullets,  False)[0])
                    #Delete the asteroid if it has no health, add points and trigger death effects if it has them
                    if x.health <= 0:
                        #Explosion of Asteroid3 (16 enemy bullets in circle pattern)
                        if x.deatheffect == "Explosion":
                            for y in range(16):
                                Asteroids.add(projectiles.EnemyBullet(x.rect.center, 4, 22.5*y, 250))
                        Asteroids.remove(x)
                        score += x.worth
                        #Play sound if enabled
                        if sound:
                            killsound.play()
            #Asteroid collision with player
            if x.hitbox.colliderect(Ship.hitbox):
                print("Asteroid Collision!")
                dead = True
                #Play sound if enabled
                if sound:
                    killsound.play()
                #Destroy all asteroids
                for x in Asteroids:
                    Asteroids.remove(x) 


        #Render text for in-game gui
        ScoreL = ingame_stats_text_font.render("Score: "+str(score), True, (255, 255, 255))
        LivesL = ingame_stats_text_font.render("Lives: "+str(lives), True, (255, 255, 255))
        DifficultyL = ingame_stats_text_font.render("Difficulty: "+str(difficulty_mod), True, (255, 255, 255))
        UpgradesL = ingame_stats_text_font.render("Upgrades", True, (255, 255, 255))

        #Blit the GUI frame and text over it
        screen.blit(Frame, (0,0))
        screen.blit(Title, (965, 20))
        screen.blit(ScoreL, (965, 130))
        screen.blit(LivesL, (965, 80))
        screen.blit(UpgradesL, (1033, 180))
        screen.blit(DifficultyL, (1020, 560))
        #Draw in-game buttons for upgrades, sound and pause toggle
        for x in menu.Ingame_Buttons:
            #Render text
            text = menu.ingame_button_text_font.render(x.text, True, (0,0,0))
            #Create surface button
            button = pygame.Surface((text.get_size()[0]+10, text.get_size()[1]+10))
            #Get its rect and centrify it for cursor detection
            r = button.get_rect()
            r.center = x.position
            #Apply hover background color if it is hovered by cursor
            if r.collidepoint(pygame.mouse.get_pos()):
                button.fill(x.hovercolor)
            #Else apply ordinary background color
            else:
                button.fill(x.bgcolor)
            #Place text and blit the button to screen
            button.blit(text, (5,5))
            x.rect = r
            screen.blit(button, r)

        
    #Pygame processing
    pygame.display.flip()
    clock.tick(FPS)
    