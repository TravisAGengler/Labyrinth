import random

from agent import Agent


class Soldier(Agent):

    def __init__(self, startingLocation, sightRange, width, height, name):
        super(Soldier, self).__init__(
            startingLocation, sightRange, width, height, name)
        self.addAction(self.shoot)

    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        validActions = [self.turnLeft, self.turnRight, self.turnAround]
        cell = self.getState().getCellAt(
            self.getLocation()['x'], self.getLocation()['y'])

        if self.canMove(cell):
            validActions.append(self.move)

        if len(cell.getItemList()) > 0:
            validActions.append(self.pickUp)

        return validActions

    def chooseAction(self):
        """
        Choose an action to perform
        :return:          the chosen action function
        """
        actionUtility = {}

        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(
            self.getLocation()["x"], self.getLocation()["y"])

        validActions = self.getValidActions(self.getActions())
        if len(validActions) == 0:
            return self.doNothing

        for action in validActions:
            actionUtility[action] = self._getUtility(action, self.getState())

        # if multiple actions tie for best utility, pick randomly between them
        maxUtility = actionUtility[max(actionUtility, key=actionUtility.get)]
        maxActions = []
        for action in actionUtility.keys():
            if actionUtility[action] == maxUtility:
                maxActions.append(action)
        return random.choice(maxActions)

    """
    Actions
    """

    def shoot(self):
        """
        Shoot gun in a direction
        :return:
        """
        pass

    """
    Private Methods
    """

    def _getUtility(self, action, state):
        """
        Get the utility of a potential action
        :param action:    the action to determine the utility of
        :param state:    the known environment.
        :return:          the numerical utility of the action
        """
        utility = {
            self.move: 10,
            self.turnLeft: 0,  # default value
            self.turnRight: 0,
            self.turnAround: 0,
            self.pickUp: 0
        }

        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(
            self.getLocation()["x"], self.getLocation()["y"])

        # agent will prioritize picking up items
        if len(currentCell.getItemList()):
            utility[self.pickUp] = 20

        # agent prioritizes learning its surroundings over moving
        # check up
        if self.getState().getCellLocation(surroundings[self.UP]) == None and not currentCell.isWallUp():
            utility[self.turnDirections[(self.getDirection(), self.UP)]] = 2
        # check down
        if self.getState().getCellLocation(surroundings[self.DOWN]) == None and not currentCell.isWallDown():
            utility[self.turnDirections[(self.getDirection(), self.DOWN)]] = 2
        # check left
        if self.getState().getCellLocation(surroundings[self.LEFT]) == None and not currentCell.isWallLeft():
            utility[self.turnDirections[(self.getDirection(), self.LEFT)]] = 2
        # check right
        if self.getState().getCellLocation(surroundings[self.RIGHT]) == None and not currentCell.isWallRight():
            utility[self.turnDirections[(self.getDirection(), self.RIGHT)]] = 2

        # agent tries to not retread ground
        nextCell = surroundings[self.getDirection()]
        nextCellLocation = self.getState().getCellLocation(nextCell)
        if nextCellLocation != None:
            # TODO: This is kinda ugly. Figure out some way to make this less messy
            if self.getState().isVisited(nextCellLocation["x"], nextCellLocation["y"]):
                # check if any neighboring cells are unvisited
                unvisitedNeighbors = False
                for direction in self.DIRECTIONS:
                    if direction != self.getDirection():
                        location = self.getState().getCellLocation(
                            surroundings[direction])
                        if location != None:
                            if not self.getState().isVisited(location["x"], location["y"]):
                                # turn towards cell
                                unvisitedNeighbors = True
                                utility[self.turnDirections[(
                                    self.getDirection(), direction)]] = 3

                if unvisitedNeighbors == False:
                    # TODO: talk about what the agent should do if every cell around them has been visited.
                    # Right now, the agent simply resets its visited cells
                    self.getState().resetVisitedCells()

        return utility[action]
