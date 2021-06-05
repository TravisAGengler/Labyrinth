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

    def __init__(self, width=10, height=10, layout=None):
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

    def __applyLayout(self, layout):
        # TODO: This is just a proof for rendering. Replace this with a better layout.
        # We can place agents and items randomly based on criteria

        # Place Civilian at (0, 0)
        self.__grid[0][0].addAgent(Civilian(startingLocation={'x': 0, 'y': 0}))
        # Place Soldier at (width-1, 0)
        self.__grid[self.__width -
                    1][0].addAgent(Soldier(startingLocation={'x': self.__width-1, 'y': 0}))
        # Place Scientist at (0, height-1)
        self.__grid[0][self.__height -
                       1].addAgent(Scientist(startingLocation={'x': 0, 'y': self.__height-1}))
        # Place Monster at (width-1, height-1)
        self.__grid[self.__width-1][self.__height - 1].addAgent(
            Monster(startingLocation={'x': self.__width-1, 'y': self.__height-1}))

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
        # Place a left wall at (1,1)
        self.__grid[1][1].WALL_LEFT = True

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getCellAt(self, x, y):
        return self.__grid[x][y]
