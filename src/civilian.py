from agent import Agent


class Civilian(Agent):

    def __init__(self, startingLocation):
        super(Civilian, self).__init__(startingLocation)

    def getValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
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

        if not self.knowsSurroundings():
            # set value of turnLeft, turnRight to 2. Agent prioritizes knowing its environment over moving forwards.
            pass

        return utility[action]
