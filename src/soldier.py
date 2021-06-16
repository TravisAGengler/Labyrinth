import random

from agent import Agent
from item import Item
from monster import Monster


class Soldier(Agent):

    def __init__(self, startingLocation, sightRange, width, height, name):
        super(Soldier, self).__init__(
            startingLocation, sightRange, width, height, name)
        self.pickUp(Item.gun)

    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        validActions = [self.turnLeft, self.turnRight,
                        self.turnAround, self.flee]
        cell = self.getState().getCellAt(
            self.getLocation()['x'], self.getLocation()['y'])

        if self.canMove(cell):
            validActions.append(self.move)

        if len(cell.getItemList()):
            for item in cell.getItemList():
                if item is Item.keyCard:
                    validActions.append(self.pickUp)

        if Item.gun in self.getInventory() and self.seenAgents():
            validActions.append(self.shoot)

        if Item.keyCard in self.getInventory() and self.knowsMonsterIsDead() and cell.isExit:
            validActions.append(self.win)

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
        self.removeItem(Item.gun)

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
            self.move: 1,
            self.turnLeft: 0,  # default value
            self.turnRight: 0,
            self.turnAround: 0,
            self.pickUp: 0,
            self.shoot: 0,
            self.flee: 0,
        }

        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(
            self.getLocation()["x"], self.getLocation()["y"])

        # If agent has a gun, and agent sees (and is facing) the monster, prioritize shooting
        # Otherwise flee
        seen = self.seenAgents()
        for s in seen:
            if isinstance(s, Monster):
                if Item.gun in self.getInventory():
                    utility[self.shoot] = 100
                else:
                    utility[self.flee] = 100

        # agent will prioritize picking up items
        itemsNotHeld = [
            i for i in currentCell.getItemList() if i not in self.getInventory()]
        if len(itemsNotHeld):
            utility[self.pickUp] = 20

        # agent will prioritize moving towards items
        if len(self.seenItems()) != 0:
            utility[self.move] = 10

        # agent will move towards exit when it sees it and has the key
        if self.seesExit() and Item.keyCard in self.getInventory():
            utility[self.move] = 15

        # agent will exit when it has the key
        if currentCell.isExit:
            if Item.keyCard in self.getInventory():
                utility[self.win] = 50
            # agent will remember where it saw the exit if it cannot immediately exit
            else:
                self.getState().addBreadTrail(
                    self.getLocation()["x"], self.getLocation()["y"])

        # agent will head back for the exit when it has the key and knows where the exit is
        if Item.keyCard in self.getInventory() and self.isRememberingPath():
            nextCellLocation = self.getState().getActiveBreadTrail().getNextStep(self.getLocation()["x"],
                                                                                 self.getLocation()["y"])
            if nextCellLocation == None:
                self.getState().finishBreadTrail()
            else:
                nextCell = self.getState().getCellAt(
                    nextCellLocation["x"], nextCellLocation["y"])
                nextCellDirection = list(surroundings.keys())[list(
                    surroundings.values()).index(nextCell)]  # get key of value in dict
                if nextCellDirection == self.getDirection():
                    utility[self.move] = 10
                else:
                    utility[self.turnDirections[(
                        self.getDirection(), nextCellDirection)]] = 10

        # agent prioritizes learning its surroundings over moving ONLY if it is not fleeing
        if not self.isFleeing():
            # check up
            if self.getState().getCellLocation(surroundings[self.UP]) == None and not currentCell.isWallUp():
                utility[self.turnDirections[(
                    self.getDirection(), self.UP)]] = 2
            # check down
            if self.getState().getCellLocation(surroundings[self.DOWN]) == None and not currentCell.isWallDown():
                utility[self.turnDirections[(
                    self.getDirection(), self.DOWN)]] = 2
            # check left
            if self.getState().getCellLocation(surroundings[self.LEFT]) == None and not currentCell.isWallLeft():
                utility[self.turnDirections[(
                    self.getDirection(), self.LEFT)]] = 2
            # check right
            if self.getState().getCellLocation(surroundings[self.RIGHT]) == None and not currentCell.isWallRight():
                utility[self.turnDirections[(
                    self.getDirection(), self.RIGHT)]] = 2

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
