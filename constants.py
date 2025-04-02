
import pygame
import os
from map import *

k = -19
gun_transform = [{'angle':-15, 'shift':(18,53+k)},
        {'angle':0, 'shift':(20,48+k)},
        {'angle':43, 'shift':(20,18+k)},
        {'angle':45, 'shift':(10,13+k)}]

bullet_transform= [[[70,67+k],[70,45+k],[63,10+k],[54,0+k]],[[17+k,60+k],[17+k,45+k],[22+k,12+k],[6+k,-5+k]]]
guns_rate = [1,2,3,4,4,5]
guns_speed = [7,30,50,10,11,20,10]
bullet_counts = [100,200,300,400,500,600,700]

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")



toggle = lambda n,max: 0 if n > max else n +1
toggleN = lambda n,max: max if n == 0 else n -1

to_int = lambda x: 2*(x*1 - 0.5)

def load_image(name, colorkey=None, scale=2,strech=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale*strech)
    image = pygame.transform.scale(image, size)

    # image = image.convert()
    # if colorkey is not None:
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

bgImage,bgImageRect = load_image("2 Background/Day/Background.png",scale=2.8)
char,hand,gun,bullet = "1 Characters","3 Hands","2 Guns","5 Bullets"
guns = [load_image(f"{gun}/{i}_1.png")[0] for i in range(1,7)]
bullets = [load_image(f"{bullet}/{i}.png")[0] for i in range(1,6)]


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




