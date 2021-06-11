from abc import ABC, abstractmethod
import random

from state import State


class Agent(ABC):

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, startingLocation, sightRange, width, height):
        self.__location = startingLocation  # {'x': x, 'y', y}
        self.__sightRange = sightRange  # how far the agent can see in front of itself
        self.__state = State(memoryLoss=0, width=width, height=height)
        # TODO: possibly change how direction is selected, will depend on how agents are spawned in
        self.__direction = self.UP # random.choice(self.DIRECTIONS)
        self.__inventory = []
        self.__isAlive = True
        self.__score = 0

        # map of how to turn based on current direction and desired direction
        # (agentDirection, desiredDirection): turnFunction
        self.turnDirections = {
            (self.UP, self.DOWN): self.turnAround,
            (self.UP, self.LEFT): self.turnLeft,
            (self.UP, self.RIGHT): self.turnRight,

            (self.DOWN, self.UP): self.turnAround,
            (self.DOWN, self.LEFT): self.turnRight,
            (self.DOWN, self.RIGHT): self.turnLeft,

            (self.LEFT, self.UP): self.turnRight,
            (self.LEFT, self.DOWN): self.turnLeft,
            (self.LEFT, self.RIGHT): self.turnAround,

            (self.RIGHT, self.UP): self.turnLeft,
            (self.RIGHT, self.DOWN): self.turnRight,
            (self.RIGHT, self.LEFT): self.turnAround
        }

        self.__actions = [self.pickUp, self.die, self.win,
                          self.turnRight, self.turnLeft, self.turnAround, self.move]

    """
    Abstract Methods
    """

    @abstractmethod
    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        # TODO: implement
        pass

    @abstractmethod
    def chooseAction(self, percepts):
        """
        Choose an action to perform
        :param percepts:  list of what the agent currently perceives
        :return:          the chosen action function
        """
        pass

    # TRICKY: While we would prefer to have this be a "private" method,
    # mangling makes it impossible to implement in the subclasses
    # See https://stackoverflow.com/a/31458576/7759262
    @abstractmethod
    def _getUtility(self, action, percepts):
        """
        Get the utility of a potential action
        :param action:    the action to determine the utility of
        :param percepts:  list of what the agent currently perceives
        :return:          the numerical utility of the action
        """
        pass

    """
    Getter Methods
    """

    def getLocation(self):
        return self.__location

    def getSightRange(self):
        return self.__sightRange

    def getDirection(self):
        return self.__direction

    def isAlive(self):
        return self.__isAlive

    def getScore(self):
        return self.__score

    def getInventory(self):
        return self.__inventory

    def getState(self):
        return self.__state

    def getActions(self):
        return self.__actions

    """
    Setter Methods
    """

    def setLocation(self, location):
        self.__location = location

    def setScore(self, score):
        self.__score = score

    def addAction(self, action):
        self.__actions.append(action)

    """
    Actions
    """

    def pickUp(self, item):
        self.__inventory.append(item)

    def die(self):
        """
        Kill the agent and drop all its items
        :return:  the list of dropped items
        """
        self.__isAlive = False
        inventory = self.__inventory.copy()
        self.__inventory = []
        return inventory

    def win(self):
        pass  # TODO: implement

    def turnRight(self):
        if self.getDirection() == self.RIGHT:
            self.__direction = self.DOWN
        elif self.getDirection() == self.DOWN:
            self.__direction = self.LEFT
        elif self.getDirection() == self.LEFT:
            self.__direction = self.UP
        elif self.getDirection() == self.UP:
            self.__direction = self.RIGHT

    def turnLeft(self):
        if self.getDirection() == self.RIGHT:
            self.__direction = self.UP
        elif self.getDirection() == self.UP:
            self.__direction = self.LEFT
        elif self.getDirection() == self.LEFT:
            self.__direction = self.DOWN
        elif self.getDirection() == self.DOWN:
            self.__direction = self.RIGHT

    def turnAround(self):
        self.turnLeft()
        self.turnLeft()

    def move(self):
        """
        Move the hero forwards 1 cell in the direction he is facing
        :param cell:  the current cell the Agent is in
        :return:      the new cell the Agent moved to
        """
        self.__location = self.__getForwards()
        return self.__location

    def doNothing(self):
        """
        The agent does nothing
        This is for debugging and fail-safe purposes, and should never happen in a real run
        """
        return

    """
    Misc
    """

    def observe(self, cell):
        """
        Take a look at the environment and add it to agent's internal state
        Does not count as an action, as it is always performed every tick
        :param cell:  The cell the agent is currently in
        """
        # remember cell agent is standing in and mark it as traversed
        self.__state.remember(
            self.getLocation()['x'], self.getLocation()['y'], cell, beenTo=True)

        # remember cells the agent can see in front of itself
        seenCell = cell
        seenCellDirection = [0, 0]  # positive and negative x and y modifiers
        for i in range(self.getSightRange()):
            if self.getDirection() == self.UP:
                seenCell = seenCell.getCellUp()
                seenCellDirection[1] -= 1
            elif self.getDirection() == self.DOWN:
                seenCell = seenCell.getCellDown()
                seenCellDirection[1] += 1
            elif self.getDirection() == self.LEFT:
                seenCell = seenCell.getCellLeft()
                seenCellDirection[0] -= 1
            elif self.getDirection() == self.RIGHT:
                seenCell = seenCell.getCellRight()
                seenCellDirection[0] += 1

            if seenCell == None:  # reached end of grid
                break
            else:
                try:
                    self.__state.remember(self.getLocation()['x'] + seenCellDirection[0],
                                          self.getLocation()[
                        'y'] + seenCellDirection[1],
                        seenCell)
                except Exception as err:
                    print(seenCell)
                    raise(err)

    def canMove(self, cell):
        """
        Check if the agent can legally move forwards. Walls and grid edges prevent movement
        :param cell:  The cell the agent is currently in
        :return:      True if can move forwards, false if not
        """
        if self.getDirection() == self.UP and (cell.isWallUp() or cell.getCellUp() == None):
            return False
        elif self.getDirection() == self.DOWN and (cell.isWallDown() or cell.getCellDown() == None):
            return False
        elif self.getDirection() == self.LEFT and (cell.isWallLeft() or cell.getCellLeft() == None):
            return False
        elif self.getDirection() == self.RIGHT and (cell.isWallRight() or cell.getCellRight() == None):
            return False
        return True

    def seenAgents(self):
        """
        Determine if the agent can see another agent
        :return:  List of agents that are seen. Empty if sees none.
        """
        # TODO: implement this
        seenAgents = []
        return seenAgents


    """
    Private Methods
    """

    def __getForwards(self):
        """
        Get the coordinates of the cell directly in front of the Agent
        Does not check if coordinates exist on the grid
        :return:  the coordinates of the cell
        """
        if self.getDirection() == self.UP:
            return {'x': self.getLocation()['x'], 'y': self.getLocation()['y'] - 1}
        elif self.getDirection() == self.DOWN:
            return {'x': self.getLocation()['x'], 'y': self.getLocation()['y'] + 1}
        elif self.getDirection() == self.LEFT:
            return {'x': self.getLocation()['x'] - 1, 'y': self.getLocation()['y']}
        elif self.getDirection() == self.RIGHT:
            return {'x': self.getLocation()['x'] + 1, 'y': self.getLocation()['y']}
