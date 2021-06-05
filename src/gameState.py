from cell import Cell


class Gamestate:
    """
    This is the representation for the true state of the game, separate from the Agent State (state.py)
    """

    def __init__(self, width=10, height=10):
        self.__width = width
        self.__height = height
        self.__grid = []
        for i in range(width):
            self.__grid.append([])
            for j in range(height):
                cell = Cell(wallUp=False, wallDown=False,
                            wallLeft=False, wallRight=False)
                self.__grid[i].append(cell)
        # Place a civilian top left
        # Place a soldier top right
        # Place a scientist bottom left
        # Place a monster bottom right

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getCellAt(self, row, col):
        return self.__grid[col][row]
