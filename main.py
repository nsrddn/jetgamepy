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
color_white = (255, 255, 255)
color_gold = (255, 215, 0)

enemies = []
clouds = []
points = []
hearts = []
airdrops = []
bosses = []
textsLevel = []
levels = ['Easy', 'Medium', 'Hard', 'Anomali']
textPlace = []
places = ['Earth', 'Space']

y_text = 100
y_cursor_level = 102
y_cursor_place = 102

shot_sound = pygame.mixer.Sound('sounds/mixkit-game-gun-shot-1662.mp3')
explode_sound = pygame.mixer.Sound('sounds/explosion-312361.mp3')
healing_sound = pygame.mixer.Sound('sounds/084373_heal-36672.mp3')
reload_sound = pygame.mixer.Sound('sounds/reload-123781.mp3')
coin_sound = pygame.mixer.Sound('sounds/mixkit-arcade-game-jump-coin-216.wav')
speed_sound = pygame.mixer.Sound(
    'sounds/jet-engine-start-up-and-acceleration-sound-effect-328919.mp3')
bg_music = pygame.mixer_music.load(
    'sounds/epic-game-music-by-kris-klavenes-3-mins-49771.mp3')
boss_explode = pygame.mixer.Sound(
    'sounds/mixkit-explosive-impact-from-afar-2758.mp3')


class Player():
    def __init__(self):
        self.x = 50
        self.y = 150
        self.live = 3
        self.point = 0
        self.missile = 10
        self.fire = []
        self.speed = False
        self.time = 0

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
            if player.time >= 100:
                enemies.remove(self)
            else:
                self.x = random.randint(610, 1000)
                self.y = random.randint(0, 400)
                self.icon = 'img/spaceship.png' if place == 'earth' else 'img/ufo.png'
                self.speed = 2
        else:
            self.x -= self.speed
            self.collision()
            if player.time == 60:
                self.speed *= 2

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
            pygame.mixer.Sound.play(explode_sound)


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
            pygame.mixer.Sound.play(coin_sound)


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
        if distance <= 50 and self.icon == 'img/heart.png' and player.live < 7:
            player.live += 1
            self.icon = 'img/add.png'
            pygame.mixer.Sound.play(healing_sound)


class Text:
    def __init__(self, x, y, text, size, color):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', self.size)
        self.text_render = self.font.render(self.text, True, self.color)

    def draw(self):
        screen.blit(self.text_render, (self.x, self.y))

    def getText(self):
        return self.text_render


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
            player.missile += 3
            self.icon = 'img/open-box.png'
            pygame.mixer.Sound.play(reload_sound)


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
                pygame.mixer.Sound.play(explode_sound)


class Boss:
    def __init__(self):
        self.icon = 'img/boss-spaceship.png'
        self.x = random.randint(610, 1000)
        self.y = 150
        self.impact_time = []
        self.fires = []
        self.missile_speed = .8
        self.live = 100
        self.explosions_begin = 0
        self.explosions = []
        for i in range(9):
            self.explosions.append(
                f'img/explosions/explosion_{i}.png')

    def move(self):
        if self.x > 500:
            self.x -= 1
        else:
            self.addMissile()
            self.collision()
            if self.live > 0:
                self.fire()
                self.liveBar()
            self.fireCollision()
            for impact in self.impact_time:
                impact['current_time'] = pygame.time.get_ticks()

    def liveBar(self):
        pygame.draw.rect(screen, (128, 128, 128),
                         (self.x - 18, self.y + 70, 100, 5))
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.x - 18, self.y + 70, self.live, 5))

    def addMissile(self):
        if len(self.fires) < 1:
            x_missile = self.x + 100
            for _ in range(3):
                self.fires.append({'missile_distance': 0, 'dx': 0, 'dy': 0, 'x': x_missile,
                                  'y': self.y, 'icon': 'img/spaceship.png', 'collision': False})
                x_missile += 100

    def fire(self):
        for missile in self.fires:
            dx = player.x - missile['x']
            dy = player.y - missile['y']
            missile['missile_distance'] = math.hypot(dx, dy)

            missile['dx'] = dx / missile['missile_distance']
            missile['dy'] = dy / missile['missile_distance']

            if missile['collision']:
                missile['x'] -= .5
                missile['y'] += 0
                if missile['x'] < 0:
                    self.fires.remove(missile)
            else:
                missile['x'] += missile['dx'] * self.missile_speed
                missile['y'] += missile['dy'] * self.missile_speed

            img = pygame.image.load(missile['icon'])
            screen.blit(img, (missile['x'], missile['y']))

    def fireCollision(self):
        for missile in self.fires:
            if missile['missile_distance'] <= 30 and missile['icon'] == 'img/spaceship.png':
                pygame.mixer.Sound.play(explode_sound)
                missile['icon'] = 'img/explode.png'
                missile['collision'] = True
                player.live -= 1

        for missile, player_missile in zip(self.fires, player.fire):
            collision = math.sqrt(
                ((missile['x'] - player_missile.x) ** 2 + (missile['y'] - player_missile.y) ** 2)) <= 20
            if collision and missile['icon'] == 'img/spaceship.png' and player_missile.icon == 'img/missile-right.png':
                pygame.mixer.Sound.play(explode_sound)
                missile['icon'] = 'img/explode.png'
                player_missile.icon = 'img/blast.png'
                player_missile.speed = .5
                player_missile.reverse = True
                missile['collision'] = True

    def draw(self):
        if self.live <= 0:
            if self.explosions_begin >= len(self.explosions):
                self.explosions_begin = 0
            self.icon = self.explosions[math.floor(self.explosions_begin)]
            objectImage(self.x - 30, self.y - 50, self.icon)
            self.explosions_begin += .05
        else:
            img = pygame.image.load(self.icon)
            screen.blit(img, (self.x, self.y))

    def collision(self):
        for missile in player.fire:
            distance = math.sqrt(
                ((self.x - missile.x) ** 2 + (self.y - missile.y) ** 2))
            if distance <= 30 and missile.icon == 'img/missile-right.png':
                self.live -= 10
                missile.speed = 0
                missile.x = self.x + 5
                missile.icon = 'img/explode.png'
                pygame.mixer.Sound.play(explode_sound)
                self.impact_time.append(
                    {'start_time': pygame.time.get_ticks(), 'current_time': 0, 'missile': missile})
                if self.live <= 0:
                    pygame.mixer.Sound.play(boss_explode)
        self.updateImpact()

    def updateImpact(self):
        for impact in self.impact_time:
            if impact['current_time'] - impact['start_time'] >= 1000:
                player.fire.remove(impact['missile'])
                self.impact_time.remove(impact)


