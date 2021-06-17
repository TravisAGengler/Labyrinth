#!/usr/bin/env python3

import argparse
import pygame
import sys
import random
import time

from inputManager import InputManager, InputEvent
from render import Renderer
from run import Run, SimParams
from rng import LABYRINTH_SEEDS


class LabyrinthArgs:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="labyrinth", description='Create, display and step through Labyrinth runs')
        parser.add_argument('-r', '--run', type=str, nargs='?',
                            default="", help='A previous run to display')
        parser.add_argument(
            '-s', '--stats', action='store_true', help='Run simulations and present stats before presenting a new run')
        args = vars(parser.parse_args())
        self.run_path = args['run']
        self.simulate = args['stats']


def terminate():
    pygame.quit()
    sys.exit()


def runSimulations():
    nSimulations = 20
    allStats = []
    for i in range(nSimulations):
        seedIdxMax = len(LABYRINTH_SEEDS)-1
        random.seed(time.time())
        simParams = SimParams(width=10, height=10, seedIdxs={
            # Random seed indexes for each run.
            # If we wanted, we could control for any one of these by making the index fixed
            'layout': random.randint(0, seedIdxMax),
            'monster': random.randint(0, seedIdxMax),
            'civilian': random.randint(0, seedIdxMax),
            'scientist': random.randint(0, seedIdxMax),
            'soldier': random.randint(0, seedIdxMax),
        })
        run = Run(simParams=simParams)
        stats = run.getStats()
        allStats.append(stats)

    # Aggrigate and report overall stats
    averageNRounds = sum([s[0] for s in allStats]) // nSimulations
    humanWinRate = sum([1 if 'monster' not in s[1]
                        and len(s[1]) else 0 for s in allStats]) / nSimulations
    monsterWinRate = sum(
        [1 if 'monster' in s[1] and len(s[1]) else 0 for s in allStats]) / nSimulations
    stalemateRate = sum(
        [1 if len(s[1]) == 0 else 0 for s in allStats]) / nSimulations
    civilianEscapeRate = sum(
        [1 if 'civilian' in s[2] else 0 for s in allStats]) / nSimulations
    civilianDeathRate = sum(
        [1 if 'civilian' in s[3] else 0 for s in allStats]) / nSimulations
    scientistEscapeRate = sum(
        [1 if 'scientist' in s[2] else 0 for s in allStats]) / nSimulations
    scientistDeathRate = sum(
        [1 if 'scientist' in s[3] else 0 for s in allStats]) / nSimulations
    soldierEscapeRate = sum(
        [1 if 'soldier' in s[2] else 0 for s in allStats]) / nSimulations
    soldierDeathRate = sum(
        [1 if 'soldier' in s[3] else 0 for s in allStats]) / nSimulations

    print("===Simulation Stats===")
    print(f"Avg number of rounds: \t{averageNRounds}")
    print(f"Human win rate: \t{humanWinRate:.2f}")
    print(f"Monster win rate: \t{monsterWinRate:.2f}")
    print(f"Stalemate rate: \t{stalemateRate:.2f}")
    print(f"Civilian escape rate: \t{civilianEscapeRate:.2f}")
    print(f"Civilian death rate: \t{civilianDeathRate:.2f}")
    print(f"Scientist escape rate: \t{scientistEscapeRate:.2f}")
    print(f"Scientist death rate: \t{scientistDeathRate:.2f}")
    print(f"Soldier escape rate: \t{soldierEscapeRate:.2f}")
    print(f"Soldier death rate: \t{soldierDeathRate:.2f}")


def main():
    args = LabyrinthArgs()

    if args.simulate:
        runSimulations()

    simParams = SimParams(width=10, height=10)
    run = Run(load_path=args.run_path) if args.run_path else Run(
        simParams=simParams)
    renderer = Renderer(windowWidth=800,
                        windowHeight=800,
                        nCellsHorizontal=simParams.getWidth(),
                        nCellsVertical=simParams.getHeight(),
                        fps=10)
    inputManager = InputManager()
    agents = run.getState().getAgents()

    autoStep = False
    audoStepRate = 25
    autoStepTicks = pygame.time.get_ticks()

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
        elif event == InputEvent.autoStep:
            autoStep = not autoStep
        elif event == InputEvent.restart:
            run.restart()

        if autoStep and pygame.time.get_ticks()-autoStepTicks >= audoStepRate:
            run.stepForward()
            autoStepTicks = pygame.time.get_ticks()

        renderer.draw(run.getState())


if __name__ == '__main__':
    main()
