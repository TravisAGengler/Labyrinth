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


if __name__ == '__main__':
    main()
