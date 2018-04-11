# Simulateur de robots

## Maze file format

The simulator's maze is configured by a file wich has the following format :

5 5\n
0010 0110 0101 0101 0011\n
1110 1101 0011 0110 1011\n
1110 0001 1000 1010 1000\n
1110 0111 0111 1101 0011\n
1000 1000 1100 0001 1000\n
\n

The first line are the dimensions of the maze. (WIDTH, HEIGHT)

The next lines are the cells in the maze, separated with a single space,
and each line ends with a '\n'.
A cell is represented with a string of 4 zeros and ones. A 1 mean there is no wall,
a 0 mean there is a wall.
The walls are described in this order : UP, RIGHT, DOWN, LEFT


## Inputs

This simulator is meant to be used with a planner, connected with it via TCP.
The simulator receive a list of instructions from the planner, and execute them.
An instruction looks like "A RIGHT", or "B UP" with A, B the identifiers of the robots.


## Usage

`./simulator.py`




