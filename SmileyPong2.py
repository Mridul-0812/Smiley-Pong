import pygame
import time

pygame.init()

# Load background and set the screen
background = pygame.image.load("background.bmp")
background = pygame.transform.scale(background, (800, 600))
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Smiley Pong")

# Load images and set variables
pic = pygame.image.load("Smilee.bmp")
colorkey = pic.get_at((0, 0))
pic.set_colorkey(colorkey)
picx = 0
picy = 0
picw = 100
pich = 100
pic = pygame.transform.scale(pic, (125, 125))

# Set colors and fonts
BLACK = (0, 0, 0)
WHITE = (250, 255, 255)
BLUE = (0, 250, 250)
font = pygame.font.SysFont("Times", 24)

# Game variables and flags
speedx = 5
level = 1
speedy = 5
paddlew = 200
paddleh = 25
paddlex = 300
paddley = 550
points = 0
lives = 5
game_over = False
paused = False
countdown = 150
highest_level_reached = 1
high_score = 0

if points > high_score:
    high_score = points


# Sounds
bounce_sound = pygame.mixer.Sound("bounce.mp3")
game_end = pygame.mixer.Sound("GameOver.mp3")
music = pygame.mixer.music.load("arcade.mp3")
luck = pygame.mixer.Sound("BetterLuck.mp3")
congrats = pygame.mixer.Sound("congratulations.mp3")

music = pygame.mixer.music.set_volume(0.75)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
keepGoing = True
level = 1

luck_sound_played = False
game_end_sound_played = False

def show_text(text, x, y):
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)

while keepGoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:  # Start a new game
                points = 0
                lives = 5
                picx = 0
                picy = 0
                speedx = 5
                speedy = 5
                game_over = False
                countdown = 150
                luck_sound_played = False
                game_end_sound_played = False
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)

            if event.key == pygame.K_SPACE:  # Pause/unpause
                paused = not paused

    if level == 1:  # Level 1 rules
        if points < 2:
            if lives <= 0:
                if not game_over:
                    game_over = True
                    pygame.mixer.music.stop()
                    if not game_end_sound_played:
                        game_end.play()
                        game_end_sound_played = True
                    if not luck_sound_played:
                        time.sleep(1.5)
                        luck.play()
                        luck_sound_played = True
                    game_over_sound_played = True
        else:
            if lives == 0 and level == 1:
                level += 1
                lives = 5
                points = 0
                speedx = 6
                speedy = 6

    elif level == 2:  # Level 2 rules
        if points < 40:
            if lives <= 0:
                if not game_over:
                    game_over = True
                    pygame.mixer.music.stop()
                    if not game_end_sound_played:
                        game_end.play()
                        game_end_sound_played = True
                    if not luck_sound_played:
                        time.sleep(1.5)
                        luck.play()
                        luck_sound_played = True
        else:
            level += level
            lives = 5
            points = 0
            speedx = 7
            speedy = 7
            
    elif level == 3: 
        if points < 60 and lives == 0:
            if not game_over:
                game_over = True
                pygame.mixer.music.stop()
                if not game_end_sound_played:
                    game_end.play()
                    game_end_sound_played = True
                if not luck_sound_played:
                    time.sleep(1.5)
                    luck.play()
                    luck_sound_played = True
            if points >= 60 and lives == 0:
                game_over = True
                game_end.play()
                game_end_sound_played = True

    if not game_over:
        if not paused:
            picx += speedx
            picy += speedy

            if picx <= 0 or picx >= 700:
                speedx = -speedx * 1.1
            if picy <= 0:
                speedy = -speedy + 1
            if picy >= 500:
                lives -= 1
                speedy = -5
                speedx = 5
                picy = 499

            if picy + pich >= paddley and picy + pich <= paddley + paddleh and speedy > 0:
                if picx + picw / 2 >= paddlex and picx + picw / 2 <= paddlex + paddlew:
                    bounce_sound.play()
                    speedy = -speedy
                    points += 1

    screen.blit(background, (0, 0))

    if not paused:
        screen.blit(pic, (picx, picy))
        paddlex = pygame.mouse.get_pos()[0] - paddlew / 2
        pygame.draw.rect(screen, BLUE, (paddlex, paddley, paddlew, paddleh))

    show_text(f"Lives: {lives} Points: {points} High Score: {high_score} Level: {level}", 400, 20)

    
    if paused or countdown > 0:
        show_text("Press Space Bar to Pause/Resume", 400, 50)
        countdown = max(0, countdown - 1)

    if level == 1:
        if countdown == 0:
            show_text("You need to score 30 points to unlock LEVEL-2", 400, 50)

    if level == 2:
        show_text("You have successfully unlocked LEVEL-2!", 400, 50)
        show_text("You need to score 40 points in just 4 lives to unlock LEVEL-3.", 390, 75)
    
    if level == 3:
        show_text("You have successfully unlocked the final level!", 400, 50)
        show_text("You need to score 60 points in 5 lives to win.", 390, 75)
    
    if level == 3 and points >= 60:
        if lives == 0:
            show_text("You have passed all levels! You win!", 200, 200 )
    
    if level == 3:
        if event.key == pygame.K_F1:
                points = 0
                lives = 5
                level = 1
                picx = 0
                picy = 0
                speedx = 5
                speedy = 5
                game_over = False
                countdown = 150
                luck_sound_played = False
                game_end_sound_played = False
                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
