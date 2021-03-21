import pygame
import random

SCREENRECT = pygame.Rect(0, 0, 800, 600)
ALIEN_RELOAD = 10
ALIEN_ODDS = 22  # chances a new alien appears
ALIEN_SPEED = 5
SCORE = 0


class Player(pygame.sprite.Sprite):
    speed = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)  # call Sprite initializer
        self.image = pygame.image.load('data/space.png')
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.facing = -1

    def move(self, direction):

        if direction:
            self.rect.move_ip(direction * self.speed, 0)
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > 800:
                self.rect.right = 800


class Alien(pygame.sprite.Sprite):
    """ An alien space ship. That slowly moves down the screen.
    """

    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load('data/enemy.png')
        self.rect = self.image.get_rect(topleft=SCREENRECT.topleft)
        self.facing = random.choice((-1, 1)) * speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.frame = self.frame + 1


class Shot(pygame.sprite.Sprite):
    """ a bullet the Player sprite fires.
    """

    speed = -10

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load('data/bullet.png')
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        """ called every time around the game loop.

        Every tick we move the shot upwards.
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class Score(pygame.sprite.Sprite):
    """ to keep track of the score.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 33)
        self.color = pygame.Color("white")
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect(topleft=SCREENRECT.topleft)

    def update(self):
        """ We only update the score in update() when it has changed.
        """
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)


pygame.init()

screen = pygame.display.set_mode((SCREENRECT.size))
pygame.display.set_caption('Space Invader')
pygame.mouse.set_visible(0)

players = pygame.sprite.Group()
aliens = pygame.sprite.Group()
shots = pygame.sprite.Group()
all_sprites = pygame.sprite.RenderUpdates()

Player.containers = all_sprites, players
Shot.containers = all_sprites, shots
Alien.containers = all_sprites, aliens
Score.containers = all_sprites

clock = pygame.time.Clock()
game = True

player = Player()

alienreload = ALIEN_RELOAD
for i in range(2):
    alien = Alien(ALIEN_SPEED)

background = pygame.Surface(SCREENRECT.size)

background.fill((255, 255, 255))

bgdtile = pygame.image.load("data/imkv74m4q5g41.png")
background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    background.blit(bgdtile, (x, 0))
screen.blit(background, (0, 0))

pygame.display.flip()

while player.alive():
    if pygame.font:
        all_sprites.add(Score())
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.kill()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            player.kill()

    keystate = pygame.key.get_pressed()
    direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
    firing = keystate[pygame.K_SPACE]

    if firing and len(shots) < 1:
        shot = Shot(player.rect.midbottom)

    player.move(direction)

    # Create new alien
    if alienreload:
        alienreload = alienreload - 1
    elif not int(random.random() * ALIEN_ODDS):
        Alien(ALIEN_SPEED)
        alienreload = ALIEN_RELOAD
        ALIEN_SPEED += 0.1

    for alien in pygame.sprite.spritecollide(player, aliens, 1):
        player.kill()

    for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
        SCORE += 1

    all_sprites.update()
    all_sprites.clear(screen,background)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
