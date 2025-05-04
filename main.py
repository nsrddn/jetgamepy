import pygame
import random
import math
import sys

# inisialisasi
pygame.init()
# mengubah title
pygame.display.set_caption("Jet & Something")

# mengatur lebar dan tinggi
width = 600
height = 400

screen = pygame.display.set_mode([width, height])

x_point = 0
y_point = 0

place = None
enemy_count = None

fill_dark_space = (25, 39, 52)
fill_sky_blue = (135, 206, 235)

enemies = []
clouds = []
points = []
hearts = []
airdrops = []
textsLevel = []
levels = ['Easy', 'Medium', 'Hard', 'Anomali']
textPlace = []
places = ['Earth', 'Space']

y_text = 100
y_cursor_level = 102
y_cursor_place = 102


class Player():
    def __init__(self):
        self.x = 50
        self.y = 150
        self.live = 3
        self.point = 0
        self.missile = 0
        self.fire = []
        self.speed = False

    def move(self, x, y):
        self.x += x
        self.y += y
        self.draw()

    def draw(self):
        img = pygame.image.load('img/jet.png')
        screen.blit(img, (self.x, self.y))

    def speedCheck(self):
        if self.speed:
            img = pygame.image.load('img/speed.png')
            screen.blit(img, (self.x - 18, self.y + 5))


player = Player()


class Enemy:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = random.randint(0, 400)
        self.icon = 'img/spaceship.png' if place == 'earth' else 'img/ufo.png'
        self.speed = 2

    def move(self):
        if self.x < -10:
            self.x = random.randint(610, 1000)
            self.y = random.randint(0, 400)
            self.icon = 'img/spaceship.png' if place == 'earth' else 'img/ufo.png'
            self.speed = 2
        else:
            self.x -= self.speed
            self.collision()

    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def collision(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 30 and (self.icon == 'img/spaceship.png' or self.icon == 'img/ufo.png'):
            player.live -= 1
            self.icon = 'img/explode.png'
            self.speed = .5

class FlyingObject:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = random.randint(100, 300)
        self.icon = 'img/stone.png' if place == 'space' else 'img/cloud-computing.png'
        self.angle = 0

    def move(self):
        if self.x < -100:
            self.x = random.randint(610, 1000)
            self.y = random.randint(100, 300)
        else:
            self.x -= .5

    def draw(self):
        img = pygame.image.load(self.icon)
        if self.icon != 'img/cloud-computing.png':
            img = pygame.transform.rotate(img, self.angle)
            self.angle = 0 if self.angle >= 360 else self.angle + .1
        screen.blit(img, (self.x, self.y))


class Point:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = random.randint(100, 300)
        self.icon = 'img/coin.png'

    def move(self):
        if self.x < -100:
            self.x = random.randint(610, 1000)
            self.y = random.randint(100, 300)
            self.icon = 'img/coin.png'
        else:
            self.x -= .5
            self.collision()

    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def collision(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 50 and self.icon == 'img/coin.png':
            player.point += 1
            self.icon = 'img/magic.png'


class Heart:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = random.randint(100, 300)
        self.icon = 'img/heart.png'

    def move(self):
        if self.x < -100:
            self.x = random.randint(610, 1000)
            self.y = random.randint(100, 300)
            self.icon = 'img/heart.png'
        else:
            self.x -= .5
            self.collision()

    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def collision(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 50 and self.icon == 'img/heart.png':
            player.live += 1
            self.icon = 'img/add.png'


class Text:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self):
        font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 24)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))

class Airdrop:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = 0
        self.icon = 'img/airdrop.png'
        self.speed_x = .5
        self.speed_y = .2
    
    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def move(self):
        if self.y > 400:
            self.x = random.randint(610, 1000)
            self.y = 0
            self.icon = 'img/airdrop.png'
        else:
            self.x -= self.speed_x
            self.y += self.speed_y
            self.collision()

    def collision(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 30 and self.icon == 'img/airdrop.png':
            player.live += 1
            player.missile += 3
            self.icon = 'img/open-box.png'


class Missile:
    def __init__(self):
        self.icon = 'img/missile-right.png'
        self.x = player.x + 5
        self.y = player.y + 3
        self.speed = 2
        self.reverse = False

    def draw(self):
        img = pygame.image.load(self.icon)
        spark = pygame.image.load('img/speed.png')
        screen.blit(spark, (self.x - 15, self.y))
        screen.blit(img, (self.x, self.y))

    def move(self):
        if self.x > 1000 or self.x <= 0:
            player.fire.remove(self)
        else:
            if self.reverse:
                self.x -= self.speed
            else:
                self.x += self.speed
            self.collision()

    def collision(self):
        for enemy in enemies:
            distance = math.sqrt(
                ((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2))
            if distance <= 15 and self.icon == 'img/missile-right.png' and enemy.icon == ('img/ufo.png' if place == 'space' else 'img/spaceship.png'):
                self.icon = 'img/blast.png'
                self.speed = .5
                self.reverse = True
                enemy.icon = 'img/explode.png'
                enemy.speed = .5

def generate_text(y_text, datas, Obj, texts):
    for data in datas:
        texts.append(Obj(180, y_text, data))
        y_text += 40


def generate(count, attr, obj) -> None:
    while count > 0:
        attr.append(obj())
        count -= 1


def move(attr: list) -> None:
    for att in attr:
        att.draw()
        att.move()


def objectImage(x, y, path):
    img = pygame.image.load(path)
    screen.blit(img, (x, y))


def cursor(x, y):
    img = pygame.image.load('img/right.png')
    screen.blit(img, (x, y))


def text_heart_score(value, path, xImg, xText, y):
    img = pygame.image.load(path)
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 24)
    live_label = font.render(f"x{value}", True, (255, 255, 255))
    screen.blit(img, (xImg, y))
    screen.blit(live_label, (xText, y))


def gameOver():
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 36)
    over_label = font.render(
        "Game Over, Press R -> Restart, Q -> Quit", True, (255, 255, 255))
    rect = over_label.get_rect(center=(width/2, height/2))
    screen.blit(over_label, rect)


