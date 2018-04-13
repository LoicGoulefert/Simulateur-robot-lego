# Simulateur de robots

## Maze file format

The simulator's maze is configured by a file wich has the following format :

```
0010 0110 0101 0101 0011
1110 1101 0011 0101 1011
1110 0001 1000 1010 1000
1110 0111 0111 1101 0011
1000 1000 1100 0001 1000
```


Each line represent the cells in the maze, separated with a single space,
and ends with a '\n'.
A cell is represented with a string of 4 zeros and ones. A 1 mean there is no wall,
a 0 mean there is a wall.
The walls are described in this order : UP, RIGHT, DOWN, LEFT


## Inputs

This simulator is meant to be used with a planner, connected with it via TCP.
The simulator receive a list of instructions from the planner, and execute them.
An instruction looks like "A RIGHT", or "B UP" with A, B the identifiers of the robots.


## Usage

In a first terminal, execute :
`./simulator.py`

This will launch the server, waiting for the planner's instructions

In a second terminal :
`./client.py`

You can find the **client.py** script [here](https://github.com/LoicGoulefert/Planificateur-robot-lego) (work on progress)


