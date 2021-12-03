import pygame, time, math

# TODO:
# Difficulty level adjusts vertical speed
# In-game timer (also tied with difficulty)
# vertical speed increases when brick count decreases
# number of balls tied with difficulty

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption('Brick Breaker')
pygame.display.set_icon(pygame.image.load('./img/joystick.png'))

class Ball():
    # change ball's velocity in Ball object
    SIZE = 32
    LOC = (400, 300)
    VEL = [0.3, 1]
    CENTRE = 32*math.sqrt(2)
    BNDRY_H = SCREEN_SIZE[0] - SIZE
    BNDRY_V = SCREEN_SIZE[1] - SIZE
    MARGIN_V = 20
    ball = pygame.image.load('./img/ball.png')

    def __init__(self):
        # add option to pass ball location and image
        self.coords = self.LOC
        self.velocity = self.VEL

    def load(self):
        screen.blit(Ball.ball, self.coords)

    def update(self):
        if self.coords[0] + self.velocity[0] >= Ball.BNDRY_H  or self.coords[0] + self.velocity[0] < 0:
            self.velocity[0] *= -1
        if self.coords[1] + self.velocity[1] < Ball.MARGIN_V:
            self.velocity[1] *= -1
        self.coords = (self.coords[0] + self.velocity[0], self.coords[1] + self.velocity[1])

class Brick():
    brick = pygame.image.load('./img/brick.png')
    SIZE = 64
    CENTRE = 32
    CORNER_SLOPE = 0.5

    def __init__(self, position:tuple, visible:bool) -> None:
        self.coords = position
        self.vis = visible

    def load(self):
        if self.vis:
            global screen
            screen.blit(Brick.brick, self.coords)

    def hit(self):
        self.vis = False

    def visible(self):
        return self.vis

    def bounce(self, ball:Ball):
        curr_x, curr_y = (self.coords[0]+self.CENTRE, self.coords[1]+self.CENTRE)
        ball_x, ball_y = (ball.coords[0] + ball.CENTRE, ball.coords[1] + ball.CENTRE)
        # determine which surface is being hit
        # horizontal, vertical
        hit = [False, False]
        if curr_x == ball_x:
            hit[0] = True
        elif curr_y == ball_y:
            hit[1] = True
        else:
            # corner hit should change speed in both directions
            slope = (curr_y-ball_y)/(curr_x-ball_x)
            if abs(slope) > 1:
                hit[0] = True
            else:
                hit[1] = True
        if hit[0]:
            ball.velocity[1] *= -1
        if hit[1]:
            ball.velocity[0] *= -1

class Grid():
    ROWS = 3
    COLS = 12
    MARGIN_H = (SCREEN_SIZE[0] - COLS*Brick.SIZE)/2
    MARGIN_V = 20

    def __init__(self):
        self.grid = [[Brick(position=(Grid.MARGIN_H + j*Brick.SIZE, Grid.MARGIN_V + i*Brick.SIZE), visible=True) for j in range(Grid.COLS)] for i in range(Grid.ROWS)]
        self.broken = 0

    def empty(self) -> bool:
        return self.broken == Grid.ROWS*Grid.COLS

    def load(self):
        for i in range(Grid.ROWS):
            for j in range(Grid.COLS):
                self.grid[i][j].load()

    def update(self, ball:Ball):
        for i in range(Grid.ROWS):
            for j in range(Grid.COLS):
                brick = self.grid[i][j]
                curr_x, curr_y = brick.coords
                if brick.visible() and ball.coords[0]+ball.SIZE/2 >= curr_x and ball.coords[0]-ball.SIZE/2 <= curr_x + brick.SIZE and ball.coords[1]+ball.SIZE/2 >= curr_y and ball.coords[1]-ball.SIZE/2 <= curr_y + brick.CENTRE:
                    brick.hit()
                    self.broken += 1
                    brick.bounce(ball=ball)
                    break

