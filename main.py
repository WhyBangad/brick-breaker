import pygame, time, math

# TODO:
# Difficulty level adjusts vertical speed
# In-game timer (also tied with difficulty)

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption('Brick Breaker')
pygame.display.set_icon(pygame.image.load('./img/joystick.png'))

class Ball():
    # change ball's velocity in Ball object
    SIZE = 32
    LOC = (400, 300)
    VEL = [0.3, 2]
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
    VEL_CHANGE = 1
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
            self.velocity[0] = 0
        self.coords = (self.coords[0] + self.velocity[0], self.coords[1] + self.velocity[1])

class Window():
    SCORE_COORDS = (200,5)
    TIMER_COORDS = (450, 5)
    RESULT_DISPLAY_X = 310
    RESULT_DISPLAY_Y = 400
    TEXT_DISPLAY_X = 255
    TEXT_DISPLAY_Y = 430
    SHIFT = 50
    font = pygame.font.Font('./font/Basketball.otf', 30)
    background = pygame.transform.scale(pygame.image.load('./img/brick-background.jpg'), (800,600))

    def load(self, score:int, time:int) -> None:
        screen.blit(Window.background, (0,0))
        screen.blit(Window.font.render('Score : ' + str(score), True, (0,0,0)), Window.SCORE_COORDS)
        screen.blit(Window.font.render('Time left : ' + str(time), True, (0,0,0)), Window.TIMER_COORDS)

    def loading_screen(self) -> int:
        font = pygame.font.Font('./font/Team 401.ttf', 30)
        up, down, square = pygame.image.load('./img/up.png'), pygame.image.load('./img/down.png'), pygame.image.load('./img/square.png')
        difficulty = 1
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                        break
                    elif event.key == pygame.K_DOWN:
                        difficulty += 1
                        if difficulty > 4:
                            difficulty = 1
                    elif event.key == pygame.K_UP:
                        difficulty -= 1
                        if difficulty <= 0:
                            difficulty = 4
                if event.type == pygame.QUIT:
                    return -1
            screen.fill((0,0,0))
            screen.blit(self.background, (0,0))
            screen.blit(font.render('Brick breaker game', True, (0,0,0)), (100,100))
            screen.blit(square, (540, 245))
            screen.blit(up, (540, 190))
            screen.blit(font.render(f'Difficulty    {difficulty}', True, (0,0,0)), (180, 250))
            screen.blit(down, (540, 300))
            pygame.display.update()
        return difficulty

    def run_game(self, difficulty:int):
        diff_timer_map = {1: 100, 2: 75, 3: 60, 4: 50}
        ball = Ball()
        grid = Grid()
        platform = Platform()
        run = True
        timer, start_time = diff_timer_map[difficulty], time.time()
        while run:
            press = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if platform.velocity[0] > 0:
                            platform.velocity[0] += -Platform.VEL_CHANGE
                        else:
                            platform.velocity[0] -= Platform.VEL_CHANGE
                        press = True
                    if event.key == pygame.K_RIGHT:
                        if platform.velocity[0] < 0:
                            platform.velocity[0] -= -Platform.VEL_CHANGE
                        else:
                            platform.velocity[0] += Platform.VEL_CHANGE
                        press = True
            if not press:
                if platform.velocity[0] > 0:
                    platform.velocity[0] += Platform.VEL_DEGRADE
                elif platform.velocity[0] < 0:
                    platform.velocity[0] -= Platform.VEL_DEGRADE
            if grid.empty():
                self.game_over('W')
                run = False
            ball.update()
            platform.update()
            if ball.coords[1] + ball.velocity[1] >= Ball.BNDRY_V:
                self.game_over('L', grid.broken)
                run = False
            if timer - int(time.time()-start_time) <= 0:
                self.game_over('T')
                run = False
            if run == False:
                break
            grid.update(ball=ball)
            platform.bounce(ball=ball)
            screen.fill((0,0,0))
            self.load(grid.broken, timer - int(time.time()-start_time))
            platform.load()
            ball.load()
            grid.load()
            pygame.display.update()

    def game_over(self, status:str, broken_count:int=None) -> None:
        time.sleep(1)
        img_size = 256
        result = []
        screen.fill((0,0,0))
        screen.blit(self.background, (0,0))
        margin = (SCREEN_SIZE[0]-img_size)/2, (SCREEN_SIZE[1]-img_size)/2 - Window.SHIFT
        if status == 'W':
            result.append((self.font.render('Congratulations, You won!', True, (0,0,0)), (Window.TEXT_DISPLAY_X-Window.SHIFT/2, Window.RESULT_DISPLAY_Y)))
            screen.blit(pygame.image.load('./img/success.png'), margin)
        elif status == 'L':
            result.append((Window.font.render(f'Final score : {broken_count}', True, (0,0,0)), (Window.RESULT_DISPLAY_X, Window.RESULT_DISPLAY_Y)))
            result.append((Window.font.render('Better luck next time!', True, (0,0,0)), (Window.TEXT_DISPLAY_X, Window.TEXT_DISPLAY_Y)))
            screen.blit(pygame.image.load('./img/game-over.png'), margin)
        elif status == 'T':
            result.append((Window.font.render(f'Timeup! Try to be quicker!', True, (0,0,0)), (Window.TEXT_DISPLAY_X, Window.RESULT_DISPLAY_Y)))
            screen.blit(pygame.image.load('./img/timeout.png'), margin)
        screen.blits(result)
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False

if __name__ == '__main__':
    game_window = Window()
    difficulty = game_window.loading_screen()
    if difficulty != -1:
        game_window.run_game(difficulty)