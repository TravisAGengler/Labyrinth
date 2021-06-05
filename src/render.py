import pygame

from pygame.locals import *


from gameState import Gamestate

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,   0,   0)
COLOR_RED = (255,   0,   0)
COLOR_GREEN = (0, 255,   0)
COLOR_DARKGREEN = (0, 155,   0)
COLOR_DARKGRAY = (40,  40,  40)
COLOR_BLUE = (0,   0, 255)
COLOR_DARKBLUE = (0,   0, 155)
COLOR_YELLOW = (255, 255,   0)


class Renderer:
    """
    This class is responsible for rendering a Gamestate (gameState.py)
    """

    def __init__(self, windowWidth=800, windowHeight=800, cellWidth=80, cellHeight=80, fps=10):
        pygame.init()
        self.__clearColor = COLOR_BLACK
        self.__fps = fps
        self.__fpsClock = pygame.time.Clock()
        self.__windowWidth = windowWidth
        self.__windowHeight = windowHeight
        self.__cellWidth = cellWidth
        self.__cellHeight = cellHeight
        self.__displaySurface = pygame.display.set_mode(
            (self.__windowWidth, self.__windowHeight))
        pygame.display.set_caption('Labyrinth')

    def __draw_grid(self, width: int, height: int):
        for x in range(0, width):
            pygame.draw.line(self.__displaySurface, COLOR_DARKGRAY,
                             (x * self.__cellWidth, 0),
                             (x * self.__cellWidth, self.__windowHeight))
        for y in range(0, height):
            pygame.draw.line(self.__displaySurface, COLOR_DARKGRAY,
                             (0, y * self.__cellHeight),
                             (self.__windowWidth, y * self.__cellHeight))

    def __drawState(self, state: Gamestate):
        self.__draw_grid(state.getWidth(), state.getHeight())

    def draw(self, state: Gamestate):
        self.__displaySurface.fill(self.__clearColor)
        self.__drawState(state)
        pygame.display.update()
        self.__fpsClock.tick(self.__fps)
