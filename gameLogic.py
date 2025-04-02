import pygame
import numpy as np
from roles import *
from setup import *
from ui import *


game = True
gunPanel = GunPanel(font)
configPanel = ConfigPanel(font)
lifeBar = LoadingBar(120,105-12,100,scale=4.8,stretch=0.25)


while running:
    count = inital_bats_count - bats.__len__()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN and game):
            gameKeyEvent(event)

    updateWorld(screen,game)
    
    if not game:
        configPanel.update(screen)
    else:
        gunPanel.update(screen,cyborg)

    lifeBar.update(screen,cyborg.life)

    pygame.display.update()
    dt = clock.tick(60) / 1000
pygame.quit()
