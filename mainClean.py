import pygame
from utils import *
import pygame.display
from random import randint
from scraper import *
from screensAndFunctions import *

fpsClock = pygame.time.Clock()
FPS = 30
idling = False
pygame.time.set_timer(pygame.USEREVENT, int(refreshRate)*1000)


running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            print("refreshing")
            checkAndQueue()
        if not idling:
            if event.type == pygame.USEREVENT:
                refreshAllText()
            if event.type == pygame.VIDEORESIZE:
                print("true")
                for button in Button.buttons:
                    button.resize(screen)
                Text.resizeAll(screen)

    if not idling:
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        Screen.run(screen, events)
        pygame.display.flip()
        fpsClock.tick(FPS)
    
    handleQueue(events)
