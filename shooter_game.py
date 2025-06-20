#Створи власний Шутер!
import random
import pygame 
pygame.mixer.init()
pygame.font.init()

WIDHT = 1200
HEIGHT = 600
SIZE = (WIDHT, HEIGHT)
FPS = 60

window = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), SIZE)

small_font = pygame.font.SysFont("calibri", 20)
medium_font = pygame.font.SysFont("impact", 40)
big_font = pygame.font.SysFont("helvetica",60)
fire_sound = pygame.mixer.Sound("fire.ogg")

score = 0 
lost = 0

pygame.mixer.music.load("space.ogg")
#pygame.mixer.music.play()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename: str, coords: tuple[int, int], size: tuple [int, int], speed: int ):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(filename), size
        )
        self.rect  = pygame.Rect(coords, size)

        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

        self.rect = self.image.get_rect(topleft=coords)

        self.speed = speed

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self, ):
        keys = pygame.key.get_pressed()

        x,y = self.rect.x, self.rect.y

        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_d] and self.rect.right < WIDHT:
            self.rect.x += self.speed

    def fire(self):
        fire_sound.play()

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDHT-self.rect.width)
            global lost
            lost += 1



player = Player("rocket.png", (WIDHT//2-32, HEIGHT-95), (65,95), 15)

ufo_group = pygame.sprite.Group()
ufo_num = 5
for i in range(5):
    ufo = Enemy("ufo.png", (random.randint(0,WIDHT - 60), -20), (60,30), random.randint(3,8))
    ufo_group.add(ufo)



run = True
finish = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    if not finish:
        window.blit(background, (0,0))
        player.draw(window)
        player.update()

        ufo_group.draw(window)
        ufo_group.update()

        score_text = medium_font.render("Збито: " + str(score), True, (255,255,255) )
        lost_text = medium_font.render("Пропущено: "+ str(lost), True, (255,255,255) )
        window.blit(score_text, (10,10))
        window.blit(lost_text, (10,60))

    pygame.display.update()
    clock.tick(FPS)

