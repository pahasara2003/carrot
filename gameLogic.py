import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine, UIPanel
from pygame_gui import UI_FORM_SUBMITTED
import numpy as np
from pygame.locals import *
from constants import *




class World(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.tiles = []
        for i,row in enumerate(world):
            for j,tile in enumerate(row):
                if tile > 0:
                    index = f"0{int(tile)}" if tile < 10 else int(tile)
                    image,rect = load_image(f"1 Tiles/Tile_{index}.png",scale=2)
                    rect.move_ip(i*64,j*64)
                    self.tiles.append((image,rect))

    def update(self):
        for tile in self.tiles:
            screen.blit(tile[0],tile[1])

class Object(pygame.sprite.Sprite):
    def __init__(self,name,index,x,n,animated=False):
        pygame.sprite.Sprite.__init__(self)
        self.animated = animated

        if(animated):
            self.img,self.rect = load_image(f"3 Objects/{name}.png")
            self.L = 144
            self.n = 0
        else:
             self.image,self.rect = load_image(f"3 Objects/{name}/{index}.png")
       
        y = self.rect.bottom -64
        self.rect.move_ip(x,64*n - y)

    def update(self):
        if(self.animated):
            if(self.n < int(self.img.width/self.img.height -1)):
                self.image = self.img.subsurface(int(np.floor(self.n))*self.L,0,self.L,self.L)
                self.n = self.n + 0.12
            else:
                self.n = 0
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self,index,rect,hand_index,direction):
        pygame.sprite.Sprite.__init__(self)
        self.index = index
        self.direction = -2*(direction-0.5)
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(f"{bullet}/{index}_2.png")
        self.angle = gun_transform[hand_index]["angle"]
        self.image = pygame.transform.rotate(self.image,self.angle+45)
        self.image = pygame.transform.flip(self.image,direction,False)
        self.rect = self.image.get_rect()
        
        # Adjust the position of the rect
        self.rect.move_ip(rect.x + bullet_transform[int(  direction)][hand_index][0],rect.y + bullet_transform[int( direction)][hand_index][1])
        
        self.angle = np.deg2rad(-self.angle)

    def update(self,key):
        v = guns_speed[self.index]*np.array([self.direction*np.cos(self.angle),np.sin(self.angle)])
        self.rect = self.rect.move(tuple(v))

        for tile in world.tiles:
            if tile[1].colliderect(self.rect.centerx,self.rect.centery, 10,10):  
                 self.kill()
        for enemy in bats:
            if enemy.boundary.colliderect(self.rect.centerx,self.rect.centery, 10,10): 
                 if(enemy.life-1 >= 0):
                    enemy.hurt = True 
                    enemy.n = 0.001
                    enemy.life -= 1
                 self.kill()
        if(self.rect.centerx > 1600 or self.rect.centerx < 0):
                 self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,seed):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Bat"
        self.runImage,_ = load_image(f"{self.name}/{self.name}-Run.png")
        self.idleImage,_ = load_image(f"{self.name}/{self.name}-IdleFly.png")
        self.dieImage,_ = load_image(f"{self.name}/{self.name}-Die.png")
        self.attackImage,_ = load_image(f"{self.name}/{self.name}-Attack1.png")
        self.hurtImage,_ = load_image(f"{self.name}/{self.name}-Hurt.png")

        self.L = 128
      
        self.rect = pygame.Rect(0,0,self.L,self.L)
        self.rect = self.rect.move(np.random.randint(300,1200),np.random.randint(10,140))
        self.velocity = [0,0]

        self.direction = False
        self.image = self.runImage.subsurface(0,0,self.L,self.L)
        self.n = 0
        self.boundary = pygame.Rect(0,0,35,35)
        self.hurt = False
        self.life = 10
        self.phase = seed

        self.t  = 0


  
    def run_idle(self,img,rate = 1):
        if(self.n < int(img.width/img.height -1)):
            self.image = img.subsurface(int(np.floor(self.n))*self.L,0,self.L,self.L)
            self.n = self.n + 0.12*rate
        else:
            self.n = 0


    def update(self):
        self.t += 0.1
        self.velocity[1] = np.random.uniform(3,5)*np.sin(self.t + self.phase)
        self.velocity[0] = np.random.uniform(3,5)*np.cos(self.t/5 + self.phase)

        self.rect = self.rect.move(self.velocity[0],self.velocity[1])
            


        if(self.life <= 0):
            self.run_idle(self.dieImage)
            if self.n  == 0:
                self.kill()

        elif(self.hurt):
            self.run_idle(self.hurtImage,2)
            if self.n  == 0:
                self.hurt = False
        else:
            self.run_idle(self.runImage)
       



    

        self.image = pygame.transform.flip(self.image,self.direction,False)
        self.boundary.center = self.rect.center



