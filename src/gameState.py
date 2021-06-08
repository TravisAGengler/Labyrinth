from cell import Cell

from civilian import Civilian
from item import Item
from monster import Monster
from scientist import Scientist
from soldier import Soldier


class Gamestate:
    """
    This is the representation for the true state of the game, separate from the Agent State (state.py)
    """

    def __init__(self, width, height, layout):
        self.__agents = {}
        self.__width = width
        self.__height = height
        self.__grid = []
        for i in range(width):
            self.__grid.append([])
            for j in range(height):
                cell = Cell(wallUp=False, wallDown=False,
                            wallLeft=False, wallRight=False)
                self.__grid[i].append(cell)
        self.__applyLayout(layout)
        self.__linkCells()

    def __applyLayout(self, layout):
        # TODO: This is just a proof for rendering. Replace this with something we make from the layout provided
        # We can place agents and items randomly based on criteria

        # Place Civilian at (0, 0)
        self.__agents["civilian"] = Civilian(
            startingLocation={'x': 0, 'y': 0},
            sightRange=3, width=self.__width, height=self.__height)
        self.__grid[0][0].addAgent(self.__agents["civilian"])
        # Place Soldier at (width-1, 0)
        self.__agents["soldier"] = Soldier(
            startingLocation={'x': self.__width-1, 'y': 0},
            sightRange=3, width=self.__width, height=self.__height)
        self.__grid[self.__width - 1][0].addAgent(self.__agents["soldier"])
        # Place Scientist at (0, height-1)
        self.__agents["scientist"] = Scientist(
            startingLocation={'x': 0, 'y': self.__height-1},
            sightRange=3, width=self.__width, height=self.__height)
        self.__grid[0][self.__height - 1].addAgent(self.__agents["scientist"])
        # Place Monster at (width-1, height-1)
        self.__agents["monster"] = Monster(
            startingLocation={'x': self.__width-1, 'y': self.__height-1},
            sightRange=3, width=self.__width, height=self.__height)
        self.__grid[self.__width-1][self.__height -
                                    1].addAgent(self.__agents["monster"])

        # Place Research at (1, 1)
        self.__grid[1][1].addItem(Item.research)
        # Place Gun at (1, height-2)
        self.__grid[1][self.__height - 2].addItem(Item.gun)
        # Place Keycard at (width-2, 1)
        self.__grid[self.__width - 2][1].addItem(Item.keyCard)

        # Place a top wall at (4,4)
        self.__grid[4][4].WALL_UP = True
        # Place a right wall at (3,3)
        self.__grid[3][3].WALL_RIGHT = True
        # Place a down wall at (2,2)
        self.__grid[2][2].WALL_DOWN = True
        # Place a left wall at (1,0)
        self.__grid[1][0].WALL_LEFT = True

    def __linkCells(self):
        """
        Link all cells together by filling in their neighbor variables
        Also fill in walls from neighbors where necessary
        """
        for x in range(len(self.__grid)):
            for y in range(len(self.__grid[x])):
                if x + 1 < self.__width:
                    self.__grid[x][y].setCellRight(
                        self.__grid[x + 1][y])
                    if self.__grid[x + 1][y].isWallLeft():
                        self.__grid[x][y].WALL_RIGHT = True
                if x - 1 >= 0:
                    self.__grid[x][y].setCellLeft(
                        self.__grid[x - 1][y])
                    if self.__grid[x - 1][y].isWallRight():
                        self.__grid[x][y].WALL_LEFT = True
                if y + 1 < self.__height:
                    self.__grid[x][y].setCellDown(
                        self.__grid[x][y + 1])
                    if self.__grid[x][y + 1].isWallUp():
                        self.__grid[x][y].WALL_DOWN = True
                if y - 1 >= 0:
                    self.__grid[x][y].setCellUp(self.__grid[x][y - 1])
                    if self.__grid[x][y - 1].isWallDown():
                        self.__grid[x][y].WALL_UP = True

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getCellAt(self, x, y):
        return self.__grid[x][y]

    def getAgents(self):
        return self.__agents