class Platform():
    platform = pygame.image.load('./img/platform.png')
    LOC = (400, 550)
    VEL = [0, 0]
    VEL_DEGRADE = -0.002
    SIZE = 64
    BNDRY_H = SCREEN_SIZE[0] - SIZE
    BNDRY_V = SCREEN_SIZE[1] - SIZE

    def __init__(self):
        self.coords = Platform.LOC
        self.velocity = Platform.VEL

    def load(self):
        screen.blit(self.platform, self.coords)

    def bounce(self, ball:Ball):
        if ball.coords[0]+ball.SIZE/2 >= self.coords[0] and ball.coords[0]-ball.SIZE/2 <= self.coords[0]+self.SIZE and ball.coords[1]+ball.SIZE/2 >= self.coords[1]+self.SIZE/4:
            ball.velocity[1] *= -1
            ball.velocity[0] = ball.velocity[0]/2 + self.velocity[0]/5
    
    def update(self):
        if self.coords[0] + self.velocity[0] >= self.BNDRY_H  or self.coords[0] + self.velocity[0] <= 0:
            self.velocity[0] *= -1
        self.coords = (self.coords[0] + self.velocity[0], self.coords[1] + self.velocity[1])

class Window():
    SCORE_COORDS = (350,5)
    RESULT_DISPLAY_X = 310
    RESULT_DISPLAY_Y = 400
    TEXT_DISPLAY_X = 255
    TEXT_DISPLAY_Y = 430
    SHIFT = 50
    font = pygame.font.Font('./basketball-font/Basketball.otf', 30)
    background = pygame.transform.scale(pygame.image.load('./img/brick-background.jpg'), (800,600))
    def load(self, score:int) -> None:
        screen.blit(Window.background, (0,0))
        text = Window.font.render('Score : ' + str(score), True, (0,0,0))
        screen.blit(text, Window.SCORE_COORDS)

    def game_over(self, status:str, broken_count:int) -> None:
        time.sleep(1)
        img_size = 256
        result = []
        screen.fill((0,0,0))
        screen.blit(self.background, (0,0))
        if status == 'W':
            result.append((self.font.render('Congratulations, You won!', True, (0,0,0)), (Window.TEXT_DISPLAY_X-Window.SHIFT/2, Window.RESULT_DISPLAY_Y)))
            margin = (SCREEN_SIZE[0]-img_size)/2, (SCREEN_SIZE[1]-img_size)/2 - Window.SHIFT
            screen.blit(pygame.image.load('./img/success.png'), margin)
        elif status == 'L':
            result.append((Window.font.render(f'Final score : {broken_count}', True, (0,0,0)), (Window.RESULT_DISPLAY_X, Window.RESULT_DISPLAY_Y)))
            result.append((Window.font.render('Better luck next time!', True, (0,0,0)), (Window.TEXT_DISPLAY_X, Window.TEXT_DISPLAY_Y)))
            margin = (SCREEN_SIZE[0]-img_size)/2, (SCREEN_SIZE[1]-img_size)/2 - Window.SHIFT
            screen.blit(pygame.image.load('./img/game-over.png'), margin)
        else:
            # for timeout
            pass
        screen.blits(result)
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

ball = Ball()
grid = Grid()
platform = Platform()
window = Window()
run = True
while run:
    press = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                platform.velocity[0] -= 1
                press = True
            if event.key == pygame.K_RIGHT:
                platform.velocity[0] += 1
                press = True
    if not press:
        if platform.velocity[0] > 0:
            platform.velocity[0] += Platform.VEL_DEGRADE
        elif platform.velocity[0] < 0:
            platform.velocity[0] -= Platform.VEL_DEGRADE
    if grid.empty():
        window.game_over('W', grid.broken)
        run = False
    ball.update()
    platform.update()
    if ball.coords[1] + ball.velocity[1] >= Ball.BNDRY_V:
        window.game_over('L', grid.broken)
        run = False
    if run == False:
        break
    grid.update(ball=ball)
    platform.bounce(ball=ball)
    screen.fill((0,0,0))
    window.load(grid.broken)
    platform.load()
    ball.load()
    grid.load()
    pygame.display.update()