class Person(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = "3 Cyborg"
        self.runImage,_ = load_image(f"{char}/{self.name}/Run2.png")
        self.idleImage,_ = load_image(f"{char}/{self.name}/Idle2.png")
        self.jumpImage,_ = load_image(f"{char}/{self.name}/Jump2.png")
        
        self.hands_right = [load_image(f"{hand}/{self.name}/{i}.png")[0] for i in range(6,11)]
        self.hands_left = [load_image(f"{hand}/{self.name}/{i}.png")[0] for i in range(1,6)]
        self.rect = pygame.Rect(0,0,72,96)
        self.hand_index = 4
        self.gun_index = 0
        self.rect = self.rect.move(100,300)
        self.velocity = 0

        self.direction = False
        self.img = self.runImage.subsurface(0,0,96,96)
        self.n = 0
        self.bullet_t = 0
        self.boundary = pygame.Rect(0,0,35,80)


  
    def run_idle(self,img):
        if(self.n < int(img.width/img.height -1)):
            self.img = img.subsurface(int(np.floor(self.n))*96,20,68,75)
            self.n = self.n + 0.12
        else:
            self.n = 0
    def run_jump(self,img):
        if(self.jump_t < int(img.width/img.height -1)):
            self.img = img.subsurface(int(np.floor(self.jump_t))*96,0,68,96)

    def run_image(self,img):
        dir = to_int(self.direction)
        self.run_idle(img)
        return(-dir*5)
        


    def update(self,keys):

        if(self.velocity < 5):
             self.velocity += 0.5

        dy = self.velocity
        dx = 0

       
        if keys[pygame.K_RIGHT]:
            dx = self.run_image(self.runImage)
        elif keys[pygame.K_LEFT]:
            dx = self.run_image(self.runImage)
        else:
            self.run_idle(self.idleImage)

        if keys[pygame.K_SPACE] and self.hand_index > 0:
            if(self.bullet_t > 4):
                index = self.hand_index - 1
                self.bullet_t = 0
                allsprites.add(Bullet(self.gun_index+1,self.rect,index,self.direction))
            else:
                self.bullet_t += guns_rate[self.gun_index]

        for tile in world.tiles:
            if tile[1].colliderect(self.boundary.x,self.boundary.y + dy, self.boundary.width,self.boundary.height):  
                if(tile[1].bottom > self.boundary.top and tile[1].top < self.boundary.bottom):
                    if(self.velocity < 0):
                        self.velocity = -self.velocity
                elif(self.velocity >= 0):      
                    self.velocity = 0
                    # dy = tile[1].top - self.rect.bottom
                    dy = 0
            if tile[1].colliderect(self.boundary.x+dx,self.boundary.y,  self.boundary.width,self.boundary.height): 
                dx = 0
        if(dx + self.boundary.bottomright[0] > 1600 or dx + self.boundary.bottomleft[0] < 0):
                dx = 0

               
       
            
        
        self.rect.y += dy
        self.rect.x += dx
        
        self.image_surface = pygame.Surface((72,96),pygame.SRCALPHA)
        hand_left = self.hands_left[self.hand_index]
        hand_right = self.hands_right[self.hand_index]
        self.image_surface.blit(hand_left,(6 ,5))
        self.image_surface.blit(self.img,(0,4))

        if(self.hand_index > 0):
            gun_rotation = gun_transform[self.hand_index-1]
            gun = pygame.transform.rotate(guns[self.gun_index],gun_rotation['angle'])
            self.image_surface.blit(gun,gun_rotation['shift'])

        self.image_surface.blit(hand_right,(6 ,8))
        self.image = pygame.transform.flip(self.image_surface,self.direction,False)
     
        self.boundary = pygame.Rect(0,0,50,60)
        self.boundary.center = self.rect.center

        # pygame.draw.rect(screen,"RED",self.boundary)


pygame.init()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((w, h))

form_data = {
    "Your Name":"short_text",
}

panel_rect = pygame.Rect((w-w2)/2, (h-h2)/2, w2, h2)
cyborg = Person()

allsprites = pygame.sprite.Group(cyborg)
bats = pygame.sprite.Group()
objects1 = pygame.sprite.Group(Object('Bushes',19,300,8),Object('Bushes',14,435,8))
objects2 = pygame.sprite.Group()

objects1.add(Object('Fountain',1,1000,9,True))
objects1.add(Object('Other',1,700,7))

for i in range(1,15):
    objects2.add(Object('Grass',i,650+15*i,7))
objects1.add(Object('Other',2,1230,10))
objects1.add(Object('Benches',1,30,6))
objects2.add(Object('Other',3,130,6))

objects1.add(Object('Benches',1,30,6))




for i in range(10):
    bats.add(Enemy(i))



Start_Panel = UIPanel(panel_rect,1,manager)
Start_Button = UIButton(pygame.Rect((w2-200)/2, h2-150, 200, 60), 'ENTER', manager, Start_Panel)
Start_InputBox = UITextEntryLine(pygame.Rect((w2-200)/2, h2-250, 200, 60),manager,placeholder_text="Username",container=Start_Panel)

font = pygame.font.Font("./data/CyberpunkCraftpixPixel.otf", 20)
text = font.render(username,1,(255,255,255))
textpos = text.get_rect()
textpos.centerx = screen.get_rect().centerx
textpos.centery = screen.get_rect().centery



world = World()

game = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == Start_Button):
            username = Start_InputBox.get_text()
            game = True
        if (event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                cyborg.hand_index = toggle(cyborg.hand_index,3)
            if(event.key == pygame.K_RSHIFT and np.abs(cyborg.velocity) < 1):
                cyborg.velocity = -12
            if(event.key == pygame.K_DOWN):
                cyborg.hand_index = toggleN(cyborg.hand_index,3)
            if(event.key == pygame.K_RCTRL):
                cyborg.gun_index = toggle(cyborg.gun_index,8)
            if(event.key == pygame.K_LEFT):
                cyborg.direction = True
                # cyborg.rect.x += 35
            if(event.key == pygame.K_RIGHT):
                cyborg.direction = False
   
    Start_Panel.kill()

    if(game):
        keys = pygame.key.get_pressed()

        screen.blit(bgImage,(0,-200))
        text = font.render("username", 1, (10, 10, 10))
        screen.blit(text)



        
        objects1.update()
        objects1.draw(screen)

        allsprites.update(keys)
        allsprites.draw(screen)
        
        bats.update()
        bats.draw(screen)

        objects2.update()
        objects2.draw(screen)
        # grid(screen)
        world.update()



    manager.update(dt)
    manager.draw_ui(screen)

    pygame.display.update()
    dt = clock.tick(60) / 1000



pygame.quit()
