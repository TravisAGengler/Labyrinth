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

    def __init__(self, width: int = 10, height: int = 10):
        self.__width = width
        self.__height = height

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height


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
        roundLimit = 200
        terminated = False
        self.states = [
            Gamestate(width=params.getWidth(), height=params.getHeight())]
        while not terminated:
            nextState = copy.deepcopy(self.states[-1])

            for agentName, agent in nextState.getAgents().items():
                if agent.isAlive():
                    agent.observe(nextState.getCellAt(agent.getLocation()['x'],
                                                      agent.getLocation()['y']))
                    action = agent.chooseAction()
                    # handle actions all agents can make
                    if action == agent.move:
                        # remove agent from old cell
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).removeAgent(agent)
                        # update agent's internal position
                        action()
                        # place agent in new cell
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).addAgent(agent)
                    # handle monster actions
                    elif isinstance(agent, Monster) and action == agent.kill:
                        targets = action()
                        for target in targets:
                            itemsDropped = target.die()
                            # remove target from grid
                            targetCell = nextState.getCellAt(target.getLocation()["x"],
                                                             target.getLocation()["y"])
                            nextState.removeAgent(target)
                            targetCell.removeAgent(target)
                            # Drop items in cell
                            for i in itemsDropped:
                                # print(f"{target} dropped {i} on death")
                                targetCell.addItem(i)
                    elif isinstance(agent, Monster) and action == agent.run:
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).removeAgent(agent)
                        action()
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).addAgent(agent)
                    elif action == agent.pickUp:
                        items = nextState.getCellAt(
                            agent.getLocation()['x'], agent.getLocation()['y']).getItemList()
                        if len(items):
                            item = items[0]
                            action(item)
                            nextState.getCellAt(agent.getLocation()['x'],
                                                agent.getLocation()['y']).removeItem(item)
                            # print(f"{agentName} picked up {item}")
                    else:
                        action()

            hasMonster = len([a for a in nextState.getAgents().values()
                             if isinstance(a, Monster)]) > 0
            hasCivilians = len([a for a in nextState.getAgents().values()
                                if not isinstance(a, Monster)]) > 0
            if not hasCivilians:
                print("Monster wins!")
                terminated = True
            if not hasMonster:
                print("Humans win!")
                terminated = True
            if len(self.states) >= roundLimit:
                print(f"No winner after reaching round limit")
                terminated = True

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
            print(
                f"Viewing state ({self.current_state + 1}/{len(self.states)})")
            # TODO: Perhaps add some kind of action log here? Would make debugging/explaining easier

    def stepBack(self):
        if self.current_state > 0:
            self.current_state -= 1
            print(
                f"Viewing state ({self.current_state + 1}/{len(self.states)})")

    def restart(self):
        self.current_state = 0
        print(f"Viewing state ({self.current_state + 1}/{len(self.states)})")

    def getState(self) -> Gamestate:
        return self.states[self.current_state]
