import random

from agent import Agent


class Monster(Agent):

    def __init__(self, startingLocation, sightRange, width, height, name):
        super(Monster, self).__init__(
            startingLocation, sightRange, width, height, name)
        self.addAction(self.kill)
        self.addAction(self.run)

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

        if self.__canAttack():
            validActions.append(self.kill)

        if self.__canDashAttack():
            validActions.append(self.dashAttack)

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

        # TODO: currently, the agent always turns Left at an intersection unless he's already been that way. Talk about possibly changing this. Introduce some degree of randomization?

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

        # TODO: discuss with group and choose between these two methods

        # if multiple actions tie for best utility, pick the first option
        # return max(actionUtility, key=actionUtility.get)

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

    def kill(self):
        """
        Kill targeted agent(s)
        :return:  The agent that was killed
        """
        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        agents = currentCell.getAgentList()
        # frontCell = self.__getFrontCell()
        # if frontCell:
        #     agents += frontCell.getAgentList()
        targets = []
        for agent in agents:
            if not isinstance(agent, Monster):
                targets.append(agent)
        for target in targets:
            print(self.getName() + " killed " + target.getName())
        return targets

    def dashAttack(self):
        """
        Move forwards and attack at the same time
        This prevents the agent from always being able to move out of the square of the monster before it can attack
        :return:  the agent that was killed
        """
        self.move()
        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        agents = currentCell.getAgentList()
        # frontCell = self.__getFrontCell()
        # if frontCell:
        #     agents += frontCell.getAgentList()
        targets = []
        for agent in agents:
            if not isinstance(agent, Monster):
                targets.append(agent)
        for target in targets:
            print(self.getName() + " killed " + target.getName())
        return targets

    def run(self):
        """
        Move two spaces in one action
        Called when chasing a target that does not seen the monster
        """
        self.move()
        self.move()

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
            self.dashAttack: 100,
            self.run: 0,
            # prioritize moving towards target  # TODO:  ambush behavior
            self.move: 10 if self.seenAgents() != [] else 1,
            self.turnLeft: 0,  # default value
            self.turnRight: 0,
            self.turnAround: 0
        }

        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        surroundings = self.getState().getKnownSurroundings(
            self.getLocation()["x"], self.getLocation()["y"])

        # ambush behavior
        targets = self.seenAgents()
        seen = False
        for target in targets:
            if self.__seenBy(target):
                seen = True
        if not seen:
            utility[self.run] = 15

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

    def __seenBy(self, target):
        """
        Check if if the monster's target is facing it
        :param target:  the target agent
        :return:        True if agent is facing them, False if not
        """
        if self.getDirection() == self.UP and target.getDirection() == self.DOWN:
            return True
        elif self.getDirection() == self.DOWN and target.getDirection() == self.UP:
            return True
        elif self.getDirection() == self.LEFT and target.getDirection() == self.RIGHT:
            return True
        elif self.getDirection() == self.RIGHT and target.getDirection() == self.LEFT:
            return True
        else:
            return False

    def __getFrontCell(self):
        currentCell = self.getState().getCellAt(
            self.getLocation()["x"], self.getLocation()["y"])
        # Also allow the monster to attack agents in the cell in front of it.
        frontCell = None
        if self.getDirection() == self.UP and not currentCell.isWallUp():
            frontCell = self.getState().getCellAt(
                self.getLocation()["x"], self.getLocation()["y"] - 1)
        if self.getDirection() == self.DOWN and not currentCell.isWallDown():
            frontCell = self.getState().getCellAt(
                self.getLocation()["x"], self.getLocation()["y"] + 1)
        if self.getDirection() == self.LEFT and not currentCell.isWallLeft():
            frontCell = self.getState().getCellAt(
                self.getLocation()["x"] - 1, self.getLocation()["y"])
        if self.getDirection() == self.RIGHT and not currentCell.isWallRight():
            frontCell = self.getState().getCellAt(
                self.getLocation()["x"] + 1, self.getLocation()["y"])
        return frontCell

    def __canAttack(self):
        currentCell = self.getState().getCellAt(self.getLocation()["x"],
                                                self.getLocation()["y"])
        return currentCell.getAgentList() != [self]

    def __canDashAttack(self):
        targetCell = self.__getFrontCell()
        if targetCell != None:
            return targetCell.getAgentList() != []
        else:
            return False
