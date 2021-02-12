import pygame
import random
import time

# 23.9.2018. made by Fran Maric FM :)


speed = 8  # brzina micanja broda
b_speed = 10  # brzina metka
a_b_speed = 10  # brzina svemirskog metka
alien_bullet_amount = 80  # veci broj manja sansa za metak


def colorize(image, newColor):  # function from internet because I don't know this shit :)
    image = image.copy()
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return image


def scoreboard():  # funkcija za prikazivanje igracevih statusa
    for i in range(2, lifes-1, -1):
        gameDisplay.blit(colorize(shipImg, (255, 0, 0)),
                         (int(display_width-(i+1)*60-20), 15))
    for i in range(lifes-1, -1, -1):
        gameDisplay.blit(shipImg, (int(display_width-(i+1)*60-20), 15))
    pygame.draw.line(gameDisplay, (255, 0, 0), (0, 50), (display_width, 50), 3)
    message('Score: '+str(score), 80+len(str(score))*15, 28, (123, 0, 0))


def message(text, x, y, color):  # funkcija za prikazivanje teksta na ekranu
    largeText = pygame.font.Font('freesansbold.ttf', 30)
    textSurface = largeText.render(text, True, color)
    TextSurf, TextRect = textSurface, textSurface.get_rect()
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)


class Ship:  # klasa svemirski brod
    def __init__(self):
        self.x = display_width/2
        self.y = display_height-30

    def move(self, s):
        self.x += s*speed

    def show(self):
        gameDisplay.blit(shipImg, (int(self.x), int(self.y)))


class Bullet:  # klasa metak
    def __init__(self, x):
        self.x = x+25
        self.y = display_height-60
        self.toDelete = False

    def move(self):
        self.y -= b_speed
        if self.y < -20:
            self.toDelete = True

    def show(self):
        gameDisplay.blit(bulletImg, (int(self.x), int(self.y)))

    def checkHit(self, al):
        global score, alien_bullet_amount
        if self.y < al.y+32:
            if al.x < self.x < al.x+44 or al.x < self.x+5 < al.x+44:
                self.toDelete = True
                al.toDelete = True
                score += 15
                alien_bullet_amount -= 0.2


class Alien_Bullet:  # klasa alien metak
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.toDelete = False

    def move(self):
        self.y += a_b_speed
        if self.y > display_height:
            self.toDelete = True

    def show(self):
        gameDisplay.blit(bulletImg, (int(self.x), int(self.y)))

    def checkHit(self):
        if self.y > display_height-32 and (ship.x < self.x < ship.x+56 or ship.x < self.x+5 < ship.x+56):
            return True
        else:
            return False


class Alien:  # klasa svemirko
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.toDelete = False
        color = random.choice(colors)
        self.n = random.choice([1, 2, 4, 6])
        if n != 1:
            self.img = colorize(pygame.image.load(
                'Sprites//aliens//alien'+str(self.n)+'.png'), color)
            self.img1 = colorize(pygame.image.load(
                'Sprites//aliens//alien'+str(self.n+1)+'.png'), color)
        else:
            self.img = colorize(pygame.image.load(
                'Sprites//aliens//alien1.png'), color)
            self.img1 = self.img

    def move(self, x, y):
        self.x += x
        self.y += y

    def show(self, i):
        if i == 1:
            gameDisplay.blit(self.img, (int(self.x), int(self.y)))
        else:
            gameDisplay.blit(self.img1, (int(self.x), int(self.y)))


score = 0  # varijabla za pohranu rezultata

pygame.init()
display_width = 800
display_height = 650

background = (240, 240, 255)
backgroundExplosion = (90, 20, 0)
colors = [(249, 200, 14), (248, 102, 36), (234, 53, 70),
          (102, 46, 155), (67, 188, 205)]

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space invaders FM')
clock = pygame.time.Clock()
shipImg = pygame.image.load('sprites//shipImg.png')
bulletImg = pygame.image.load('sprites//bulletImg.png')
exploImg = colorize(pygame.image.load('Sprites//explosion.png'), (255, 0, 0))
game_over = pygame.image.load('sprites//game_over.png')
out = False

ship = Ship()

while not out:
    game = True
    lifes = 3
    boom = 0
    al_x, al_y = 1, 0
    n = 0
    k = 0
    xdir = 0
    alien_bullet_amount = 80
    bullets = []
    aliens = []
    explosions = []
    alien_bullets = []
    for i in range(10):
        for j in range(3):
            aliens.append(Alien(i*70+55, j*50+60))
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                out = True
                game = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    xdir = -1
                if event.key == pygame.K_RIGHT:
                    xdir = 1
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 2:
                        bullets.append(Bullet(ship.x))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and xdir == -1:
                    xdir = 0
                if event.key == pygame.K_RIGHT and xdir == 1:
                    xdir = 0
        gameDisplay.fill(background)  # pozadina
        if n > 15:
            n = 0
            if k == 1:
                k = 0
            else:
                k = 1
            boom = 0
            explosions = []
        else:
            if boom == 1:
                gameDisplay.fill(backgroundExplosion)
            for i in explosions:
                gameDisplay.blit(exploImg, (i[0], i[1]))
        ship.move(xdir)
        if ship.x < 0:
            ship.x = 0
        elif ship.x > display_width-55:
            ship.x = display_width-55
        ship.show()
        for i in range(len(bullets)-1, 0, -1):
            bullets[i].move()
            bullets[i].show()
            for j in aliens:
                bullets[i].checkHit(j)
            if bullets[i].toDelete:
                bullets = bullets[:-1]

        for i in aliens:
            if i.x+50 > display_width and al_x == 1:
                al_x = 0
                al_y = 1
            if i.y+32 > 250 and al_y == 1:
                al_x = -1
                al_y = 0
            if i.x < 6 and al_x == -1:
                al_x = 0
                al_y = -1
            if i.y < 60 and al_y == -1:
                al_x = 1
                al_y = 0

        if random.randint(1, int(alien_bullet_amount)) == 5:
            i = random.randint(0, len(aliens)-1)
            alien_bullets.append(Alien_Bullet(aliens[i].x+22, aliens[i].y+32))

        for i in range(len(aliens)-1, -1, -1):
            aliens[i].move(al_x, al_y)
            if aliens[i].toDelete:
                explosions.append([aliens[i].x, aliens[i].y])
                aliens.pop(i)
            else:
                aliens[i].show(k)
        for i in range(len(alien_bullets)-1, -1, -1):
            alien_bullets[i].move()
            alien_bullets[i].show()
            if alien_bullets[i].checkHit():
                alien_bullets[i].toDelete = True
                if lifes > 1:
                    lifes -= 1
                    boom = 1
                else:
                    lifes = 0
                    boom = 1
                    score = 0
                    gameDisplay.blit(colorize(game_over, (0, 0, 0)),
                                     (int(display_width/2-209), int(display_height/2-159.5)))
                    pygame.display.update()
                    time.sleep(2)
                    while game:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                game = False
            if alien_bullets[i].toDelete:
                alien_bullets.pop(i)
        scoreboard()
        pygame.display.update()
        clock.tick(60)  # FPS
        if len(aliens) == 0:
            for i in range(10):
                for j in range(3):
                    aliens.append(Alien(i*70+55, j*50+60))
        n += 1


pygame.quit()
quit()
