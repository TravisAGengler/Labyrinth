
class State:
    """
    An Agent's way of representing the world.
    Recreates the grid
    """

    def __init__(self, memoryLoss, width=10, height=10):
        # between 0 and 1. % chance that the Agent will forget details about a cell each tick.
        self.__memoryLoss = memoryLoss
        # dimensions of the grid
        self.__width = width
        self.__height = height
        # grid the Agent constructs while traversing the environment. None value indicates unseen cell
        self.__grid = []
        for i in range(width):
            self.__grid.append([])
            for j in range(height):
                self.__grid[j].append(None)


    def remember(self, x, y, cell):
        self.__grid[x][y] = cell