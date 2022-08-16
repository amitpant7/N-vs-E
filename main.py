import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
NEWTON_WIDTH, NEWTON_HEIGHT = 80, 80
EINSTEIN_WIDTH, EINSTEIN_HEIGHT = 70, 75
RAN1_EINSTEIN = random.randint(50, 100)
RAN2_EINSTEIN = random.randint(-100, 200)
BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("N Vs E")

# Events
RED_HIT = pygame.USEREVENT+1
YELLOW_HIT = pygame.USEREVENT+2

# health
red_health = 100
yellow_health = 100


# Consts color , frame rate bullets 
BLACK = (0, 0, 0)
PURPLE = (75, 0, 130)
COLOR = WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3  #no of bullets that can be fired without waiting 

#Loading Images 
NEWTON_image = pygame.image.load(os.path.join('Assets', 'newton.jpg'))
NEWTON = pygame.transform.scale(NEWTON_image, (NEWTON_WIDTH, NEWTON_HEIGHT))
EINSTEIN_image = pygame.image.load(os.path.join('Assets', 'einstein.jpg'))
EINSTEIN = pygame.transform.scale(EINSTEIN_image, (EINSTEIN_WIDTH, EINSTEIN_HEIGHT))
VOTE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'sci.jpg')), (WIDTH, HEIGHT))
APPLE_imgae = pygame.image.load(os.path.join('Assets', 'apple.png'))
APPLE = pygame.transform.scale(APPLE_imgae, (13, 13))
PHOTON = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'photon.png')), (100, 20))

#font for dispalying health
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT= pygame.font.SysFont('comicsans', 28)

#The list gets appended when bullet is fired
red_bullets = []  # red bullets= PHOTON
yellow_bullets = []  # yellow bullets= apple


#Display Winner 
winner_text = ""


#Draws windows, renders objects on screen and updates them 
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health,winner_text):
    WIN.blit(VOTE, (0, 0))
    pygame.draw.rect(WIN, PURPLE, BORDER)

    #Rendering Healt of Players 
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (WIDTH-yellow_health_text.get_width()-10, 10))
    
    #Intial Position Players
    WIN.blit(NEWTON, (red.x, red.y))
    WIN.blit(EINSTEIN, (yellow.x, yellow.y))
    #WIN.blit(HAS,(red.x+80, red.y+40) )
    for bullet in red_bullets:
        WIN.blit(APPLE, (bullet.x, bullet.y))
        #pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        WIN.blit(PHOTON, (bullet.x, bullet.y))
        #pygame.draw.rect(WIN, YELLOW, bullet)
    
    winner= WINNER_FONT.render(str(winner_text), 1, WHITE)
    WIN.blit(winner, (WIDTH/2-70, HEIGHT/2))
    #Update the frame 
    pygame.display.update()
    

#Moving the Players
def red_handel_movement(keys, red):
    if keys[pygame.K_a] and red.x-VEL > 0:  # left
        red.x -= VEL
    if keys[pygame.K_d] and red.x < BORDER.x-NEWTON_WIDTH:  # Right
        red.x += VEL
    if keys[pygame.K_w] and red.y-VEL > 0:  # UP
        red.y -= VEL
    if keys[pygame.K_s] and red.y+VEL+NEWTON_HEIGHT < HEIGHT:  # Dow
        red.y += VEL


def yellow_handel_movement(keys, yellow):
    if keys[pygame.K_LEFT] and yellow.x-VEL > BORDER.x:  # left
        yellow.x -= VEL
    if keys[pygame.K_RIGHT] and yellow.x < WIDTH-EINSTEIN_WIDTH:  # Right
        yellow.x += VEL
    if keys[pygame.K_UP] and yellow.y-VEL > 0:  # UP
        yellow.y -= VEL
    if keys[pygame.K_DOWN] and yellow.y+VEL+NEWTON_HEIGHT < HEIGHT:  # Dow
        yellow.y += VEL


#Handeling the bullets and appending list when fired 
def handle_bullets(yellow_bullets, red_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)
            
def Quit():
    pygame.quit()


def main():
    # rectangle to control the player movement, x,y,wid, heig
    red = pygame.Rect(100, 300, NEWTON_WIDTH, NEWTON_HEIGHT)
    yellow = pygame.Rect(700, 0, EINSTEIN_WIDTH, EINSTEIN_HEIGHT)
    global red_health  # As we will change this inside main()
    global yellow_health
    global winner_text
    clock = pygame.time.Clock()  # control the fram rate
    run = True
    while run:
        clock.tick(FPS)

        # defferent events and looping through them
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:  # pressed the key
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x+red.width, red.y+red.height//2, 10, 5)
                    red_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y+yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 10
            if event.type == YELLOW_HIT:
                yellow_health -= 10

        if (red_health <= 0):
            winner_text = "EINSTEIN Wins"
            
        if (yellow_health <= 0):
            winner_text = "NEWTON Wins"

      
        # what keys are currently pressed everytime loops
       
        keys_pressed = pygame.key.get_pressed()
        red_handel_movement(keys_pressed, red)
        yellow_handel_movement(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, red, yellow)
            
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, winner_text)
    Quit()


if __name__ == '__main__':  # only run if the file is run directly , won't run while importing!
    main()
