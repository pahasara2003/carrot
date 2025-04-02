import pygame
from pygame.locals import *
from constants import *
from roles import *

pygame.init()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()


font = pygame.font.Font("./data/CyberpunkCraftpixPixel.otf", 20)

world = World()
cyborg = Person(font)
allsprites = pygame.sprite.Group(cyborg)

bats = pygame.sprite.Group()
objectsBehind = pygame.sprite.Group(Object('Bushes',19,300,8),Object('Bushes',14,435,8))
objectsAfter = pygame.sprite.Group()
bulletList = pygame.sprite.Group()


objectsBehind.add(Object('Fountain',1,1000,9,True))
objectsBehind.add(Object('Other',1,700,7))

for i in range(1,15):
    objectsBehind.add(Object('Grass',i,650+15*i,7))
objectsBehind.add(Object('Other',2,1230,10))
objectsBehind.add(Object('Benches',1,30,6))
objectsAfter.add(Object('Other',3,130,6))
objectsBehind.add(Object('Benches',1,30,6))

inital_bats_count =20
for i in range(inital_bats_count):
    bats.add(Enemy(i))



def gameKeyEvent(event):
    if(event.key == pygame.K_UP):
        cyborg.hand_index = toggle(cyborg.hand_index,3)
    if(event.key == pygame.K_RSHIFT and np.abs(cyborg.velocity) < 1):
        cyborg.velocity = -12
    if(event.key == pygame.K_DOWN):
        cyborg.hand_index = toggleN(cyborg.hand_index,3)
    if(event.key == pygame.K_RCTRL):
        cyborg.gun_index = toggle(cyborg.gun_index,4)
    if(event.key == pygame.K_LEFT):
        cyborg.direction = True
        # cyborg.rect.x += 35
    if(event.key == pygame.K_RIGHT):
        cyborg.direction = False

def updateWorld(screen,game):
    keys = pygame.key.get_pressed()

    screen.blit(bgImage,(0,-200))
   
    if game :

        objectsBehind.update()
        objectsBehind.draw(screen)

        bulletList.update(bats,world)
        bats.update(screen,world,cyborg)
        objectsAfter.update()
        bats.draw(screen)

        allsprites.update(keys,bulletList,world,screen)
        allsprites.draw(screen)
        bulletList.draw(screen)

    objectsAfter.draw(screen)
    world.update(screen)
