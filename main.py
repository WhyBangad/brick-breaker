import pygame
import time

# TODO:
# Difficulty level adjusts vertical speed
# In-game timer (also tied with difficulty)
# vertical speed increases when brick decrease

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption('Brick Breaker')
pygame.display.set_icon(pygame.image.load('joystick.png'))

BALL_SIZE = 32
BALL_LOC = (400, 300)
BALL_VEL = [0.3, 1]
ball = pygame.image.load('ball.png')
ball_coords = BALL_LOC
ball_velocity = BALL_VEL
def load_ball(coords):
    screen.blit(ball, coords)

brick = pygame.image.load('brick.png')
BRICK_SIZE = 64
BRICK_HEIGHT = 32
BRICK_ROWS = 3
BRICK_COLS = 12
MARGIN_H = (SCREEN_SIZE[0] - BRICK_COLS*BRICK_SIZE)/2
MARGIN_V = 20
BNDRY_H = SCREEN_SIZE[0] - BALL_SIZE
BNDRY_V = SCREEN_SIZE[1] - BALL_SIZE
broken = [[False for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)]
broken_count = 0
def load_bricks():
    for i in range(BRICK_ROWS):
        for j in range(BRICK_COLS):
            if not broken[i][j]:
                screen.blit(brick, (MARGIN_H + j*BRICK_SIZE, MARGIN_V + i*BRICK_SIZE))

def update_bricks(coords):
    for i in range(BRICK_ROWS):
        for j in range(BRICK_COLS):
            curr_x, curr_y = MARGIN_H + j*BRICK_SIZE, MARGIN_V + i*BRICK_SIZE
            if not broken[i][j] and coords[0]+BALL_SIZE/2 >= curr_x and coords[0]-BALL_SIZE/2 <= curr_x + BRICK_SIZE and coords[1]+BALL_SIZE/2 >= curr_y and coords[1]-BALL_SIZE/2 <= curr_y + BRICK_HEIGHT:
                broken[i][j] = True
                global broken_count
                broken_count += 1

platform = pygame.image.load('platform.png')
PLATFORM_LOC = (400, 550)
PLATFORM_VEL = [0, 0]
VEL_DEGRADE = -0.002
PLATFORM_SIZE = 64
platform_coords = PLATFORM_LOC
platform_velocity = PLATFORM_VEL
def load_platform(coords):
    screen.blit(platform, coords)

def platform_bounce():
    global ball_coords, platform_coords
    if ball_coords[0]+BALL_SIZE/2 >= platform_coords[0] and ball_coords[0]-BALL_SIZE/2 <= platform_coords[0]+PLATFORM_SIZE and ball_coords[1]+BALL_SIZE/2>= platform_coords[1]+PLATFORM_SIZE/4:
        ball_velocity[1] *= -1
        ball_velocity[0] = ball_velocity[0]/2 + platform_velocity[0]/5

font = pygame.font.Font('./basketball-font/Basketball.otf', 30)
SCORE_COORDS = (350,5)
def load_score(score):
    text = font.render('Score : ' + str(score), True, (0,0,0))
    screen.blit(text, SCORE_COORDS)

RESULT_DISPLAY_X = 310
RESULT_DISPLAY_Y = 400
TEXT_DISPLAY_X = 255
TEXT_DISPLAY_Y = 430
SHIFT = 50
background = pygame.transform.scale(pygame.image.load('brick-background.jpg'), (800,600))
def game_over(status):
    time.sleep(1)
    img_size = 256
    result = []
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    if status == 'W':
        result.append((font.render('Congratulations, You won!', True, (0,0,0)), (TEXT_DISPLAY_X-SHIFT/2, RESULT_DISPLAY_Y)))
        margin = (SCREEN_SIZE[0]-img_size)/2, (SCREEN_SIZE[1]-img_size)/2 - SHIFT
        screen.blit(pygame.image.load('success.png'), margin)
    elif status == 'L':
        result.append((font.render(f'Final score : {broken_count}', True, (0,0,0)), (RESULT_DISPLAY_X, RESULT_DISPLAY_Y)))
        result.append((font.render('Better luck next time!', True, (0,0,0)), (TEXT_DISPLAY_X, TEXT_DISPLAY_Y)))
        margin = (SCREEN_SIZE[0]-img_size)/2, (SCREEN_SIZE[1]-img_size)/2 - SHIFT
        screen.blit(pygame.image.load('game-over.png'), margin)
    else:
        # for timeout
        pass
    screen.blits(result)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                run = False

run = True
while run:
    press = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                platform_velocity[0] -= 1
                press = True
            if event.key == pygame.K_RIGHT:
                platform_velocity[0] += 1
                press = True
    if not press:
        if platform_velocity[0] > 0:
            platform_velocity[0] += VEL_DEGRADE
        elif platform_velocity[0] < 0:
            platform_velocity[0] -= VEL_DEGRADE
    if broken_count == BRICK_COLS*BRICK_ROWS:
        game_over('W')
        run = False
    if ball_coords[0] + ball_velocity[0] >= BNDRY_H  or ball_coords[0] + ball_velocity[0] < 0:
        ball_velocity[0] *= -1
    if ball_coords[1] + ball_velocity[1] < MARGIN_V:
        ball_velocity[1] *= -1
    if ball_coords[1] + ball_velocity[1] >= BNDRY_V:
        game_over('L')
        run = False
    if run == False:
        break
    if platform_coords[0] + platform_velocity[0] >= BNDRY_H  or platform_coords[0] + platform_velocity[0] < 0:
        platform_velocity[0] *= -1
    ball_coords = ((ball_coords[0] + ball_velocity[0]), (ball_coords[1] + ball_velocity[1]))
    platform_coords = ((platform_coords[0] + platform_velocity[0]), (platform_coords[1] + platform_velocity[1]))
    update_bricks(ball_coords)
    platform_bounce()
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    load_platform(platform_coords)
    load_ball(ball_coords)
    load_bricks()
    load_score(broken_count)
    pygame.display.update()