from pygame import*

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
door_open = mixer.Sound('open.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    direction2 = 'up'
    def update1(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    def update2(self):
        if self.rect.y <= 1:
            self.direction2 = "down"
        if self.rect.y >= win_height -85:
            self.direction2 = "up"

        if self.direction2 == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

color_1, color_2, color_3 = 218, 165, 32

player = Player('hero.png', 20, 45, 7)
enemy = Enemy('cyborg.png', 520, 175, 5)
enemy2 = Enemy('cyborg.png', 420, 0, 13)
gold = GameSprite('treasure.png', 620, 362, 0)
key1 = GameSprite('key.png', 330, 270, 0)
wall1 = Wall(color_1, color_2, color_3, 100, 90, 10, 150)
wall2 = Wall(color_1, color_2, color_3, 100, 240, 320, 10)
wall3 = Wall(color_1, color_2, color_3, 100, 330, 10, 75)
wall4 = Wall(color_1, color_2, color_3, 210, 330, 10, 300)
wall5 = Wall(color_1, color_2, color_3, 310, 90, 10, 300)
wall6 = Wall(color_1, color_2, color_3, 410, 90, 10, 500)
wall7 = Wall(color_1, color_2, color_3, 210, 0, 10, 155)
wall8 = Wall(color_1, color_2, color_3, 505, 160, 100, 10)
wall9 = Wall(color_1, color_2, color_3, 580, 340, 130, 10)
door = Wall(165, 42, 42, 580, 340, 10, 300)

FPS = 60
clock = time.Clock()
game = True
finish = False
open = False
font.init()
font = font.SysFont('Arial', 60)
win = font.render('YOU WIN!', True, (127, 255, 212))
loss = font.render('YOU LOSS!', True, (255, 0, 255))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))

        gold.reset()
        player.reset()
        player.update()
        enemy.reset()
        enemy.update1()
        enemy2.reset()
        enemy2.update2()
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()
        wall8.draw_wall()
        wall9.draw_wall()

        if sprite.collide_rect(player, gold):
            window.blit(win, (228, 228))
            finish = True
            money.play()

        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, enemy2) or sprite.collide_rect(player, wall1):
            window.blit(loss, (217, 226))
            finish = True
            kick.play()
        if sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall4):
            window.blit(loss, (217, 226))
            finish = True
            kick.play()
        if sprite.collide_rect(player, wall5) or sprite.collide_rect(player, wall7) or sprite.collide_rect(player, wall6):
            window.blit(loss, (217, 226))
            finish = True
            kick.play()
        if sprite.collide_rect(player, wall8) or sprite.collide_rect(player, wall9):
            window.blit(loss, (217, 226))
            finish = True
            kick.play()
        if sprite.collide_rect(player, key1):
            door_open.play(1)
            open = True
        if not open:
            key1.reset()
            door.draw_wall()
        if sprite.collide_rect(player, door) and not open:
            window.blit(loss, (217, 226))
            finish = True
            kick.play()

    display.update()
    clock.tick(FPS)