from pygame import *
from random import *
class MainSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, x_speed, y_speed, player_x, player_y):
        sprite.Sprite.__init__(self)
        self.image =  transform.scale(image.load(player_image), (80,80))
        self.player_speed = player_speed
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.stands_on = False
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(MainSprite):
    def gravitate(self):
        self.y_speed += 0.25
    def jump(self, y):
        if self.stands_on:
            self.y_speed = y
    def update(self):
        self.rect.x += self.player_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.player_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.player_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.gravitate()
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
                    self.stands_on = p
        if self.y_speed < 0: #^
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
                    self.stands_on = p




class Stena(sprite.Sprite):
    def __init__ (self, player_image, wall_x, wall_y, wall_widht, wall_height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (wall_widht,wall_height))
        self.wall_widht = wall_widht
        self.wall_height = wall_height
        #self.image = Surface([self.wall_widht, self.wall_height])
        #self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        #self.rect = Rect(wall_x, wall_y, wall_widht, wall_height)

    def draw_wall(self):
        #draw.rect(window,(self.player_image, self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.wall_widht, self.wall_height))
        window.blit(self.image, (self.rect.x, self.rect.y))

barriers = sprite.Group()




class Vrag(MainSprite):
    def update(self):
        self.rect.x += randint(-2,2)
        self.rect.y += randint(-2,2)
monsters = sprite.Group()
monsters2 = sprite.Group()
x = 450
y = 300
monster = Vrag("kol.png", 5, 0, 0, x, y)
monster2 = Vrag("kol.png", 5, 0, 0, x, y)
monsters.add(monster)
monsters2.add(monster2)

all_sprites = sprite.Group()
all_sprites.add(monsters)
all_sprites.add(monsters2)


class WINS(MainSprite):
    pass
winner = sprite.Group()
x = 650
y = 250
win = WINS("cat.png", 0, 0, 0, x, y)
winner.add(win)
all_sprites.add(winner)

shift = 0
speed = 0

win_width = 800
win_height = 600
player_x = 50
player_y = 500
left_bound = win_width / 40
right_bound = win_width - 8 * left_bound
window = display.set_mode((win_width,win_height))
display.set_caption("Аркада")
fon = transform.scale(image.load("fantasyforest_2.png"), (win_width, win_height))
w1 = Stena("plato.png", 0, 510, 5000, 30)
barriers.add(w1)
all_sprites.add(w1)
w2 = Stena("stone_packed.png", 200, 300, 150, 50)
barriers.add(w2)
all_sprites.add(w2)
w3 = Stena("plato.png", 450, 300, 150, 50)
barriers.add(w3)
all_sprites.add(w3)
w4 = Stena("plato.png", 650, 300, 150, 50)
barriers.add(w4)
all_sprites.add(w4)
p = Player("cat.png", 0,0, 0, 45, 450)
all_sprites.add(p)
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_LEFT :
                p.player_speed = -4
            elif e.key == K_RIGHT:
                p.player_speed = 4
            elif e.key == K_UP:
                p.jump(-7)
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                p.player_speed = 0
            elif e.key == K_RIGHT:
                p.player_speed = 0
    #shift += speed
    if p.rect.x > right_bound and p.player_speed > 0 or p.rect.x < left_bound and p.player_speed < 0:
        shift -= p.player_speed 
        for s in all_sprites:
            s.rect.x -= p.player_speed 
    local_shift = shift % win_width
    window.blit(fon, (local_shift, 0))
    if local_shift != 0:
        window.blit(fon, (local_shift - win_width, 0))


    p.gravitate()
    p.update()
    p.reset()
    monsters.update()
    monsters.draw(window)
    monsters2.update()
    monsters2.draw(window)
    winner.update()
    winner.draw(window)
    barriers.update()
    barriers.draw(window)
    if sprite.collide_rect(p, monster) or sprite.collide_rect(p, monster2):
        a =transform.scale(image.load("fail_1.jpg"), (800,600))
        window.blit(a, (0,0))
    if sprite.collide_rect(p, win):
        b = transform.scale(image.load("winner_1.jpg"), (800,600))
        window.blit(b, (0,0))
    display.update()





