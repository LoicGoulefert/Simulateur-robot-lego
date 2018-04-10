# -*- coding: utf-8 -*-

import pickle
import numpy as np

test_maze = np.array([
        [[(0,1)], [(1,1), (0,2)], [(0,1), (0,3)], [(0,2), (0,4)], [(0,3), (1, 4)]],
        [[(0,0), (1,1), (2,0)], [(0,1), (1,2), (1,0)], [(1,1), (2,2)], [(1,4), (2,3)], [(0,4), (1,3), (2,4)]]
        [[(1,0), (2,1), (3,0)], [(2,0)], [(1,2)], [(1,3), (3,3)], [(1,4)]],
        [[(2,0), (3,1), (4,0)], [(4,1), (3,0)], [(3,3), (4,2), (3,1)], [()]]
        ])

def read_graph_from_file(path):
	"""
	Read a graph from a file and returns it.
	File format :
	width height
	vertice1 neighbour1 neighbour2
	vertice2 neighbour3 neighbour4 neighbour5
	...
	and ends with a newline (\n)

	A vertice is represented by its coordinates, ex : A1, B5...
	"""

	graph = {}
	f = open(path, 'r')

	# Get the dimension of the maze from file
	l = f.readline().split(' ')
	width, height = int(l[0]), int(l[1])

	# Read file in order to create the graph
	for line in f:
		l = line.strip('\n').split(' ')
		vertice, neighbours = l[0], l[1:]
		graph[vertice] = neighbours
	
	f.close()
	return width, height, graph




#***************************************************#

class Maze:

	def __init__(self, configfile_path):
		self.width, self.height, self.graph = read_graph_from_file(configfile_path)


	def __str__(self):
		"""Return maze table in ASCII"""

		result = '.' + self.width * '_.'
		result += '\n'

		for i in range(self.height):
			result += '|'

			for j in range(self.width):
				if i==self.height-1: # or self.maze[i][j][BOTTOMWALL]:
					result += '_'
				else:
					result += ' '
				if j==self.width-1: # or self.maze[i][j][RIGHTWALL]:
					result += '|'
				else:
					result += '.'

			result += '\n'

		return result



#***************************************************#

if __name__ == "__main__":

	path = './mazes/m1.txt'
	maze = Maze(path)
	print(maze)







