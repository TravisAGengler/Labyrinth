
class State:
    """
    An Agent's way of representing the world.
    Recreates the grid
    """

    def __init__(self, memoryLoss, width, height):
        # between 0 and 1. % chance that the Agent will forget details about a cell each tick.
        self.__memoryLoss = memoryLoss
        # dimensions of the grid
        self.__width = width
        self.__height = height
        # grid the Agent constructs while traversing the environment. None value indicates unseen cell
        self.__grid = []
        # grid of locations the agent has already traversed
        self.__visitedCells = []
        for i in range(width):
            self.__grid.append([])
            self.__visitedCells.append([])
            for j in range(height):
                self.__grid[i].append(None)
                self.__visitedCells[i].append(False)

        self.__breadTrails = []

    def remember(self, x, y, cell, beenTo=False):
        self.__grid[x][y] = cell
        if beenTo:
            self.__visitedCells[x][y] = True

    def getCellAt(self, x, y):
        return self.__grid[x][y]

    def getCellLocation(self, cell):
        if cell != None:
            for x in range(len(self.__grid)):
                for y in range(len(self.__grid[x])):
                    if self.__grid[x][y] == cell:
                        return {"x": x, "y": y}
        return None

    def getBreadTrails(self):
        return self.__breadTrails

    def getActiveBreadTrail(self):
        if len(self.__breadTrails) != 0:
            return self.__breadTrails[-1]
        else:
            return None

    def addBreadTrail(self, x, y):
        self.__breadTrails.append(self.BreadTrail(x, y))

    def finishBreadTrail(self):
        """
        remove the latest BreadTrail from the array of BreadTrails
        used when an agent finishes backtracking along the entire trail
        """
        self.__breadTrails.pop()


    def isVisited(self, x, y):
        return self.__visitedCells[x][y]

    def cellIsDeadEnd(self, cell):
        """
        Check if a cell has a way out, or if it is a dead end
        :param cell:  the cell to check
        :return:      True if dead end, False if not
        """
        wallCount = 0
        wallCount += cell.isWallUp()
        wallCount += cell.isWallDown()
        wallCount += cell.isWallLeft()
        wallCount += cell.isWallRight()
        return wallCount >= 3

    def getKnownSurroundings(self, x, y):
        """
        Determine which neighboring cells the Agent knows about
        :param x:  The x location of the agent
        :param y:  The y location of the agent
        :return:   a dict of known neighboring cells
        """
        currentCell = self.getCellAt(x, y)
        return {
            "up": currentCell.getCellUp() if not currentCell.isWallUp() else None,
            "down": currentCell.getCellDown() if not currentCell.isWallDown() else None,
            "left": currentCell.getCellLeft() if not currentCell.isWallLeft() else None,
            "right": currentCell.getCellRight() if not currentCell.isWallRight() else None
        }

    def resetVisitedCells(self):
        """
        Mark every cell in the state as unvisited.
        This functions to allow the agent to continue exploring the labyrinth after exploring all it initially can
        """
        for x in range(len(self.__visitedCells)):
            for y in range(len(self.__visitedCells[x])):
                self.__visitedCells[x][y] = False

    class BreadTrail:
        """
        A path of cells through the internal state
        Used by Agents to retrace their steps back to specific remembered points
        """

        def __init__(self, x, y):
            self.__startingPoint = {"x": x, "y": y}
            self.__path = [self.__startingPoint]

        def getNextStep(self, x, y):
            """
            Get the next step in the path while retracing steps
            :param x:  the x coordinate of the agent
            :param y:  the y coordinate of the agent
            :return:   the coordinates of the next cell
            """
            curr = self.__path.index({"x": x, "y": y})
            if curr == None or curr == 0:
                return None
            return self.__path[curr - 1]

        def addPoint(self, x, y):
            self.__path.append({"x": x, "y": y})

        def isFinished(self, x, y):
            return (x == self.__startingPoint["x"] and y == self.__startingPoint["y"])
