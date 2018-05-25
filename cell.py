#! /usr/bin/python3

"""This module represent a cell of the maze.

A cell can have up to 4 walls, it can be occupied by a robot
or an objective. More details can be added, like a background color,
it's state, i.e "visited" in order to improve the visual aspect of the cell.
"""


class Cell:

    def __init__(self, walls):
        """Create a cell from a string.

        String format : 0010 , meaning:
            UP -> wall
            RIGHT -> wall
            DOWN -> no wall
            LEFT -> wall

        Parameters:
            walls: string, see format above
        """
        self.UP = walls[0] == '1'
        self.RIGHT = walls[1] == '1'
        self.DOWN = walls[2] == '1'
        self.LEFT = walls[3] == '1'
        # Content is used to store a robot, an objective or the exit
        # It can store more than 1 object, but only 2 are displayed maximum.
        self.content = []
