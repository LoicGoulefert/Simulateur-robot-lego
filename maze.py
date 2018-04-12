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
		self.cell_tab = list()
		with open(configfile_path) as configfile:
			for line in configfile:
				cell_line = list()
				for cell in line.split(" "):
					cell_line.append(Cell(cell))
				
				self.cell_tab.append(cell_line)
		self.width = len(self.cell_tab[0])
		self.height = len(self.cell_tab)


	def __str__(self):
		"""Return maze table in ASCII.
		A cell can have more than 1 robot (or objective), but we display max. 2 objects per cell."""
		result = '.' + self.width * '___.'
		result += '\n'

		for i in range(self.height):
			result += '|'

			# First "line" of the line
			for j in range(self.width):
				content = self.cell_tab[i][j].content
				if content == [] or len(content) == 1:
					result += '   '
				elif len(content) > 1:
					result += ' {} '.format(content[1])
				if j==self.width-1 or self.cell_tab[i][j].walls['RIGHT']:
					result += '|'
				else:
					result += ' '
			result += '\n|'

			# Seconde "line" of the line
			for j in range(self.width):
				content = self.cell_tab[i][j].content
				if i==self.height-1 or self.cell_tab[i][j].walls['DOWN']:
					if content == []:
						result += '___'
					else:
						result += '_{}_'.format(content[0])
				elif content != []:
					result += ' {} '.format(self.cell_tab[i][j].content[0])
				else:
					result += '   '
				if j==self.width-1 or self.cell_tab[i][j].walls['RIGHT']:
					result += '|'
				else:
					result += '.'

			result += '\n'
		return result


