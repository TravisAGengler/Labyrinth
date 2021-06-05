#!/usr/bin/env python3

import argparse
import pygame
import sys

from inputManager import InputManager, InputEvent
from render import Renderer
from run import Run


class LabyrinthArgs:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="labyrinth", description='Create, display and step through Labyrinth runs')
        parser.add_argument('-r', '--run', type=str, nargs='?',
                            default="", help='A previous run to display')
        args = vars(parser.parse_args())
        self.run_path = args['run']


def terminate():
    pygame.quit()
    sys.exit()


def main():
    args = LabyrinthArgs()
    run = Run(load_path=args.run_path) if args.run_path else Run()
    renderer = Renderer(windowWidth=800,
                        windowHeight=800,
                        cellWidth=80,
                        cellHeight=80,
                        fps=10)
    inputManager = InputManager()
    agents = run.get_state().getAgents()

    while True:
        event = inputManager.getInputEvent()
        if event == InputEvent.terminate:
            terminate()
        elif event == InputEvent.nextState:
            run.step_forward()
        elif event == InputEvent.prevState:
            run.step_back()
        elif event == InputEvent.saveRun:
            run.to_file()
        elif event == InputEvent.newRun:
            run = Run()
        renderer.draw(run.get_state())

        for agent in agents.values():
            if agent.isAlive():
                action = agent.chooseAction()
                if action == agent.move:
                    # remove agent from old cell
                    run.get_state().getCellAt(agent.getLocation()['x'], agent.getLocation()['y']).removeAgent(agent)
                    # update agent's internal position
                    action()
                    # place agent in new cell
                    run.get_state().getCellAt(agent.getLocation()['x'], agent.getLocation()['y']).addAgent(agent)
                else:
                    # most actions can be handled with a general call like this
                    # specific cases, such as move (shown above), can be handled in their own blocks
                    action()





if __name__ == '__main__':
    main()
