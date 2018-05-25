# Simulateur de robots

## Inputs

This simulator is meant to be used with a planner, connected with it via TCP.
The simulator receive a list of instructions from the planner, and execute them.


## Usage

In a terminal, execute :
`./simulator.py`

This will launch the server, waiting for the planner's instructions

In an other terminal :
`./planner.py`

You can find the **planner** [here](https://github.com/LoicGoulefert/Planificateur-robot-lego).

