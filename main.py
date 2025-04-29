import pygame
import random
import math
import sys

# inisialisasi
pygame.init()
# mengubah title
pygame.display.set_caption("My first pygame")

# mengatur lebar dan tinggi
width = 600
height = 400

screen = pygame.display.set_mode([width, height])

x_point = 0
y_point = 0


class Player():
    def __init__(self):
        self.x = 50
        self.y = 150
        self.live = 3
        self.point = 0

    def move(self, x, y):
        self.x += x
        self.y += y
        self.draw()

    def draw(self):
        img = pygame.image.load('img/jet.png')
        screen.blit(img, (self.x, self.y))

player = Player()

class Enemy:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = random.randint(0, 400)
        self.icon = 'img/missile.png'
        self.speed = 2

    def move(self):
        if self.x < -10:
            self.x = random.randint(610, 1000)
            self.y = random.randint(0, 400)
            self.icon = 'img/missile.png'
            self.speed = 2
        else:
            self.x -= self.speed
            self.collison()

    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def collison(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 30 and self.icon == 'img/missile.png':
            player.live -= 1
            self.icon = 'img/blast.png'
            self.speed = .5
        else:
            pass


class Cloud:
    def __init__(self):
        self.x = random.randint(610, 1000)
        self.y = random.randint(100, 300)

    def move(self):
        if self.x < -100:
            self.x = random.randint(610, 1000)
            self.y = random.randint(100, 300)
        else:
            self.x -= .5

    def draw(self):
        img = pygame.image.load('img/cloud-computing.png')
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
            self.collison()

    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def collison(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 50 and self.icon == 'img/coin.png':
            player.point += 1
            self.icon = 'img/magic.png'
        else:
            pass


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
            self.collison()

    def draw(self):
        img = pygame.image.load(self.icon)
        screen.blit(img, (self.x, self.y))

    def collison(self):
        distance = math.sqrt(
            ((player.x - self.x) ** 2 + (player.y - self.y) ** 2))
        if distance <= 50 and self.icon == 'img/heart.png':
            player.live += 1
            self.icon = 'img/add.png'
        else:
            pass


class Text:
    def __init__(self, x, y, text, width, height):
        self.x = x
        self.y = y
        self.text = text

    def draw(self):
        font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 24)
        text = font.render(self.text, True, (54, 69, 79))
        screen.blit(text, (self.x, self.y))


# membuat fungsi plane untuk mengubah posisi pesawat
enemies = []
clouds = []
points = []
hearts = []
texts = []
levels = ['Easy', 'Medium', 'Hard', 'Anomali']

y_text = 100
y_cursor = 102

for level in levels:
    texts.append(Text(220, y_text, level, 200, 30))
    y_text += 40


def generate(count: int, attr: list, obj: object) -> None:
    while count > 0:
        attr.append(obj())
        count -= 1


def move(attr: list) -> None:
    for att in attr:
        att.draw()
        att.move()

def sun(x, y):
    img = pygame.image.load('img/sun.png')
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


def play():
    sun(500, 20)
    move(clouds)
    player.move(x_point, y_point)
    move(points)
    move(hearts)
    move(enemies)
    text_heart_score(str(player.live), 'img/heart.png', 30, 60, 20)
    text_heart_score(str(player.point), 'img/coin.png', 100, 130, 20)


def dashboard():
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 36)
    label = font.render("Choose Level", True, (255, 255, 255))
    screen.blit(label, (220, 50))
    for text in texts:
        text.draw()
    cursor(200, y_cursor)

def reset(enemy_count):
    global player
    global enemies
    global clouds
    global points
    global hearts

    player = Player()
    enemies = []
    clouds = []
    points = []
    hearts = []
    generate(enemy_count, enemies, Enemy)
    generate(10, clouds, Cloud)
    generate(3, points, Point)
    generate(1, hearts, Heart)

isPlay = False
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT or e.key == ord('a'):
                x_point -= 1
            if e.key == pygame.K_RIGHT or e.key == ord('d'):
                x_point += 1
            if e.key == pygame.K_UP and not isPlay:
                if y_cursor > 102:
                    y_cursor -= 40
            if e.key == pygame.K_UP or e.key == ord('w'):
                y_point -= 1
            if e.key == pygame.K_DOWN and not isPlay:
                if y_cursor < 222:
                    y_cursor += 40
            if e.key == pygame.K_DOWN or e.key == ord('s'):
                y_point += 1
            if e.key == pygame.K_RETURN and not isPlay:
                match(y_cursor):
                    case 102:
                        enemy_count = 5
                    case 142:
                        enemy_count = 10
                    case 182:
                        enemy_count = 20
                    case 222:
                        enemy_count = 50
                isPlay = True
                reset(enemy_count)
            if e.key == ord('q') and player.live < 1 and isPlay:
                isPlay = False
                reset(enemy_count)
            if e.key == ord('r') and player.live < 1 and isPlay:
                reset(enemy_count)
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == ord('a'):
                x_point = 0
            if e.key == pygame.K_RIGHT or e.key == ord('d'):
                x_point = 0
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
    screen.fill([135, 206, 235])

    if not isPlay:
        dashboard()
    elif isPlay and player.live > 0:
        play()
    elif isPlay and player.live < 1:
        gameOver()
    pygame.display.flip()

pygame.quit()
sys.exit()