def choose(labelText, texts, y_cursor):
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 36)
    label = font.render(labelText, True, (255, 255, 255))
    screen.blit(label, (180, 50))
    for text in texts:
        text.draw()
    cursor(160, y_cursor)


def play():
    objectImage(
        450, 20, 'img/full-moon.png') if place == 'space' else objectImage(500, 20, 'img/sun.png')
    move(clouds)
    move(player.fire)
    move(airdrops)
    player.speedCheck()
    player.move(x_point, y_point)
    move(points)
    move(hearts)
    move(enemies)
    text_heart_score(str(player.live), 'img/heart.png', 30, 60, 20)
    text_heart_score(str(player.point), 'img/coin.png', 100, 130, 20)
    text_heart_score(str(player.missile), 'img/missile-right.png', 170, 200, 20)


generate_text(100, levels, Text, textsLevel)
generate_text(100, places, Text, textPlace)
isPlay = False


def dashboard():
    global isPlay
    if enemy_count is None:
        choose("Choose Your Level", textsLevel, y_cursor_level)
    elif place is None:
        choose("Choose Your Place", textPlace, y_cursor_place)
    elif enemy_count is not None and place is not None:
        isPlay = True


def reset():
    global player
    global enemies
    global clouds
    global points
    global hearts
    global enemy_count
    global airdrops

    player = Player()
    enemies = []
    clouds = []
    points = []
    hearts = []
    airdrops = []
    generate(1, airdrops, Airdrop)
    generate(enemy_count, enemies, Enemy)
    generate(10, clouds, FlyingObject)
    generate(3, points, Point)
    generate(1, hearts, Heart)


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == ord('f'):
                if player.missile > 0:
                    player.fire.append(Missile())
                    player.missile -= 1
            if e.key == pygame.K_LEFT or e.key == ord('a'):
                x_point -= 1
            if e.key == pygame.K_RIGHT or e.key == ord('d'):
                x_point += 1
                player.speed = True
            if e.key == pygame.K_UP and not isPlay:
                if y_cursor_level > 102:
                    y_cursor_level -= 40

                if y_cursor_place > 102:
                    y_cursor_place -= 40
            if e.key == pygame.K_UP or e.key == ord('w'):
                y_point -= 1
            if e.key == pygame.K_DOWN and not isPlay:
                if y_cursor_level < 222:
                    y_cursor_level += 40

                if y_cursor_place < 142:
                    y_cursor_place += 40
            if e.key == pygame.K_DOWN or e.key == ord('s'):
                y_point += 1
            if e.key == pygame.K_RETURN and not isPlay:
                if enemy_count is not None:
                    match(y_cursor_place):
                        case 102:
                            place = 'earth'
                        case 142:
                            place = 'space'

                if enemy_count is None:
                    match(y_cursor_level):
                        case 102:
                            enemy_count = 5
                        case 142:
                            enemy_count = 10
                        case 182:
                            enemy_count = 20
                        case 222:
                            enemy_count = 50
                reset()
            if e.key == ord('q') and player.live < 1 and isPlay:
                isPlay = False
                enemy_count = None
                place = None
            if e.key == ord('r') and player.live < 1 and isPlay:
                reset()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == ord('a'):
                x_point = 0
            if e.key == pygame.K_RIGHT or e.key == ord('d'):
                x_point = 0
                player.speed = False
            if e.key == pygame.K_UP or e.key == ord('w'):
                y_point = 0
            if e.key == pygame.K_DOWN or e.key == ord('s'):
                y_point = 0

        if player.x <= 10:
            player.x = 10
        elif player.x >= 525:
            player.x = 525
        elif player.y <= 5:
            player.y = 5
        elif player.y >= 350:
            player.y = 350
# mengubah background
    screen.fill(fill_dark_space if place == 'space' else fill_sky_blue)

    if not isPlay:
        dashboard()
    elif isPlay and player.live > 0:
        play()
    elif isPlay and player.live < 1:
        gameOver()
    pygame.display.update()

pygame.quit()
sys.exit()
