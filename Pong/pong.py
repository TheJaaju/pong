#Ping pong game
import pygame
from random import randint

pygame.init()

# --- Color list
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (255,100,150)

# --- Window Stats
resolution = (700,500)
title = ("Pong")

# --- Creating the window
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption(title)


# --- Paddle code
class Paddle(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        super().__init__()

        # --- Paddle Speed
        #self.paddleSpeed = 0.1

        # --- Stuff for the paddles
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # --- Drawing the paddle
        pygame.draw.rect(self.image, color, [0,0, width, height])

        self.rect = self.image.get_rect()

    # --- Code for moving the paddle up
    def moveUp(self, pixels):
        self.rect.y -= pixels

        if self.rect.y < 0:
            self.rect.y = 0
    
    # --- Code for moving the paddle down
    def moveDown(self, pixels):
        self.rect.y += pixels

        if self.rect.y > 400:
            self.rect.y = 400

# --- Ball code
class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        # --- Stuff for the ball
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # --- Draw the ball
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4,8),randint(-8,8)]
        self.rect = self.image.get_rect()

    # --- Ball movement
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    # --- Add bounce to the ball
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)


# ----- Placing stuff -----

aw, ah = 10, 100 # --- (Default: 10, 100)
bw, bh = 10, 100 # --- (Default: 10, 100)

# --- Place Paddle A
paddleA = Paddle(RED, aw, ah)
paddleA.rect.x = 20
paddleA.rect.y = 200

# --- Place Paddle B
paddleB = Paddle(BLUE, bw, bh)
paddleB.rect.x = 670
paddleB.rect.y = 200

# --- Place the Ball
ball = Ball(ORANGE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

 # --- --- --- --- ---

# --- A list for sprites
sprites = pygame.sprite.Group()

# --- Add everything to the sprite list
sprites.add(paddleA)
sprites.add(paddleB)
sprites.add(ball)

Running = True

# --- Clock to keep the fps in control xD
clock = pygame.time.Clock()



# ----- Setting values -----

# --- Points
scoreA = 0
scoreB = 0

# --- Default ammount of point(s) given when a player scores
point = 1

# --- Point Hack Ammount (LShift for player A(red), RShift for player b(Blue))
phx = 100

# --- Paddle speed (Default: 5)
spd = 5

# --- Sets the max fps (Default: 60)
fps = 60

# ---------- Game Loop ----------
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # --- Pressing the ESC key closes the game
                print("Gn")
                Running = False
    
    # --- Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(spd)
    if keys[pygame.K_s]:
        paddleA.moveDown(spd)
    if keys[pygame.K_UP]:
        paddleB.moveUp(spd)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(spd)
    if keys[pygame.K_SPACE]:
        scoreA, scoreB = 0, 0

    # --- Score hack buttons
    if keys[pygame.K_LSHIFT]:
        scoreA += phx
    if keys[pygame.K_RSHIFT]:
        scoreB += phx

    # --- Game Logic
    sprites.update()

    # --- Ball colliding with the borders // giving scores
    if ball.rect.x >= 690:
        scoreA += point
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        scoreB += point
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    # --- Ball colliding with the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()


    # --- Drawing stuff
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    sprites.draw(screen)

    # --- Display the scores
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, RED)
    screen.blit(text, (250, 10))
    text2 = font.render(str(scoreB), 1, BLUE)
    screen.blit(text2, (420, 10))

    # --- Updates the screen
    pygame.display.flip()

    # --- Limit the fps to the set value
    clock.tick(fps)

pygame.quit()