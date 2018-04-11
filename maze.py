#! /usr/bin/python3

""" This module represent the maze that is being simulated. """

#Libs
import numpy as np

#Others
from cell import Cell


def build_cells_from_file(path):
    """Build a matrix of cells from the config file.
    Return a tuple containing width, height, matrix of cells"""
    
    f = open(path, 'r')
    
    # Get the dimension of the maze from file
    l = f.readline().split(' ')
    width, height = int(l[0]), int(l[1])
    
    cell_tab = np.empty((height, width), dtype=Cell)
    
    i, j = 0, 0
    
    # Read file in order to create the cell matrix
    for i in range(height):
        line = f.readline()
        l = line.strip('\n').split(' ')
        j = 0
        for cell in l:
            c = Cell(cell)
            cell_tab[i][j] = c
            j += 1
    
    f.close()
    
    return width, height, cell_tab


#***************************************************#

class Maze:

    def __init__(self, configfile_path):
        self.width, self.height, self.cell_tab = build_cells_from_file(configfile_path)	


    # TODO : Agrandir les cases, on part sur du 3x3 pour que ça soit plus clair
    def __str__(self):
        """Return maze table in ASCII"""
        result = '.' + self.width * '___.'
        result += '\n'

        for i in range(self.height):
            result += '|'

            for j in range(self.width):
                if i==self.height-1 or self.cell_tab[i][j].walls['DOWN']:
                    content = self.cell_tab[i][j].content
                    if content == ' ':
                        result += '___'
                    else:
                        result += '_{}_'.format(content)
                else:
                    result += ' {} '.format(self.cell_tab[i][j].content)
                if j==self.width-1 or self.cell_tab[i][j].walls['RIGHT']:
                    result += '|'
                else:
                    result += '.'
            result += '\n'
        return result      


    