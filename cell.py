#! /usr/bin/python3

""" This module represent a cell of the maze.
A cell can have up to 4 walls, it can be occupied by a robot, 
an objective or the exit.
More details can be added, like a background color, it's state, 
i.e "visited"... """

class Cell:
    def __init__(self, walls):
        """Init a cell with the string walls.
        String format : 0010 , meaning: 
            UP -> wall
            RIGHT -> wall
            DOWN -> no wall
            LEFT -> wall"""
        self.walls = {}
        self.walls['UP'] = walls[0] == '0'
        self.walls['RIGHT'] = walls[1] == '0'
        self.walls['DOWN'] = walls[2] == '0'
        self.walls['LEFT'] = walls[3] == '0'
        # Content is used to store a robot, an objective or the exit
        # Content can store more than 1 object
        self.content = []
        

