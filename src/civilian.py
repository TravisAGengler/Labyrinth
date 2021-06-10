from agent import Agent


class Civilian(Agent):

    def __init__(self, startingLocation, sightRange, width, height):
        super(Civilian, self).__init__(
            startingLocation, sightRange, width, height)

    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        validMoves = []
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

        for action in self.getValidActions(self.getActions()):
            actionUtility[action] = self._getUtility(action, self.getState())
        return max(actionUtility, key=actionUtility.get)

    """
    Actions
    """

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
            self.move: 100
        }

        return utility[action]
