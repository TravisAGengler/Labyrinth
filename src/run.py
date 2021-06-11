import copy
import pickle
import time


from gameState import Gamestate
from civilian import Civilian
from soldier import Soldier
from scientist import Scientist
from monster import Monster

class SimParams:
    """
    This allows us to configure the simulation
    """

    def __init__(self, width: int = 10, height: int = 10, layout=None):
        self.__width = width
        self.__height = height
        self.__layout = layout

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getLayout(self):
        return self.__layout


class Run:
    states = []
    current_state: int = 0

    def __init__(self, load_path: str = "", simParams: SimParams = SimParams()):
        if load_path:
            print(f"Loading run from \"{load_path}\"")
            self.__from_file(load_path)
        else:
            print(f"Simulating new run")
            self.__simulateRun(simParams)
        self.current_state = 0

    def __simulateRun(self, params: SimParams):
        # TODO: Just generate the first 10 steps for now.
        # TODO: Add termination criteria later (No remaining humans, or humans escaped)
        roundLimit = 100
        terminated = False
        self.states = [
            Gamestate(width=params.getWidth(), height=params.getHeight(), layout=params.getLayout())]
        while len(self.states) < roundLimit and not terminated:
            nextState = copy.deepcopy(self.states[-1])

            for agent in nextState.getAgents().values():
                if agent.isAlive():
                    agent.observe(nextState.getCellAt(agent.getLocation()['x'],
                                                      agent.getLocation()['y']))
                    action = agent.chooseAction()
                    if action == agent.move:
                        # remove agent from old cell
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).removeAgent(agent)
                        # update agent's internal position
                        action()
                        # place agent in new cell
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).addAgent(agent)
                    elif isinstance(agent, Monster) and action == agent.kill:
                        targets = action()
                        for target in targets:
                            target.die()
                            # remove target from grid
                            targetCell = nextState.getCellAt(target.getLocation()["x"],
                                                             target.getLocation()["y"])
                            targetCell.removeAgent(target)
                    else:
                        # most actions can be handled with a general call like this
                        # specific cases, such as move (shown above), can be handled in their own blocks
                        action()

            self.states.append(nextState)

    def __from_file(self, file_path: str):
        with open(file_path, "rb") as f:
            self.states = pickle.load(f)

    def toFile(self):
        file_path = time.strftime("labyrinth_run_%m%d%Y_%H%M%S")
        print(f"Writing run to file \"{file_path}.pkl\"")
        with open(f"{file_path}.pkl", "wb") as f:
            pickle.dump(self.states, f)

    def stepForward(self):
        if self.current_state < len(self.states) - 1:
            self.current_state += 1
        print(f"Viewing state ({self.current_state + 1}/{len(self.states)})")
        # TODO: Perhaps add some kind of action log here? Would make debugging/explaining easier

    def stepBack(self):
        if self.current_state > 0:
            self.current_state -= 1
        print(f"Viewing state ({self.current_state + 1}/{len(self.states)})")

    def getState(self) -> Gamestate:
        return self.states[self.current_state]
