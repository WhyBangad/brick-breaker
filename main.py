import pygame, time, math

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption('Brick Breaker')
pygame.display.set_icon(pygame.image.load('./img/joystick.png'))

class Ball(pygame.sprite.Sprite):
    SIZE = 32
    LOC = (400, 300)
    # VEL = [1, 1]
    VEL = [2, 2]
    VEL_BOUND = [6, 8]
    CENTRE = 32*math.sqrt(2)
    BNDRY_H = SCREEN_SIZE[0] - SIZE
    BNDRY_V = SCREEN_SIZE[1] - SIZE
    MARGIN_V = 20
    img = pygame.image.load('./img/ball.png')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Ball.img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Ball.LOC
        self.velocity = Ball.VEL
    
    def draw(self, screen:pygame.surface.Surface):
        screen.blit(self.image, self.rect)
    
    def update(self):
        if self.rect.x + self.velocity[0] >= Ball.BNDRY_H  or self.rect.x + self.velocity[0] < 0:
            self.velocity[0] *= -1
            if abs(self.velocity[0]) > Ball.VEL_BOUND[0]:
                self.velocity[0] = math.copysign(Ball.VEL_BOUND[0], self.velocity[0])
        if self.rect.y + self.velocity[1] < Ball.MARGIN_V:
            self.velocity[1] *= -1
            if abs(self.velocity[1]) > Ball.VEL_BOUND[1]:
                self.velocity[1] = math.copysign(Ball.VEL_BOUND[1], self.velocity[1])
        self.rect.move_ip(self.velocity[0], self.velocity[1])

class Brick(pygame.sprite.Sprite):
    img = pygame.image.load('./img/brick.png')
    SIZE = 64
    CENTRE = 32
    CORNER_SLOPE = 0.5

    def __init__(self, coords: tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image = Brick.img
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = coords

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def update(self, ball: Ball):
        if self.rect.colliderect(ball.rect):
            self.kill()
            curr_x, curr_y = (self.rect.x+self.CENTRE, self.rect.y+self.CENTRE)
            ball_x, ball_y = (ball.rect.x + ball.CENTRE, ball.rect.y + ball.CENTRE)
            if curr_x == ball_x:
                ball.velocity[1] *= -1
            elif curr_y == ball_y:
                ball.velocity[0] *= -1
            else:
                if ball.rect.x < self.rect.x or ball.rect.x > self.rect.x + self.SIZE:
                    ball.velocity[0] *= -1
                else:
                    ball.velocity[1] *= -1            

class Grid(pygame.sprite.Group):
    def __init__(self, rows: int, cols: int):
        pygame.sprite.Group.__init__(self)
        self.rows = rows
        self.cols = cols
        self.margin_h = (SCREEN_SIZE[0] - self.cols*Brick.SIZE)/2
        self.margin_v = 20
        self.broken = 0
        [[self.add(Brick((self.margin_h+ j*Brick.SIZE, self.margin_v + i*Brick.SIZE))) for j in range(cols)] for i in range(rows)]

    def update(self, ball: Ball):
        for sprite in self.sprites():
            if sprite.rect.colliderect(ball.rect):
                sprite.update(ball)
                self.broken += 1
                break

class Platform(pygame.sprite.Sprite):
    platform = pygame.image.load('./img/platform.png')
    LOC = (400, 550)
    VEL = [0.0, 0.0]
    # VEL_CHANGE = 1
    VEL_CHANGE = 2
    SIZE = 64
    BNDRY_H = SCREEN_SIZE[0] - SIZE

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Platform.platform
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = Platform.LOC
        self.velocity = Platform.VEL

    def draw(self, screen:pygame.Surface):
        screen.blit(self.image, self.rect)

    def update(self, ball: Ball):
        if self.rect.x + self.velocity[0] >= self.BNDRY_H  or self.rect.x + self.velocity[0] <= 0:
            self.velocity[0] = 0
        self.rect.move_ip(self.velocity[0], self.velocity[1])
        if pygame.Rect.colliderect(self.rect.move(0, Platform.SIZE/2), ball.rect):
            ball.velocity[1] *= -1
            ball.velocity[0] += int(self.velocity[0]/3)
            if ball.velocity[0] == 0:
                if self.velocity[0] > 0:
                    ball.velocity[0] = 1
                elif self.velocity[0] < 0:
                    ball.velocity = -1

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

    def draw(self, score:int, time:int) -> None:
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
        grid = Grid(rows=3, cols=10)
        platform = Platform()
        run = True
        timer, start_ticks = diff_timer_map[difficulty], pygame.time.get_ticks()
        clock = pygame.time.Clock()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        platform.velocity[0] -= Platform.VEL_CHANGE
                    if event.key == pygame.K_RIGHT:
                        platform.velocity[0] += Platform.VEL_CHANGE
            if len(grid.sprites()) == 0:
                self.game_over('W')
                run = False
            ball.update()
            platform.update(ball=ball)
            if ball.rect.y + ball.velocity[1] >= Ball.BNDRY_V:
                self.game_over('L', grid.broken)
                run = False
            elif timer - int((pygame.time.get_ticks()-start_ticks)/1000) <= 0:
                self.game_over('T')
                run = False
            if run == False:
                break
            grid.update(ball=ball)
            screen.fill((0,0,0))
            self.draw(grid.broken, timer - int((pygame.time.get_ticks()-start_ticks)/1000))
            grid.draw(screen)
            platform.draw(screen)
            ball.draw(screen)
            pygame.display.update()
            clock.tick(120)

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