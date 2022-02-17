import pygame
from utils import *
import pygame.display
from random import randint
from scraper import *
from screensAndFunctions import *


fpsClock = pygame.time.Clock()
FPS = 30



running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            print("true")
            for button in Button.buttons:
                button.resize(screen)
            Text.resizeAll(screen)


    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    Screen.run(screen, events)
    pygame.display.flip()
    fpsClock.tick(FPS)