def generate_text(y_text, datas, Obj, texts):
    for data in datas:
        texts.append(Obj(180, y_text, data, 24, color_white))
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


def gameOver():
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 36)
    over_label = font.render(
        "Game Over!, Press R -> Restart, Q -> Quit", True, (255, 255, 255))
    rect = over_label.get_rect(center=(width/2, height/2))
    screen.blit(over_label, rect)


def choose(labelText, texts, y_cursor):
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 36)
    label = font.render(labelText, True, (255, 255, 255))
    screen.blit(label, (180, 50))
    for text in texts:
        text.draw()
    cursor(160, y_cursor)


def displaySurvivalTime():
    font = pygame.font.Font('fonts/PixelGame-R9AZe.otf', 24)
    score = font.render(
        f'Survival Time: {player.time:.2f}s', True, (255, 255, 255))
    screen.blit(score, (240, 20))


bosses.append(Boss())


def play():
    global enemies

    objectImage(
        450, 20, 'img/full-moon.png') if place == 'space' else objectImage(500, 20, 'img/sun.png')
    move(clouds)
    if player.time >= 100:
        move(bosses)
    move(player.fire)
    move(airdrops)
    player.speedCheck()
    player.move(x_point, y_point)
    move(points)
    move(hearts)
    move(enemies)
    objectImage(30, 20, 'img/heart.png')
    objectImage(100, 20, 'img/coin.png')
    objectImage(170, 20, 'img/missile-right.png')
    Text(60, 20, 'x' + str(player.live), 24, color_white).draw()
    Text(130, 20, 'x' + str(player.point), 24, color_white).draw()
    Text(200, 20, 'x' + str(player.missile), 24, color_white).draw()
    displaySurvivalTime()
    player.time += .01 if bosses[0].live > 0 else 0
    if bosses[0].live <= 0:
        text = Text(width/2, height/2, "You Win!", 48, color_gold).getText()
        subtext = Text(width/2, height/2,
                       "Enter to Back to Dashboard", 24, color_white).getText()
        rect = text.get_rect(center=(width/2, height/2))
        subtext_rect = subtext.get_rect(center=(width/2, height/2 + 30))
        screen.blit(text, rect)
        screen.blit(subtext, subtext_rect)


generate_text(100, levels, Text, textsLevel)
generate_text(100, places, Text, textPlace)
isPlay = False


def dashboard():
    global isPlay
    pygame.mixer_music.play(-1)
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
    global bosses

    player = Player()
    bosses.clear()
    enemies.clear()
    clouds.clear()
    points.clear()
    hearts.clear()
    airdrops.clear()
    generate(1, airdrops, Airdrop)
    generate(enemy_count, enemies, Enemy)
    generate(10, clouds, FlyingObject)
    generate(3, points, Point)
    generate(1, hearts, Heart)
    bosses.append(Boss())


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == ord('f'):
                if player.missile > 0:
                    player.fire.append(Missile())
                    pygame.mixer.Sound.play(shot_sound)
                    player.missile -= 1
            if e.key == pygame.K_LEFT or e.key == ord('a'):
                x_point -= 1
            if e.key == pygame.K_RIGHT or e.key == ord('d'):
                x_point += 1
                player.speed = True
                pygame.mixer.Sound.play(speed_sound)
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
            if (e.key == ord('q') and player.live < 1 and isPlay) or (e.key == pygame.K_RETURN and bosses[0].live <= 0 and isPlay):
                isPlay = False
                enemy_count = None
                place = None
            if e.key == ord('r') and (player.live < 1 and isPlay or bosses[0].live <= 0 and isPlay):
                reset()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == ord('a'):
                x_point = 0
            if e.key == pygame.K_RIGHT or e.key == ord('d'):
                x_point = 0
                player.speed = False
                pygame.mixer.Sound.stop(speed_sound)
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
    elif isPlay:
        play() if player.live > 0 else gameOver()
    pygame.display.update()

pygame.quit()
sys.exit()
