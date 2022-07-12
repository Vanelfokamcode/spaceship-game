import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # taille et hauteur de la fenetre
pygame.display.set_caption("First Game!")   # title of the screen 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255,255)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)   # border in the middle of the screen divided by two -5 (half of the border width)
# so that the rectangle will start drawing in the middle of the half - 5 and end in the second half - 5 so that our rectangle stay in the 
# middle of the screen et c'est un rectangle de largeur de l'ecran // 2 et la hauteur de la taille de l'ecran y = 0 , width = 10 


#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60   
VEL = 5  
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))  # to display the image on the WIN
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  # to rotate the image to 90 deg and scale to resize the img width and height

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)  # to rotate the image to 270 deg because we want to face the other yellow spaceship and scale to resize the img width and height

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT)) 


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))  
    pygame.draw.rect(WIN, BLACK, BORDER) # we draw a rectangle on the window with a black color  

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # to display text image etc in the screen yellow.x means that we are drawing at the x position for that
    # move we have to update the x and  y postion 
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT a button to go left  and will check that we not go outside the window the window
        # when we press the left button and - VEL so that we can go to the left and > 0 because the window in the left is on the 0 position
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT  d button to go right on doit s'assurer que lorsqu'on appuie sur la touche de 
        # direction droite ne traverse notre rectangle du milieu et que la largeur ou la grosseur  du yellow ne trepasse la coordonnee x du yellow spaceship
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP the w button to go UP  
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN   we have to check that the yellow spaceship y coordonate + VEL to go down we go from eg 5 to 20 + la taille du yellow doit etre inferieur a la taille 
        # du window not just that - 15 because the yellow 

        yellow.y += VEL


def red_handle_movement(keys_pressed, red):  #take the key_pressed and the red spaceship
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT  if the K_left (c'est le boutton gauche des bouttons de direction)
        # we check that we can't cross the border x position and the border width (so that our red width ne pas se mettre au dessus de notre bordure) #get on top of the border width
        red.x -= VEL # the red spaceship will move to the let donc a gauche 
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL # the red spaceship will move to the right donc a droite 
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL  # red.y now the red spaceship will move up and down that why we considered the y coordinate
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # rectangle with a x and y position 
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = [] #this will basically store the red spaceship bullet in a list []
    yellow_bullets = [] #this will basically store the yellow spaceship bullet in a []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # tell the programm or the game to run only in 60 fps 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()  # show the possibility to the user to quit with the x red 

            if event.type == pygame.KEYDOWN: # that's means if a user type something on the keyboard do the follow instruction
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # if the user press the left control do the follow instruction 
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow) #we call the yellow handle movement after the key_pressed 
        # call function so that the key will be pressed before and then we can go up down R L 
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    main()


if __name__ == "__main__":   # basically tell we gonna run the game in the main not import 
    main()