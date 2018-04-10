# -*- coding: utf-8 -*-

import pickle
import numpy as np


def build_cells_from_file(path):
    """Return a tuple containing width, height, matrix of cells"""
    
    f = open(path, 'r')
    
    # Get the dimension of the maze from file
    l = f.readline().split(' ')
    width, height = int(l[0]), int(l[1])
    
    cell_tab = np.empty((width, height), dtype=Cell)
    
    i, j = 0, 0
    
    # Read file in order to create the cell matrix
    for line in f:
        j = 0
        l = line.strip('\n').split(' ')
        for cell in l:
            c = Cell(cell)
            cell_tab[i][j] = c
            j += 1
        i += 1
    
    f.close()
    
    return width, height, cell_tab
    

#***************************************************#

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
        

def test_cell(walls):
    cell = Cell(walls)
    print(cell.walls)

#***************************************************#

class Maze:

	def __init__(self, configfile_path):
		self.width, self.height, self.maze = build_cells_from_file(configfile_path)


	def __str__(self):
		"""Return maze table in ASCII"""

		result = '.' + self.width * '_.'
		result += '\n'

		for i in range(self.height):
			result += '|'

			for j in range(self.width):
				if i==self.height-1 or self.maze[i][j].walls['DOWN']:
					result += '_'
				else:
					result += ' '
				if j==self.width-1 or self.maze[i][j].walls['RIGHT']:
					result += '|'
				else:
					result += '.'

			result += '\n'

		return result


#***************************************************#

if __name__ == "__main__":
    maze = Maze('./mazes/m1.txt')
    print(maze)
    
    


