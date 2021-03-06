import copy
import pickle
import time

from rng import labyrinthSeed, labyrinthSetSeedIdxs, LABYRINTH_SEED_IDXS
from gameState import Gamestate
from civilian import Civilian
from soldier import Soldier
from scientist import Scientist
from monster import Monster


class SimParams:
    """
    This allows us to configure the simulation
    """

    def __init__(self, width: int = 10, height: int = 10, seedIdxs=LABYRINTH_SEED_IDXS):
        self.__width = width
        self.__height = height
        self.__seedIdxs = seedIdxs

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getSeedIdxs(self):
        return self.__seedIdxs


class Run:
    states = []
    current_state: int = 0
    HUMAN_COUNT = 3

    def __init__(self, load_path: str = "", simParams: SimParams = SimParams()):
        if load_path:
            print(f"Loading run from \"{load_path}\"")
            self.__from_file(load_path)
        else:
            print(f"Simulating new run")
            self.__simulateRun(simParams)
        self.current_state = 0

    def __simulateRun(self, params: SimParams):
        # Set the seeds

        labyrinthSetSeedIdxs(params.getSeedIdxs())

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
                    elif action == agent.pickUp:
                        items = nextState.getCellAt(
                            agent.getLocation()['x'], agent.getLocation()['y']).getItemList()
                        if len(items):
                            item = items[0]
                            action(item)
                            nextState.getCellAt(agent.getLocation()['x'],
                                                agent.getLocation()['y']).removeItem(item)
                            # print(f"{agentName} picked up {item}")

                    # handle monster actions
                    elif isinstance(agent, Monster) and action == agent.kill:
                        targets = action()
                        # print(f"Monster killed {targets}")
                        for target in targets:
                            itemsDropped = target.die()
                            # remove target from grid
                            targetCell = nextState.getCellAt(target.getLocation()["x"],
                                                             target.getLocation()["y"])
                            nextState.removeAgent(target)
                            targetCell.removeAgent(target)
                            # Drop items in cell
                            for i in itemsDropped:
                                targetCell.addItem(i)
                    elif isinstance(agent, Monster) and action == agent.dashAttack:
                        # move the monster forwards
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).removeAgent(agent)
                        targets = action()
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).addAgent(agent)
                        # attack the target
                        for target in targets:
                            itemsDropped = target.die()
                            # remove target from grid
                            targetCell = nextState.getCellAt(target.getLocation()["x"],
                                                             target.getLocation()["y"])
                            nextState.removeAgent(target)
                            targetCell.removeAgent(target)
                            # Drop items in cell
                            for i in itemsDropped:
                                targetCell.addItem(i)
                    elif isinstance(agent, Monster) and action == agent.run:
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).removeAgent(agent)
                        action()
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).addAgent(agent)

                    # handle human actions
                    elif not isinstance(agent, Monster) and action == agent.shoot:
                        # See if the agent shot anyone
                        action()  # All this does is remove gun after use from inventory
                        # TRICKY: Hit checking needs to be handled at this level, since this is the true layout
                        agentPos = agent.getLocation()
                        d = agent.getDirection()
                        bulletPath = [agentPos]
                        if d == agent.UP:
                            wall = "WALL_UP"
                            def inLims(p): return p['y'] > 0
                            def transform(p): return {
                                'x': p['x'], 'y': p['y'] - 1}
                        elif d == agent.RIGHT:
                            wall = "WALL_RIGHT"
                            def inLims(p): return p['x'] < nextState.getWidth()

                            def transform(p): return {
                                'x': p['x'] + 1, 'y': p['y']}
                        elif d == agent.DOWN:
                            wall = "WALL_DOWN"

                            def inLims(
                                p): return p['y'] < nextState.getHeight()
                            def transform(p): return {
                                'x': p['x'], 'y': p['y'] + 1}
                        elif d == agent.LEFT:
                            wall = "WALL_LEFT"
                            def inLims(p): return p['x'] > 0
                            def transform(p): return {
                                'x': p['x'] - 1, 'y': p['y']}

                        bulletCell = nextState.getCellAt(
                            bulletPath[-1]['x'], bulletPath[-1]['y'])
                        while not getattr(bulletCell, wall) and inLims(bulletPath[-1]):
                            bulletPath.append(transform(bulletPath[-1]))
                            bulletCell = nextState.getCellAt(
                                bulletPath[-1]['x'], bulletPath[-1]['y'])

                        # This is a trick to make sure we dont shoot through walls, and also ourselves!
                        bulletPath = [p for p in bulletPath if p != agentPos]

                        for p in bulletPath:
                            targets = nextState.getCellAt(
                                p['x'], p['y']).getAgentList()
                            if len(targets):
                                # Just kill the first thing
                                target = targets[0]
                                targetCell = nextState.getCellAt(target.getLocation()["x"],
                                                                 target.getLocation()["y"])
                                nextState.removeAgent(target)
                                targetCell.removeAgent(target)
                                # TODO: For now, notify all agents that the monster is killed.
                                # Maybe come up with some way for agents to communicate? See a body?
                                for _, a in nextState.getAgents().items():
                                    a.learnOfMonsterDeath()
                                # print(f"{type(agent).__name__} killed {type(target).__name__}")

                    elif not isinstance(agent, Monster) and action == agent.win:
                        nextState.getCellAt(agent.getLocation()['x'],
                                            agent.getLocation()['y']).removeAgent(agent)
                        nextState.removeAgent(agent)
                        nextState.addEscapee(agent)
                    else:
                        action()

            hasMonster = len([a for a in nextState.getAgents().values()
                             if isinstance(a, Monster)]) > 0
            hasHumans = len([a for a in nextState.getAgents().values()
                             if not isinstance(a, Monster)]) > 0

            # if not hasHumans and len(nextState.getEscapees()) > 0:
            #     for escapee in nextState.getEscapees():
            #         # print(escapee.getName() + " escaped!")
            #         nextState.removeEscapee(escapee)
            #         nextState.addVictor(escapee)

            if not hasHumans and len(nextState.getVictors()) == 0:
                # print("Monster killed all humans!")
                m = list(nextState.getAgents().values())[0]
                nextState.addVictor(m)
                terminated = True
            if not hasHumans and len(nextState.getVictors()) > 0:
                # print("Some humans escaped!")
                # print("Monster survived.")
                pass
            if not hasHumans and len(nextState.getVictors()) == self.HUMAN_COUNT:
                # print("All humans escaped!")
                # print("Monster survived.")
                pass
            if not hasMonster:
                humans = list(nextState.getAgents().values())
                for h in humans:
                    nextState.addVictor(h)
                # print("Humans killed the monster!")
                terminated = True
            if len(self.states) + 1 >= roundLimit:
                # print(f"No winner after reaching round limit")
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

    def getStats(self):
        terminalState = self.states[-1]

        victors = [a.getName() for a in terminalState.getVictors()]
        escaped = [a.getName() for a in terminalState.getEscapees()]

        allAgents = [a for a in self.states[0].getAgents()]
        remaningAgents = [a for a in terminalState.getAgents()]

        killed = [
            a for a in allAgents if a not in victors and a not in escaped and a not in remaningAgents]

        nRounds = len(self.states)

        return nRounds, victors, escaped, killed
