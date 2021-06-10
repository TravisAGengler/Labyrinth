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
        validMoves = [self.turnLeft, self.turnRight]
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
            self.turnRight: 0,  # default value
            self.turnLeft: 0
        }

        currentCell = self.getState().getCellAt(self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(self.getLocation()["x"], self.getLocation()["y"])

        # agent prioritizes learning its surroundings over moving
        # TODO: figure out why these are never being called
        # check up
        if surroundings[self.UP] == None and not currentCell.isWallUp():
            if self.getDirection() == self.LEFT or self.getDirection() == self.DOWN:
                utility[self.turnRight] = 2
            elif self.getDirection() == self.RIGHT:
                utility[self.turnLeft] = 2
        # check down
        if surroundings[self.DOWN] == None and not currentCell.isWallDown():
            if self.getDirection() == self.LEFT or self.getDirection() == self.UP:
                utility[self.turnLeft] = 2
            elif self.getDirection() == self.RIGHT:
                utility[self.turnRight] = 2
        # check left
        if surroundings[self.LEFT] == None and not currentCell.isWallLeft():
            if self.getDirection() == self.UP or self.getDirection() == self.RIGHT:
                utility[self.turnLeft] = 2
            elif self.getDirection() == self.DOWN:
                utility[self.turnRight] = 2
        # check right
        if surroundings[self.RIGHT] == None and not currentCell.isWallRight():
            if self.getDirection() == self.UP or self.getDirection() == self.LEFT:
                utility[self.turnRight] = 2
            elif self.getDirection() == self.DOWN:
                utility[self.turnLeft] = 2

        # agent tries to not retread ground
        nextCell = surroundings[self.getDirection()]
        if nextCell != None:
            nextCellLocation = self.getState().getCellLocation(nextCell)




            # # TODO: This is awful. Figure out some way to make this less messy
            # if self.getState().isVisited(nextCellLocation["x"], nextCellLocation["y"]):
            #     # check if any neighboring cells are unvisited
            #     unvisitedNeighbors = False
            #     for direction in self.DIRECTIONS:
            #         if direction != self.getDirection():
            #             if surroundings[direction] != None:
            #                 location = self.getState().getCellLocation(surroundings[direction])
            #                 if not self.getState().isVisited(location["x"], location["y"]):
            #                     # turn towards cell
            #                     unvisitedNeighbors = True
            #                     # TODO: turn agent towards unvisited cell
            #     if unvisitedNeighbors == False:
            #         # TODO: talk about what the agent should do if every cell around them has been visited.
            #         # Currently, the agent just picks a random direction to move in, including not turning
            #         utility[self.turnRight] = random.choice([0, 1])
            #         utility[self.turnLeft] = random.choice([0, 1])
            #         pass







        # TODO: figure out how to incorporate actions such as "die". It wants to avoid things that lead to it, but "die" should always override other action choices

        return utility[action]
