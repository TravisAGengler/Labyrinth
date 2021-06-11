Labyrinth multiagent system project

DONE
- Framework and fixed environment (3-5 days)
  - Actions
  - Perceps
  - Cell class
  - Agent classes
  - Fixed layout
  - Rendering
  - Runs (Serialize and load)

TODO
- Agent behavior (10-15 days)
  - Monster
  - Soldier
  - Scientist
  - Civilian
- Simulations and report (2-3 days)
  - Recordings
  - Presentation slides

Generating Runs:
- By default, when you run `labyrinth.py`, a Run will be generated. Press "n" to generate a new Run at any time
- Step forward through a run by pressing "right" and backward by pressing "left"
- Watch the console output, it will report which round in the Run you are currently viewing.

Saving and loading of Runs:
- Save a run by pressing "s". That will generate a timestamped .pkl in the direcory you ran from
- Load a run by running `labyrinth.py` with the `--run` option and point it to a previously saved .pkl
- Run `labyrinth.py --help` for more details