#!/usr/bin/env python3

import argparse
import pygame
import sys

from inputManager import InputManager, InputEvent
from render import Renderer
from run import Run, SimParams


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
    # TODO: Add the fixed layout here. Right now, our layout is hardcoded in gameState.py
    # We might even be able to derive width and height from the layout.
    # And if that is the case, SimParams is useless, just use layout
    simParams = SimParams(width=10, height=10, layout=None)
    run = Run(load_path=args.run_path) if args.run_path else Run(
        simParams=simParams)
    renderer = Renderer(windowWidth=800,
                        windowHeight=800,
                        nCellsHorizontal=simParams.getWidth(),
                        nCellsVertical=simParams.getHeight(),
                        fps=10)
    inputManager = InputManager()
    agents = run.getState().getAgents()

    # # let the agents initially observe the environment
    # for agent in agents.values():
    #     agent.observe(run.getState().getCellAt(agent.getLocation()['x'], agent.getLocation()['y']))

    while True:
        event = inputManager.getInputEvent()
        if event == InputEvent.terminate:
            terminate()
        elif event == InputEvent.nextState:
            run.stepForward()
        elif event == InputEvent.prevState:
            run.stepBack()
        elif event == InputEvent.saveRun:
            run.toFile()
        elif event == InputEvent.newRun:
            run = Run(simParams=simParams)
        renderer.draw(run.getState())


        # for agent in agents.values():
        #     if agent.isAlive():
        #         agent.observe(run.getState().getCellAt(agent.getLocation()['x'], agent.getLocation()['y']))
        #         action = agent.chooseAction()
        #         if action == agent.move:
        #             # remove agent from old cell
        #             run.getState().getCellAt(agent.getLocation()['x'], agent.getLocation()['y']).removeAgent(agent)
        #             # update agent's internal position
        #             action()
        #             # place agent in new cell
        #             run.getState().getCellAt(agent.getLocation()['x'], agent.getLocation()['y']).addAgent(agent)
        #         else:
        #             # most actions can be handled with a general call like this
        #             # specific cases, such as move (shown above), can be handled in their own blocks
        #             action()


if __name__ == '__main__':
    main()
