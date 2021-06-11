import random

from agent import Agent


class Monster(Agent):

    def __init__(self, startingLocation, sightRange, width, height):
        super(Monster, self).__init__(
            startingLocation, sightRange, width, height)
        self.addAction(self.kill)

    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        validMoves = [self.turnLeft, self.turnRight, self.turnAround]
        cell = self.getState().getCellAt(
            self.getLocation()['x'], self.getLocation()['y'])

        if self.canMove(cell):
            validMoves.append(self.move)

        return validMoves

    def chooseAction(self):
        """
        Choose an action to perform
        :return:          the chosen action function
        """
        actionUtility = {}

        currentCell = self.getState().getCellAt(self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(self.getLocation()["x"], self.getLocation()["y"])

        # print()
        # print("AGENT AT " + str(self.getLocation()))
        # print("UP: " + str(self.getState().getCellLocation(surroundings[self.UP])))
        # print("DOWN: " + str(self.getState().getCellLocation(surroundings[self.DOWN])))
        # print("LEFT: " + str(self.getState().getCellLocation(surroundings[self.LEFT])))
        # print("RIGHT: " + str(self.getState().getCellLocation(surroundings[self.RIGHT])))
        #
        # print("Wall UP: " + str(currentCell.isWallUp()))
        # print("Wall DOWN: " + str(currentCell.isWallDown()))
        # print("Wall LEFT: " + str(currentCell.isWallLeft()))
        # print("Wall RIGHT: " + str(currentCell.isWallRight()))

        validActions = self.getValidActions(self.getActions())
        if len(validActions) == 0:
            return self.doNothing

        for action in validActions:
            actionUtility[action] = self._getUtility(action, self.getState())

        return max(actionUtility, key=actionUtility.get)

    """
    Actions
    """

    def kill(self):
        """
        Kill a targeted agent
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
            self.kill: 100,  # monster will always attack when able
            self.move: 50 if self.seenAgents() != [] else 1,  # prioritize moving towards target  # TODO:  ambush behavior
            self.turnLeft: 0,  # default value
            self.turnRight: 0,
            self.turnAround: 0
        }

        currentCell = self.getState().getCellAt(self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(self.getLocation()["x"], self.getLocation()["y"])

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
            # TODO: This is awful. Figure out some way to make this less messy
            if self.getState().isVisited(nextCellLocation["x"], nextCellLocation["y"]):
                # check if any neighboring cells are unvisited
                unvisitedNeighbors = False
                for direction in self.DIRECTIONS:
                    if direction != self.getDirection():
                        location = self.getState().getCellLocation(surroundings[direction])
                        if location != None:
                            if not self.getState().isVisited(location["x"], location["y"]):
                                # turn towards cell
                                unvisitedNeighbors = True
                                utility[self.turnDirections[(self.getDirection(), direction)]] = 3


                if unvisitedNeighbors == False:
                    # TODO: talk about what the agent should do if every cell around them has been visited.
                    pass







        # TODO: figure out how to incorporate actions such as "die". It wants to avoid things that lead to it, but "die" should always override other action choices

        return utility[action]
