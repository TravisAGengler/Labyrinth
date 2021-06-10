class Cell:
    def __init__(self, wallUp, wallDown, wallLeft, wallRight):
        # Boolean: Whether there is a wall
        self.WALL_UP = wallUp
        self.WALL_DOWN = wallDown
        self.WALL_LEFT = wallLeft
        self.WALL_RIGHT = wallRight
        # Cell object: Adjacent cell data
        self.cellUp = None
        self.cellDown = None
        self.cellRight = None
        self.cellLeft = None
        self.itemList = []
        self.agentList = []

    def setWalls(self, up, down, left, right):
        self.WALL_UP = up
        self.WALL_DOWN = down
        self.WALL_LEFT = left
        self.WALL_RIGHT = right

    def isWallUp(self):
        return self.WALL_UP

    def isWallDown(self):
        return self.WALL_DOWN

    def isWallLeft(self):
        return self.WALL_LEFT

    def isWallRight(self):
        return self.WALL_RIGHT

    def setCellUp(self, cell):
        self.cellUp = cell

    def setCellDown(self, cell):
        self.cellDown = cell

    def setCellLeft(self, cell):
        self.cellLeft = cell

    def setCellRight(self, cell):
        self.cellRight = cell

    def getCellUp(self):
        return self.cellUp

    def getCellDown(self):
        return self.cellDown

    def getCellLeft(self):
        return self.cellLeft

    def getCellRight(self):
        return self.cellRight

    def getItemList(self):
        return self.itemList

    def getAgentList(self):
        return self.agentList

    def addAgent(self, agent):
        self.agentList.append(agent)

    def addItem(self, item):
        self.itemList.append(item)

    def removeAgent(self, agent):
        try:
            self.agentList.remove(agent)
        except ValueError:
            print('The agent is not in the cell')
            return False
        return True

    def removeItem(self, item):
        try:
            self.agentList.remove(item)
        except ValueError:
            print('The item is not in the cell')
            return False
        return True
