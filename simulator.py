#! /usr/bin/python3

""" """

#Libs
import curses
from curses import wrapper

#Others
from maze import Maze
from server import *

# Main curses window init (faudra le foutre autre part ça nique le terminal des fois)
stdscr = curses.initscr()

class Simulator:

	def __init__(self, path):
		self.maze = Maze(path)
		self.robots_coord = {} 		# Store the current robots coordinates to display them
		self.objectives_coord = {}  # Store the objectives that can be collected
		self.static_obj_coord = {}	# Store the objectives that can't be collected
		self.move_list = [] 		# Store the robots moves received from the planner
		self.move_history = [] 		# Store the moves made by the robots
		self.collected_history = {} # Store when and where a robot collected an objective

	def update_coord(self, robot, move, forward=True):
		"""This function is called at each step (forward or backward)
		It updates the robot's position, and the cell content if they are any
		collectable objectives on it.
		Parameter 'forward': true if we're stepping forward, false if backward.
		"""
		ct = self.maze.cell_tab
		x, y = self.robots_coord[robot]
		content = ct[x][y].content

		# We remove any objective after the robot went through
		# Because we assume an objective can't be on the exit cell
		if forward:
			for obj in self.objectives_coord.keys():
				if obj in content:
					content.remove(obj)
					self.collected_history[obj, robot] = x, y
		else:
			for obj in self.objectives_coord.keys():
				if (obj, robot) in self.collected_history:
					if self.collected_history[obj, robot] == (x, y):
						content.append(obj)

		# Remove the robot at the old coords
		ct[x][y].content.remove(robot)

		# Update x, y coords
		if move == "UP": x -= 1
		elif move == "RIGHT": y += 1
		elif move == "DOWN": x += 1
		elif move == "LEFT": y -= 1
		else: print("update_coord(): Unknown move.")

		assert x >= 0 and y >= 0 and x < self.maze.height and y < self.maze.width, \
		"Illegal move. (x = {} y = {} move = {})".format(x, y, move)
 
		#Update the cell content at the new coords
		ct[x][y].content.append(robot)
		self.robots_coord[robot] = x, y

	def update_maze(self):
		"""Update the cells content in the maze.
		Called once when initializing the simulation.
		"""
		ct = self.maze.cell_tab
		for robot in self.robots_coord.keys():
			x, y = self.robots_coord[robot]
			ct[x][y].content.append(robot)

		for obj in self.objectives_coord.keys():
			x, y = self.objectives_coord[obj]
			ct[x][y].content.append(obj)

		for obj in self.static_obj_coord.keys():
			x, y = self.static_obj_coord[obj]
			ct[x][y].content.append(obj)

	def one_step_forward(self, window):
		"""Process the next move in the move_list.
		Remove that move from the move_list and
		add it to the move_history.
		Refresh the curses window when it's done.
		"""
		if self.move_list != []:
			move = self.move_list.pop(0)
			self.move_history.append(move)
			temp = move.split(' ')
			robot, move = temp[0], temp[1]
			self.update_coord(robot, move)
			ascii_maze = str(self.maze)
			window.clear()
			window.addstr(ascii_maze)
			window.refresh()

	def one_step_backward(self, window):
		"""Cancel the last move done.
		Remove it from the move_history and add it to the move_list.
		Refresh the curses window when it's done.
		"""
		if self.move_history != []:
			move = self.move_history.pop()
			self.move_list.insert(0, move)
			robot, move = reverse_move(move)
			self.update_coord(robot, move, forward=False)
			ascii_maze = str(self.maze)
			window.clear()
			window.addstr(ascii_maze)
			window.refresh()


#***************************************************#


def init_simulator(simu, robots_coord, obj, static_obj, moves):
	"""Initialize the simulator's attributes."""
	simu.robots_coord = robots_coord
	simu.objectives_coord = obj
	simu.static_obj_coord = static_obj
	simu.move_list = moves

def reverse_move(move):
	"""Return the opposite direction of move.
	Useful for one_step_backward()
	"""
	temp = move.split(' ')
	rev_move = temp[1]
	if rev_move == "UP":
		rev_move = "DOWN"
	elif rev_move == "RIGHT":
		rev_move = "LEFT"
	elif rev_move == "DOWN":
		rev_move = "UP"
	elif rev_move == "LEFT":
		rev_move = "RIGHT"
	return temp[0], rev_move

def print_with_curses(stdscr, simulator):
	"""Draw the simulation in a pretty terminal."""
	simulator.robots_coord['A'] = (0, 0)
	simulator.maze.cell_tab[0][0].content[0] = 'A'

	ascii_maze = str(simulator.maze)

	#Maze window
	begin_x = 1; begin_y = 1
	height = curses.LINES-10; width = curses.COLS-1
	maze_w = curses.newwin(height, width, begin_y, begin_x)
	maze_w.addstr(ascii_maze)
	maze_w.refresh()

	#Shortcuts window
	begin_x = 0; begin_y = curses.LINES-2
	height = 10; width = curses.COLS-1
	bottom_w = curses.newwin(height, width, begin_y, begin_x)
	bottom_w.addstr("Q: Reculer d'une étape\t\tX: Quitter\nD: Avancer d'une étape\t\t", curses.A_BOLD)
	bottom_w.refresh()

	# The different actions possible
	while True:
		c = stdscr.getch()
		if c == ord('x'):
			break
		elif c == ord('d'):
			simulator.one_step_forward(maze_w)
		elif c == ord('q'):
			simulator.one_step_backward(maze_w)

#***************************************************#

if __name__ == "__main__":
	print("Waiting for planner to connect...")
	objectives_coord, static_obj_coord, robots_coord, move_list, config_file = start_server()
	simu = Simulator('./mazes/' + config_file)
	init_simulator(simu, robots_coord, objectives_coord, static_obj_coord, move_list)
	simu.update_maze()

	wrapper(print_with_curses, simu)

