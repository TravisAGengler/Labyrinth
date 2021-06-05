from agent import Agent


class Monster(Agent):

    def __init__(self, startingLocation):
        super(Monster, self).__init__(startingLocation)
        self.addAction(self.kill)

    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """

        # TODO: check if cell in internal state has wall, instead of cell in absolute state
        # if agent runs into a wall, prevent him from moving forwards.
        # if self.getDirection() == self.UP and cell.isWallUp():
        #     return self.getLocation()
        # elif self.getDirection() == self.DOWN and cell.isWallDown():
        #     return self.getLocation()
        # elif self.getDirection() == self.LEFT and cell.isWallLeft():
        #     return self.getLocation()
        # elif self.getDirection() == self.RIGHT and cell.isWallRight():
        #     return self.getLocation()

        return [self.move]  # TODO: temp just for testing. needs to check for collisions, etc

    def chooseAction(self):
        """
        Choose an action to perform
        :return:          the chosen action function
        """
        actionUtility = {}
        for action in self.getValidActions(self.getActions()):
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
            # prioritize moving towards target  # TODO:  ambush behavior
            self.move: 50 if self.seenAgents() != [] else 1,
        }

        if not self.knowsSurroundings():
            # set value of turnLeft, turnRight to 2. Agent prioritizes knowing its environment over moving forwards.
            pass

        # TODO: figure out how to incorporate actions such as "die". It wants to avoid things that lead to it, but "die" should always override other action choices

        return utility[action]
