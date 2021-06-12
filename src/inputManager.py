import pygame

from pygame.locals import *

from enum import Enum


class InputEvent(Enum):
    nextState = 1
    prevState = 2
    newRun = 3
    saveRun = 4
    terminate = 5
    autoStep = 6
    restart = 7


DEFAULT_INPUT_MAPPING = {
    K_ESCAPE: InputEvent.terminate,
    K_RIGHT: InputEvent.nextState,
    K_LEFT: InputEvent.prevState,
    K_s: InputEvent.saveRun,
    K_n: InputEvent.newRun,
    K_a: InputEvent.autoStep,
    K_r: InputEvent.restart}


class InputManager:
    """
    This turns pygame events into InputEvents that we can handle in the main loop
    """

    def __init__(self, inputMapping=DEFAULT_INPUT_MAPPING):
        self.__inputMapping = inputMapping

    def getInputEvent(self) -> InputEvent:
        for event in pygame.event.get():
            if event.type == QUIT:
                return InputEvent.terminate
            elif event.type == KEYDOWN:
                if event.key in self.__inputMapping:
                    return self.__inputMapping[event.key]
