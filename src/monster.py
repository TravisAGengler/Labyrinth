from agent import Agent


class Monster(Agent):

    def __init__(self, startingLocation):
        super(Monster, self).__init__(startingLocation)
        self.addAction(self.kill)

    def findValidActions(self, actions):
        """
        Find which actions are valid to perform
        :param actions:  the list of all possible actions the agent can choose from
        :return:         the list of all valid actions the agent can choose from
        """
        pass

    def chooseAction(self, state):
        """
        Choose an action to perform
        :param state:     the known environment. What the agent remembers about its environment, and what it currently perceives
        :return:          the chosen action function
        """
        actionUtility = {}
        for action in self.getValidActions(self.getActions()):
            actionUtility[action] = self._getUtility(action, state)
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
        :param states:    the known environment.
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
