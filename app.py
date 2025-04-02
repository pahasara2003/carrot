import pygame
import socketio
import threading
import json

# standard Python
sio = socketio.SimpleClient()
sio.connect('http://35.200.196.70:3000')
print('my sid is', sio.sid)
running = True
dt = 0


class GameObject:

    def __init__(self,id,position):

        self.position = pygame.Vector2(position[0],position[1])
        self.t = 0
        self.id = id

    def move(self,key):
        if keys[pygame.K_UP]:
            self.position.y -= 300 * dt
            sio.emit('player-move', list(self.position))
        if keys[pygame.K_DOWN]:
            self.position.y += 300 * dt
            sio.emit('player-move', list(self.position))
        if keys[pygame.K_LEFT]:
            self.position.x -= 300 * dt
            sio.emit('player-move', list(self.position))
        if keys[pygame.K_RIGHT]:
            self.position.x += 300 * dt
            sio.emit('player-move', list(self.position))


    def update(self):
        pygame.draw.circle(background, (0, 0, 255), self.position, 20)

PlayerGroup = []


def socket_listen_process():
    while running:
        event = sio.receive()
        print(event)
        if(event[0] == 'update'):
            pass
            msg = json.loads(event[1:][0])
            for p in PlayerGroup:
                if p.id == msg["id"] and p.id != sio.sid:
                    p.position = pygame.Vector2(tuple(msg['position']))

        elif(event[0] == 'new-player'):
            msg = json.loads(event[1:][0])

            if(len(PlayerGroup) == 0):
                PlayerGroup.append(GameObject(msg["id"],msg["position"]))
            elif(len([p for p in PlayerGroup if p.id == msg["id"]]) == 0):
                PlayerGroup.append(GameObject(msg["id"],msg["position"]))
        

listen_thread = threading.Thread(target=socket_listen_process)
listen_thread.start()

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
background = screen
background.fill((250, 250, 250))

font = pygame.font.Font(None, 36)
text = font.render("Hello There", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
textpos.centery = background.get_rect().centery
background.blit(text, textpos)

player = [p for p in PlayerGroup if p.id == sio.sid][0]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    screen.fill((250, 250, 250))
    screen.blit(text, (0, 0))
    player.move(keys)

    for p in PlayerGroup:
        p.update()
    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()
listen_thread.join()