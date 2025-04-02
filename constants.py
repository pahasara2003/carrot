
import pygame
import os
import numpy as np


k = -19

gun_transform = [{'angle':-15, 'shift':(18,53+k)},
        {'angle':0, 'shift':(20,48+k)},
        {'angle':43, 'shift':(20,18+k)},
        {'angle':45, 'shift':(10,13+k)}]

bullet_transform= [[[70,67+k],[70,45+k],[63,10+k],[54,0+k]],[[17+k,60+k],[17+k,45+k],[22+k,12+k],[6+k,-5+k]]]

guns_rate = [1,2,3,4,4,5,6,7,8,9,10,11]
guns_speed = [7,30,50,10,11,20,10,20,20,10]

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")



toggle = lambda n,max: 0 if n > max else n +1
toggleN = lambda n,max: max if n == 0 else n -1

to_int = lambda x: 2*(x*1 - 0.5)

def load_image(name, colorkey=None, scale=2):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    # image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

bgImage,bgImageRect = load_image("2 Background/Day/Background.png",scale=2.8)

char,hand,gun,bullet = "1 Characters","3 Hands","2 Guns","5 Bullets"
guns = [load_image(f"{gun}/{i}_1.png")[0] for i in range(1,11)]
bullets = [load_image(f"{bullet}/{i}.png")[0] for i in range(1,11)]


running = True
dt = 0
w,h = 64*25,64*12
w2,h2 = 500,400  #panel size
username = ""



def grid(screen):
    L = 64
    for i in range(int(h/L)+1):
        pygame.draw.line(screen,'RED',(0,L*i),(w,L*i),1)
    for i in range(int(w/L)+1):
        pygame.draw.line(screen,'RED',(L*i,0),(L*i,h),1)

world = np.zeros((25,12))
world[0,7] = 33
world[1,9] = 39
world[0,8] = 4
world[0,9] = 40

world[1,7] = 2
world[1,8] = 14
world[2,7] = 2

world[2,8] = 37
world[2,9] = 40
world[3,8] = 37
world[3,9] = 4


world[3,7] = 2
world[4,7] = 3
world[4,8] = 41
world[4,9] = 35


world[5,5] = 49
world[6,5] = 50
world[7,5] = 51

world[9,4] = 18



world[5,9] = 10
world[6,9] = 10
world[7,9] = 10
world[8,9] = 36
world[8,8] = 9
world[9,7] = 48
world[9,8] = 40
world[10,8] = 10
world[11,8] = 33
world[12,8] = 34
world[13,8] = 12
world[13,9] = 62
world[13,10] = 35
world[14,10] = 33
world[15,10] = 2
world[16,10] = 2
world[17,10] = 2
world[18,10] = 2
world[19,10] = 3


world[12,11] = 20
world[13,11] = 4
world[14,11] = 40

for i in range(9,13):
    world[i,9] = np.random.choice([4,39,40,19,20])


for i in range(0,14):
    world[i,11] = np.random.choice([4,38,39,40,19,20])
    world[i,10] = np.random.choice([4,38,39,40,19,20])



world[15,11] = 14

world[16,11] = 15
world[17,11] = 15
world[18,11] = 15
world[19,11] = 15
world[19,11] = 15
world[20,11] = 11
world[21,11] = 11
world[22,11] = 11
world[23,11] = 11
world[24,11] = 11


