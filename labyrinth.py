#!/usr/bin/env python3

import argparse
import copy
import pickle
import pygame
import sys
import time

from pygame.locals import *
from enum import Enum

FPS = 10
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
CELLSIZE = 100
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
GRIDWIDTH = int(WINDOWWIDTH / CELLSIZE)
GRIDHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
WORLDROWS = GRIDHEIGHT
WORLDCOLS = GRIDWIDTH

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
DARKGREEN = (0, 155,   0)
DARKGRAY = (40,  40,  40)
BLUE = (0,   0, 255)
DARKBLUE = (0,   0, 155)
YELLOW = (255, 255,   0)
BGCOLOR = BLACK


class InputEvent(Enum):
    next_state = 1
    prev_state = 2
    new_run = 3
    save_run = 4


class Action(Enum):
    # TODO: Flesh this out. Need to enumerate all possible actions
    moveForward = 1


class Args:
    run_path: bool

    def __init__(self, run_path: str = ""):
        self.run_path = run_path


class Percep(Enum):
    # TODO: Flesh this out. Need to enumerate all possible perceps
    see = 1


class State:
    # TODO: Flesh this out. This represents an environment
    terminal: bool

    def __init__(self, terminal: bool = False):
        self.terminal = terminal


class Agent:
   # TODO: This will need to change, this is just a stub. Maybe even add subclasses for each agent type
    internal_model: State

    def __init__(self):
        self.internal_model = State()

    def __get_perceps(self, state: State) -> list[Percep]:
        return []

    def __get_action(self, perceps: list[Percep]) -> Action:
        return Action.moveForward

    def act_on_state(self, origState: State, action: Action) -> State:
        state = copy.deepcopy(origState)
        perceps = self.__get_perceps(state)
        action = self.__get_action(perceps)
        return state


class Run:
    states: list[State] = []
    current_state: int = 0

    def __init__(self, load_path: str = ""):
        if load_path:
            print(f"Loading run from \"{load_path}\"")
            self.__from_file(load_path)
        else:
            # TODO: Construct run here through a simulation
            print(f"Generating new run")
            self.states = [State(terminal=True)]
        self.current_state = 0

    def __from_file(self, file_path: str):
        with open(file_path, "rb") as f:
            self.states = pickle.load(f)

    def to_file(self, file_path: str):
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

    def get_state(self) -> State:
        return self.states[self.current_state]


def get_input_event():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate()
            if event.key == K_RIGHT:
                return InputEvent.next_state
            if event.key == K_LEFT:
                return InputEvent.prev_state
            if event.key == K_s:
                return InputEvent.save_run
            if event.key == K_n:
                return InputEvent.new_run


def terminate():
    pygame.quit()
    sys.exit()


def draw_and_advance(state: State):
    DISPLAYSURF.fill(BGCOLOR)
    draw_grid()
    draw_state(state)
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def draw_state(state: State):
    # TODO: When we flesh out the state, draw the state here
    pass


def draw_grid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


def run_labyrinth(args: Args):
    run = Run(load_path=args.run_path) if args.run_path else Run()

    while True:
        event = get_input_event()
        if event == InputEvent.next_state:
            run.step_forward()
        elif event == InputEvent.prev_state:
            run.step_back()
        elif event == InputEvent.save_run:
            run.to_file(time.strftime("labyrinth_run_%m%d%Y_%H%M%S"))
        elif event == InputEvent.new_run:
            run = Run()
        draw_and_advance(run.get_state())


def main():
    global FPSCLOCK, DISPLAYSURF

    args = parse_args()

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Labyrinth')

    run_labyrinth(args)


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog="labyrinth", description='Create, display and step through Labyrinth runs')
    parser.add_argument('-r', '--run', type=str, nargs='?',
                        default="", help='A previous run to display')
    args = vars(parser.parse_args())
    return Args(run_path=args['run'])


if __name__ == '__main__':
    main()
