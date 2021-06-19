import pygame

from pygame.locals import *
from enum import Enum

from agent import Agent
from cell import Cell
from civilian import Civilian
from item import Item
from gameState import Gamestate
from monster import Monster
from scientist import Scientist
from soldier import Soldier

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,     0,   0)
COLOR_RED = (255,   0,   0)
COLOR_GREEN = (0,   255,   0)
COLOR_ORANGE = (255, 165,   0)
COLOR_DARKGREEN = (0,   155,   0)
COLOR_DARKGRAY = (40,   40,  40)
COLOR_BLUE = (0,     0, 255)
COLOR_DARKBLUE = (0,     0, 155)
COLOR_YELLOW = (255,  255,  0)
COLOR_PINK = (255,  43, 227)


class Renderer:
    """
    This class is responsible for rendering a Gamestate (gameState.py)
    """

    def __init__(self, windowWidth, windowHeight, nCellsHorizontal, nCellsVertical, fps=10):
        pygame.init()
        self.__clearColor = COLOR_BLACK
        self.__fps = fps
        self.__fpsClock = pygame.time.Clock()
        self.__windowWidth = windowWidth
        self.__windowHeight = windowHeight
        self.__cellWidth = windowWidth//nCellsHorizontal
        self.__cellHeight = windowHeight//nCellsVertical
        self.__displaySurface = pygame.display.set_mode(
            (self.__windowWidth, self.__windowHeight))
        pygame.display.set_caption('Labyrinth')

    def __drawRect(self, x: float, y: float, w: float, h: float, color: (int, int, int)):
        pygame.draw.rect(self.__displaySurface, color, pygame.Rect(x, y, w, h))

    def __drawCircle(self, x: float, y: float, w: float, h: float, color: (int, int, int)):
        pygame.draw.ellipse(self.__displaySurface, color,
                            pygame.Rect(x, y, w, h))

    def __drawLine(self, x1: int, y1: int, x2: int, y2: int, color: (int, int, int), width: int = 1):
        pygame.draw.line(self.__displaySurface, color,
                         (x1, y1), (x2, y2), width)

    def __drawTri(self, tri: [(int, int), (int, int), (int, int)], color: (int, int, int)):
        pygame.draw.polygon(self.__displaySurface, color, tri)

    def __getFacingTri(self, direction: str, x: int, y: int, w: int, h: int):
        tl = (x, y)
        tr = (x + w, y)
        br = (x + w, y + h)
        bl = (x, y + h)

        cu = (x + w/2, y)
        cr = (x + w, y + h/2)
        cd = (x + w/2, y + h)
        cl = (x, y + h/2)

        if direction == "right":
            return [tl, cr, bl]
        if direction == "up":
            return [bl, cu, br]
        if direction == "left":
            return [br, cl, tr]
        if direction == "down":
            return [tl, cd, tr]
        return []

    def __drawItem(self, x: int, y: int, item: Item):
        color = COLOR_DARKGRAY
        xr, yr = (x * self.__cellWidth, y * self.__cellHeight)
        if item == Item.keyCard:
            itemImage = pygame.image.load("keycard.png")
            itemImage = pygame.transform.scale(itemImage, (self.__cellWidth // 2, self.__cellHeight // 2))
            self.__displaySurface.blit(itemImage, (xr, yr))
        if item == Item.gun:
            itemImage = pygame.image.load("shotgun.png")
            itemImage = pygame.transform.scale(itemImage, (self.__cellWidth // 2, self.__cellHeight // 2))
            self.__displaySurface.blit(itemImage, (xr, yr))
        if item == Item.research:
            itemImage = pygame.image.load("science.png")
            itemImage = pygame.transform.scale(itemImage, (self.__cellWidth // 2, self.__cellHeight // 2))
            self.__displaySurface.blit(itemImage, (xr, yr))

    def __drawAgent(self, x: int, y: int, agent: Agent):
        color = COLOR_DARKGRAY
        xr, yr = (x * self.__cellWidth, y * self.__cellHeight)
        if isinstance(agent, Civilian):
            color = COLOR_BLUE
            xr = xr
            yr = yr
        if isinstance(agent, Soldier):
            color = COLOR_GREEN
            xr = xr + self.__cellWidth // 2
            yr = yr
        if isinstance(agent, Scientist):
            color = COLOR_ORANGE
            xr = xr
            yr = yr + self.__cellHeight // 2
        if isinstance(agent, Monster):
            color = COLOR_RED
            xr = xr + self.__cellWidth // 2
            yr = yr + self.__cellHeight // 2
        # TODO: When we get images, draw the image instead.
        self.__drawCircle(xr, yr, self.__cellWidth // 2,
                          self.__cellHeight // 2, color)
        facingTri = self.__getFacingTri(
            agent.getDirection(), xr, yr, self.__cellWidth//2, self.__cellHeight//2)
        self.__drawTri(facingTri, COLOR_WHITE)

    def __drawWalls(self, x: int, y: int, walls: {"up": bool, "right": bool, "down": bool, "left": bool}):
        color = COLOR_WHITE
        xr, yr = (x * self.__cellWidth, y * self.__cellHeight)
        if walls['up']:
            self.__drawLine(xr, yr, xr + self.__cellWidth, yr, color)
        if walls['right']:
            self.__drawLine(xr + self.__cellWidth, yr, xr +
                            self.__cellWidth, yr + self.__cellHeight, color)
        if walls['down']:
            self.__drawLine(xr, yr + self.__cellHeight, xr +
                            self.__cellWidth, yr + self.__cellHeight, color)
        if walls['left']:
            self.__drawLine(xr, yr, xr, yr + self.__cellHeight, color)

    def __drawExit(self, x: int, y: int):
        color = COLOR_PINK
        xr, yr = (x * self.__cellWidth, y * self.__cellHeight)
        self.__drawRect(xr, yr, self.__cellWidth,
                        self.__cellHeight, color)

    def __drawCell(self, x: int, y: int, cell: Cell):
        if cell.isExit:
            self.__drawExit(x, y)
        for item in cell.getItemList():
            self.__drawItem(x, y, item)
        for agent in cell.getAgentList():
            self.__drawAgent(x, y, agent)
        self.__drawWalls(x, y, {"up": cell.isWallUp(),
                                "right": cell.isWallRight(),
                                "down": cell.isWallDown(),
                                "left": cell.isWallLeft()})

    def __drawGrid(self, width: int, height: int):
        for x in range(0, width):
            pygame.draw.line(self.__displaySurface, COLOR_DARKGRAY,
                             (x * self.__cellWidth, 0),
                             (x * self.__cellWidth, self.__windowHeight))
        for y in range(0, height):
            pygame.draw.line(self.__displaySurface, COLOR_DARKGRAY,
                             (0, y * self.__cellHeight),
                             (self.__windowWidth, y * self.__cellHeight))

    def __drawState(self, state: Gamestate):
        self.__drawGrid(state.getWidth(), state.getHeight())

        for x in range(0, state.getWidth()):
            for y in range(0, state.getHeight()):
                cell = state.getCellAt(x, y)
                self.__drawCell(x, y, cell)

    def draw(self, state: Gamestate):
        self.__displaySurface.fill(self.__clearColor)
        self.__drawState(state)
        pygame.display.update()
        self.__fpsClock.tick(self.__fps)
