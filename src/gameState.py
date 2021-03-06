import random

from cell import Cell
from civilian import Civilian
from item import Item
from monster import Monster
from scientist import Scientist
from soldier import Soldier
from rng import labyrinthSeed


class Gamestate:
    """
    This is the representation for the true state of the game, separate from the Agent State (state.py)
    """

    def __init__(self, width, height):
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
        self.__applyLayout()
        self.__linkCells()
        self.__escapees = []
        self.__victors = []

    def __applyLayout(self):
        # Place agents

        # TRICKY: With the way things are now, the order here determines move priority
        # Place Monster at (width-1, height-1)
        self.__agents["monster"] = Monster(
            startingLocation={'x': self.__width-1, 'y': self.__height-1},
            sightRange=3, width=self.__width, height=self.__height,
            name="monster")
        self.__grid[self.__width-1][self.__height -
                                    1].addAgent(self.__agents["monster"])

        # Place Civilian at (0, 0)
        self.__agents["civilian"] = Civilian(
            startingLocation={'x': 0, 'y': 0},
            sightRange=3, width=self.__width, height=self.__height,
            name="civilian")
        self.__grid[0][0].addAgent(self.__agents["civilian"])

        # Place Soldier at (width-1, 0)
        self.__agents["soldier"] = Soldier(
            startingLocation={'x': self.__width-1, 'y': 0},
            sightRange=3, width=self.__width, height=self.__height,
            name="soldier")
        self.__grid[self.__width - 1][0].addAgent(self.__agents["soldier"])

        # Place Scientist at (0, height-1)
        self.__agents["scientist"] = Scientist(
            startingLocation={'x': 0, 'y': self.__height-1},
            sightRange=3, width=self.__width, height=self.__height,
            name="scientist")
        self.__grid[0][self.__height - 1].addAgent(self.__agents["scientist"])

        exit1Locations = [{'x': 0, 'y': 8},
                          {'x': 5, 'y': 9},
                          {'x': 9, 'y': 4}]
        exit2Locations = [{'x': 9, 'y': 1},
                          {'x': 3, 'y': 0},
                          {'x': 0, 'y': 3}]
        researchLocations = [{'x': 1, 'y': 1},
                             {'x': 2, 'y': 9},
                             {'x': 7, 'y': 6},
                             {'x': 7, 'y': 0},
                             {'x': 5, 'y': 5}]
        gunLocations = [{'x': 1, 'y': 8},
                        {'x': 4, 'y': 1},
                        {'x': 7, 'y': 2},
                        {'x': 9, 'y': 8},
                        {'x': 4, 'y': 4}]
        keyCardLocations = [{'x': 6, 'y': 3},
                            {'x': 1, 'y': 6},
                            {'x': 3, 'y': 2},
                            {'x': 8, 'y': 9},
                            {'x': 6, 'y': 5}]

        labyrinthSeed('layout')
        exitNum = random.randint(0, 2)
        researchNum = random.randint(0, 4)
        gunNum = random.randint(0, 4)
        keyNum = random.randint(0, 4)

        # Place both Exits at random location for the seed (they are paired together)
        self.__grid[exit1Locations[exitNum]['x']
                    ][exit1Locations[exitNum]['y']].setIsExit(True)
        self.__grid[exit2Locations[exitNum]['x']
                    ][exit2Locations[exitNum]['y']].setIsExit(True)
        # Place Research at random location for the seed
        self.__grid[researchLocations[researchNum]['x']
                    ][researchLocations[researchNum]['y']].addItem(Item.research)
        # Place Gun at random location for the seed
        self.__grid[gunLocations[gunNum]['x']
                    ][gunLocations[gunNum]['y']].addItem(Item.gun)
        # Place Keycard at random location for the seed
        self.__grid[keyCardLocations[keyNum]['x']
                    ][keyCardLocations[keyNum]['y']].addItem(Item.keyCard)

        # Place walls
        # Top row of maze
        self.__grid[0][0].setWalls(True, False, True, True)
        self.__grid[1][0].setWalls(True, False, True, True)
        self.__grid[2][0].setWalls(True, False, True, False)
        self.__grid[3][0].setWalls(True, False, False, False)
        self.__grid[4][0].setWalls(True, True, False, False)
        self.__grid[5][0].setWalls(True, False, False, True)
        self.__grid[6][0].setWalls(True, False, True, False)
        self.__grid[7][0].setWalls(True, False, False, False)
        self.__grid[8][0].setWalls(True, False, False, False)
        self.__grid[9][0].setWalls(True, True, False, True)
        # 2nd Row
        self.__grid[0][1].setWalls(False, False, True, True)
        self.__grid[1][1].setWalls(False, False, True, False)
        self.__grid[2][1].setWalls(False, True, False, True)
        self.__grid[3][1].setWalls(False, True, True, False)
        self.__grid[4][1].setWalls(True, True, False, True)
        self.__grid[5][1].setWalls(False, False, True, False)
        self.__grid[6][1].setWalls(False, False, False, True)
        self.__grid[7][1].setWalls(False, False, True, True)
        self.__grid[8][1].setWalls(False, False, True, False)
        self.__grid[9][1].setWalls(True, True, False, True)
        # 3rd Row
        self.__grid[0][2].setWalls(False, True, True, False)
        self.__grid[1][2].setWalls(False, True, False, False)
        self.__grid[2][2].setWalls(True, True, False, False)
        self.__grid[3][2].setWalls(True, True, False, False)
        self.__grid[4][2].setWalls(True, True, False, False)
        self.__grid[5][2].setWalls(False, False, False, True)
        self.__grid[6][2].setWalls(False, False, False, True)
        self.__grid[7][2].setWalls(False, False, True, True)
        self.__grid[8][2].setWalls(False, True, True, False)
        self.__grid[9][2].setWalls(True, False, False, True)
        # 4th Row
        self.__grid[0][3].setWalls(True, True, True, False)
        self.__grid[1][3].setWalls(True, True, False, False)
        self.__grid[2][3].setWalls(True, False, False, False)
        self.__grid[3][3].setWalls(True, True, False, False)
        self.__grid[4][3].setWalls(False, True, False, False)
        self.__grid[5][3].setWalls(False, False, False, True)
        self.__grid[6][3].setWalls(False, False, True, True)
        self.__grid[7][3].setWalls(False, True, True, False)
        self.__grid[8][3].setWalls(True, True, False, False)
        self.__grid[9][3].setWalls(False, False, False, True)
        # 5th Row
        self.__grid[0][4].setWalls(True, False, True, False)
        self.__grid[1][4].setWalls(True, True, False, False)
        self.__grid[2][4].setWalls(False, False, False, False)
        self.__grid[3][4].setWalls(True, False, True, True)
        self.__grid[4][4].setWalls(True, False, True, True)
        self.__grid[5][4].setWalls(False, False, True, True)
        self.__grid[6][4].setWalls(False, True, True, False)
        self.__grid[7][4].setWalls(True, True, False, False)
        self.__grid[8][4].setWalls(True, True, False, False)
        self.__grid[9][4].setWalls(False, False, False, True)
        # 6th Row
        self.__grid[0][5].setWalls(False, True, True, False)
        self.__grid[1][5].setWalls(True, False, False, True)
        self.__grid[2][5].setWalls(False, False, True, True)
        self.__grid[3][5].setWalls(False, False, True, True)
        self.__grid[4][5].setWalls(False, False, True, True)
        self.__grid[5][5].setWalls(False, False, True, True)
        self.__grid[6][5].setWalls(True, False, True, True)
        self.__grid[7][5].setWalls(True, False, True, False)
        self.__grid[8][5].setWalls(True, True, False, True)
        self.__grid[9][5].setWalls(False, False, True, False)
        # 7th Row
        self.__grid[0][6].setWalls(True, False, True, False)
        self.__grid[1][6].setWalls(False, True, False, True)
        self.__grid[2][6].setWalls(False, True, True, False)
        self.__grid[3][6].setWalls(False, False, False, True)
        self.__grid[4][6].setWalls(False, False, True, True)
        self.__grid[5][6].setWalls(False, False, True, True)
        self.__grid[6][6].setWalls(False, False, True, True)
        self.__grid[7][6].setWalls(False, False, True, False)
        self.__grid[8][6].setWalls(True, False, False, False)
        self.__grid[9][6].setWalls(False, False, False, True)
        # 8th Row
        self.__grid[0][7].setWalls(False, True, True, False)
        self.__grid[1][7].setWalls(True, False, False, False)
        self.__grid[2][7].setWalls(True, True, False, False)
        self.__grid[3][7].setWalls(False, True, False, False)
        self.__grid[4][7].setWalls(False, True, False, True)
        self.__grid[5][7].setWalls(False, False, True, True)
        self.__grid[6][7].setWalls(False, False, True, False)
        self.__grid[7][7].setWalls(True, False, False, False)
        self.__grid[8][7].setWalls(False, False, False, True)
        self.__grid[9][7].setWalls(True, False, True, True)
        # 9th Row
        self.__grid[0][8].setWalls(True, True, True, False)
        self.__grid[1][8].setWalls(False, False, False, False)
        self.__grid[2][8].setWalls(True, True, False, False)
        self.__grid[3][8].setWalls(True, True, False, False)
        self.__grid[4][8].setWalls(True, False, False, True)
        self.__grid[5][8].setWalls(False, True, True, False)
        self.__grid[6][8].setWalls(False, True, False, True)
        self.__grid[7][8].setWalls(False, False, True, True)
        self.__grid[8][8].setWalls(False, False, True, True)
        self.__grid[9][8].setWalls(False, False, True, True)
        # 10th Row
        self.__grid[0][9].setWalls(True, True, True, False)
        self.__grid[1][9].setWalls(False, True, False, True)
        self.__grid[2][9].setWalls(True, True, True, False)
        self.__grid[3][9].setWalls(True, True, False, False)
        self.__grid[4][9].setWalls(False, True, False, False)
        self.__grid[5][9].setWalls(True, True, False, False)
        self.__grid[6][9].setWalls(True, True, False, False)
        self.__grid[7][9].setWalls(False, True, False, True)
        self.__grid[8][9].setWalls(False, True, True, False)
        self.__grid[9][9].setWalls(False, True, False, True)

    def __linkCells(self):
        """
        Link all cells together by filling in their neighbor variables
        Also fill in walls from neighbors and grid edges where necessary
        """
        for x in range(len(self.__grid)):
            for y in range(len(self.__grid[x])):
                if x + 1 < self.__width:
                    self.__grid[x][y].setCellRight(
                        self.__grid[x + 1][y])
                    if self.__grid[x + 1][y].isWallLeft():
                        self.__grid[x][y].WALL_RIGHT = True
                else:
                    self.__grid[x][y].WALL_RIGHT = True
                if x - 1 >= 0:
                    self.__grid[x][y].setCellLeft(
                        self.__grid[x - 1][y])
                    if self.__grid[x - 1][y].isWallRight():
                        self.__grid[x][y].WALL_LEFT = True
                else:
                    self.__grid[x][y].WALL_LEFT = True
                if y + 1 < self.__height:
                    self.__grid[x][y].setCellDown(
                        self.__grid[x][y + 1])
                    if self.__grid[x][y + 1].isWallUp():
                        self.__grid[x][y].WALL_DOWN = True
                else:
                    self.__grid[x][y].WALL_DOWN = True
                if y - 1 >= 0:
                    self.__grid[x][y].setCellUp(self.__grid[x][y - 1])
                    if self.__grid[x][y - 1].isWallDown():
                        self.__grid[x][y].WALL_UP = True
                else:
                    self.__grid[x][y].WALL_UP = True

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getCellAt(self, x, y):
        return self.__grid[x][y]

    def getAgents(self):
        return self.__agents

    def removeAgent(self, agent):
        self.__agents = {an: a for an,
                         a in self.__agents.items() if a != agent}

    def addEscapee(self, agent):
        self.__escapees.append(agent)

    def removeEscapee(self, agent):
        self.__escapees = [e for e in self.__escapees if e != agent]

    def addVictor(self, agent):
        self.__victors.append(agent)

    def getEscapees(self):
        return self.__escapees

    def getVictors(self):
        return self.__victors
