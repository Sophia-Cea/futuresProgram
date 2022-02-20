import pygame
from utils import *
import pygame.display
from random import randint
from scraper import *
from screensAndFunctions import *

fpsClock = pygame.time.Clock()
FPS = 30
pygame.time.set_timer(pygame.USEREVENT, int(refreshRate)*1000)
pygame.display.set_caption("Crystal Ball")


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            checkAndQueue()
        if not Screen.idling:
            if event.type == pygame.USEREVENT:
                refreshAllText()
            if event.type == pygame.VIDEORESIZE:
                for button in Button.buttons:
                    button.resize(screen)
                Text.resizeAll(screen)
        if Screen.idling:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stopIdling()

    if not Screen.idling:
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        Screen.run(screen, events)
        pygame.display.flip()
        fpsClock.tick(FPS)
    
    handleQueue(events)
