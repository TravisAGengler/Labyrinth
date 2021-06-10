
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

    def remember(self, x, y, cell, beenTo=False):
        self.__grid[x][y] = cell
        if beenTo:
            self.__visitedCells[x][y] = True

    def getCellAt(self, x, y):
        return self.__grid[x][y]

    def getCellLocation(self, cell):
        for x in range(len(self.__grid)):
            for y in range(len(self.__grid[x])):
                if self.__grid[x][y] == cell:
                    return {"x": x, "y": y}
        return None

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
            "up": currentCell.getCellUp() if currentCell.isWallUp() == False else None,
            "down": currentCell.getCellDown() if currentCell.isWallDown() == False else None,
            "left": currentCell.getCellLeft() if currentCell.isWallLeft() == False else None,
            "right": currentCell.getCellRight() if currentCell.isWallRight() == False else None
        }