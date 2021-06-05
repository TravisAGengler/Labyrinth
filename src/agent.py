from abc import ABC, abstractmethod
import random

from state import State


class Agent(ABC):

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, startingLocation):
        self.__location = startingLocation  # {'x': x, 'y', y}
        self.__state = State(memoryLoss=0)
        # TODO: possibly change this, will depend on how agents are spawned in
        self.__direction = random.choice(self.DIRECTIONS)
        self.__inventory = []
        self.__isAlive = True
        self.__score = 0

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

    """
    Misc
    """

    def seenAgents(self):
        """
        Determine if the agent can see another agent
        :return:  List of agents that are seen. Empty if sees none.
        """
        seenAgents = []
        return seenAgents

    def knowsSurroundings(self):
        """
        Determine if the Agent knows what is in every cell directly surrounding it
        :return:  True if it knows its surroundings, false if not
        """
        # TODO: check if all surrounding cells in state are not None
        pass

    """
    Private Methods
    """

    def __getForwards(self):
        """
        Get the coordinates of the cell directly in front of the Agent
        Does not check if move is legal
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
