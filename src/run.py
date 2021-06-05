
import pickle
import time


from gameState import Gamestate


class SimulationParams:
    """
    This allows us to configure how runs are generated
    """

    def __init__(self):
        # TODO: Allow customization of runs through these params
        pass


class Run:
    states: list[Gamestate] = []
    current_state: int = 0

    def __init__(self, load_path: str = "", params: SimulationParams = SimulationParams()):
        if load_path:
            print(f"Loading run from \"{load_path}\"")
            self.__from_file(load_path)
        else:
            # TODO: Construct run here through a simulation
            print(f"Generating new run")
            self.states = [Gamestate()]
        self.current_state = 0

    def __from_file(self, file_path: str):
        with open(file_path, "rb") as f:
            self.states = pickle.load(f)

    def to_file(self):
        file_path = time.strftime("labyrinth_run_%m%d%Y_%H%M%S")
        print(f"Writing run to file \"{file_path}.pkl\"")
        with open(f"{file_path}.pkl", "wb") as f:
            pickle.dump(self.states, f)

    def step_forward(self):
        if self.current_state < len(self.states) - 1:
            self.current_state += 1
        print(f"Viewing state ({self.current_state + 1}/{len(self.states)})")

    def step_back(self):
        if self.current_state > 0:
            self.current_state -= 1
        print(f"Viewing state ({self.current_state + 1}/{len(self.states)})")

    def get_state(self) -> Gamestate:
        return self.states[self.current_state]
