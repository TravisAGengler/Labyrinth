from agent import Agent


class Civilian(Agent):

    def __init__(self, startingLocation):
        super(Civilian, self).__init__(startingLocation)

    def findValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        pass

    def chooseAction(self, percepts):
        """
        Choose an action to perform
        :param percepts:  list of what the agent currently perceives
        :return:          the chosen action function
        """
        actionUtility = {}
        for action in self.getValidActions(self.getActions()):
            actionUtility[action] = self._getUtility(action, percepts)
        return max(actionUtility, key=actionUtility.get)

    """
    Actions
    """

    """
    Private Methods
    """

    def _getUtility(self, action, percepts):
        """
        Get the utility of a potential action
        :param action:    the action to determine the utility of
        :param percepts:  list of what the agent currently perceives
        :return:          the numerical utility of the action
        """
        pass
