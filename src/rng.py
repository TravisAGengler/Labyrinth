import random


LABYRINTH_SEEDS = [365241,
                   543210,
                   976458,
                   111237,
                   666999]

LABYRINTH_SEED_IDXS = {
    'layout': 2,
    'monster': 3,
    'civilian': 2,
    'scientist': 0,
    'soldier': 1,
}


def labyrinthSeed(type):
    seedIdx = LABYRINTH_SEED_IDXS[type]
    seedIdx = seedIdx % len(LABYRINTH_SEEDS)
    # print(f"Using seed {type}: {seedIdx} : {LABYRINTH_SEEDS[seedIdx]}")
    random.seed(LABYRINTH_SEEDS[seedIdx])


def labyrinthSetSeedIdxs(seedIdxs):
    global LABYRINTH_SEED_IDXS
    # print(f"Setting seed idxs {seedIdxs}")
    LABYRINTH_SEED_IDXS = seedIdxs
