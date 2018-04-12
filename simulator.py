#! /usr/bin/python3

""" """

#Libs
import curses
from curses import wrapper
import socket, _thread


#Others
from maze import Maze

# Main curses window init
stdscr = curses.initscr()

class Simulator:

	def __init__(self, path):
		self.maze = Maze(path)
		self.robots_coord = {} 		# Store the current robots coordinates to display them
		self.objectives_coord = {}  # Also stores the objectives but they are static (?)
		self.move_list = [] 		# Store the robots moves reveived from the planner
		self.move_history = [] 		# Store the moves made by the robots

	def update_coord(self, robot, move):
		ct = self.maze.cell_tab
		x, y = self.robots_coord[robot]
		#
		ct[x][y].content.remove(robot)

		if move == "UP": x -= 1
		elif move == "RIGHT": y += 1
		elif move == "DOWN": x += 1
		elif move == "LEFT": y -= 1
		else: print("update_coord(): Unknown move.")

		assert x >= 0 and y >= 0 and x < self.maze.height and y < self.maze.width, \
		"Illegal move. (x = {} y = {} move = {}".format(x, y, move)

		ct[x][y].content.append(robot)
		self.robots_coord[robot] = x, y

	def update_maze(self):
		""" Update the cells content in the maze"""
		for robot in self.robots_coord.keys():
			x, y = self.robots_coord[robot]
			self.maze.cell_tab[x][y].content.append(robot)

		for obj in self.objectives_coord.keys():
			x, y = self.objectives_coord[obj]
			self.maze.cell_tab[x][y].content.append(obj)

	def one_step_forward(self, window):
		"""Process the next move in the move_list.
		Remove that move from the move_list and
		add it to the move_history.
		Refresh the curses window when it's done."""
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
		Refresh the curses window when it's done."""
		if self.move_history != []:
			move = self.move_history.pop()
			self.move_list.insert(0, move)
			robot, move = reverse_move(move)
			window.addstr(move)
			self.update_coord(robot, move)
			ascii_maze = str(self.maze)
			window.clear()
			window.addstr(ascii_maze)
			window.refresh()



#***************************************************#

# Fonction de test sans TCP avec le plannif
def init_coord_moves(simu, robots_coord, moves):
	simu.robots_coord = robots_coord
	simu.move_list = moves


def reverse_move(move):
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

	while True:
		c = stdscr.getch()
		if c == ord('x'):
			break
		elif c == ord('d'):
			simulator.one_step_forward(maze_w)
		elif c == ord('q'):
			simulator.one_step_backward(maze_w)


#***************************************************#




#***************************************************#

if __name__ == "__main__":
	robots_coord = {}
	robots_coord['A'] = (0, 0)
	robots_coord['B'] = (4, 4)
	robots_coord['a'] = (1, 1)
	moves = ["A DOWN", "B UP", "A RIGHT", "B LEFT", "B UP", "A UP", "A RIGHT", 
	"B UP", "B RIGHT", "B UP", "B LEFT", "A RIGHT"]

	simu = Simulator('./mazes/m1.txt')
	init_coord_moves(simu, robots_coord, moves)
	simu.update_maze()

	wrapper(print_with_curses, simu)

