from constants import load_image,bullet_counts
import pygame



class UIElement(pygame.sprite.Sprite):
    def __init__(self,bg ="",x=0,y=0,scale=3):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(bg,scale=scale)
        self.rect.move_ip(x,y )

class StatePanel:
    def __init__(self,font,X=0,Y=0,user="3 Cyborg"):
        self.menu = pygame.sprite.Group()
        self.menu.add(UIElement(bg="UI/1 Frames/Frame_37.png",x=X,y=Y,scale=4))
        self.menu.add(UIElement(bg=f"1 Characters/{user}/Idle1.png",x=X+43,y=Y+27,scale=1.4))
        self.menu.add(UIElement(bg="UI/1 Frames/Frame_38.png",x=100+X,y=4+Y))
        self.menu.add(UIElement(bg="UI/1 Frames/Frame_40.png",x=196+X,y=4+Y))
        self.x,self.y = X+140,Y+55-9
        self.font = font

    def update(self,screen,count):
        self.menu.update()
        self.menu.draw(screen)
        text = self.font.render(f"KILLS : {count}",1,(255,255,255))
        screen.blit(text,(self.x,self.y))

class LoadingBar:
    def __init__(self,X=500,Y=0,maxVal=100,scale=1,stretch=0.5):
        self.menu = pygame.sprite.Group()
        self.container,_ = load_image("UI/2 Bars/HealthBar5.png",scale=scale,strech=stretch)
        self.load_image,_ = load_image("UI/2 Bars/HealthBar1.png",scale=scale,strech=stretch)
        self.x,self.y = X,Y
        self.w,self.h = self.load_image.size
        self.maxVal = maxVal
    def update(self,screen,value):
        x = value*self.w/self.maxVal
        load = self.load_image.subsurface(0,0,x,self.h)
        screen.blit(self.container,(self.x,self.y))
        screen.blit(load,(self.x,self.y))


class GunPanel:
    def __init__(self,font,X=20,Y=620,gun=1):
        self.menu = pygame.sprite.Group()
        self.gun = UIElement(bg=f"2 Guns/{gun+1}_1.png",x=X+90,y=Y+40,scale=3)
        self.menu.add(self.gun)
        self.x,self.y = X,Y+10
        self.font = font

    def update(self,screen,owner):
        index = owner.gun_index
    
        self.gun.image,_ = load_image(f"2 Guns/{index+1}_1.png",scale=3.5) 
        self.menu.update()
        self.menu.draw(screen)
        val = owner.bulletCount[index]
        c = 0  if val < bullet_counts[index]*0.25 else 255
        count_text = self.font.render(f"{val} / {bullet_counts[index]}",1,(255,c,c))
        screen.blit(count_text,(self.x+70,self.y))


class ConfigPanel():
     def __init__(self,font):
        image,_ = load_image("UI/1 Frames/Interface windows.png",scale=1)
        self.container = image.subsurface(450,720,300,190)

        self.container = pygame.transform.scale_by(self.container,2.2)
     def update(self,screen):
        screen.blit(self.container)
