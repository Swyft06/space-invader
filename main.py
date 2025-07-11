import pygame
import os
pygame.font.init()

WIDTH = 900
HEIGHT = 500

WIN = pygame.display.set_mode([WIDTH,HEIGHT])

WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
BLACK = (0,0,0)

BORDER = pygame.Rect(WIDTH // 2-5,0,10,HEIGHT)

HEALTH_FONT = pygame.font.SysFont("comicsans",40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5 #player velocity
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

#To customize the event
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#Brings image out of folder
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','yellowship.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','redship.png'))

#Resizing image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH,HEIGHT))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

#Setting up the health,bullets and ships
def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health),1,WHITE)
    WIN.blit(yellow_health_text,(10,10))
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health),1,WHITE)
    WIN.blit(red_health_text, (700,10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x,red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    pygame.display.update()

#Bullet speed and when it collides 
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL  #move right
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #move left
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


#Moves with ASWD
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:   #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:   #DOWN
        yellow.y += VEL

#Moves with arrow keys
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x  - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1, WHITE)
    #Puts the text at the middle of the screen
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() /2))
    pygame.display.update()
    pygame.time.delay(5000)

#The main code 
def main():
    red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            #Checks if the key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_m and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y, 10,5)
                    red_bullets.append(bullet)
            #Removes helath when it is hit
            if event.type == RED_HIT:
                red_health -= 1
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        
        winner_text = ""
        if red_health < 0:
            winner_text = "Yellow Wins!"
        if yellow_health < 0 :
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        #Recalling functions
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)

    main()

#Code continues forever until quitted
if __name__ == "__main__":
    main()



