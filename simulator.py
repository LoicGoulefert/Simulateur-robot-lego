#! /usr/bin/python3

""" """

# Libs
import curses
from curses import wrapper
import sys

# Others
from maze import Maze
import server


class Simulator:

    def __init__(self, path, robots_coord, obj, static_obj, moves):
        self.maze = Maze(path)
        self.robots_coord = robots_coord    # Current robots' coordinates
        self.objectives_coord = obj         # Objectives that can be collected
        self.static_obj_coord = static_obj  # Obj. that can't be collected
        self.move_list = moves              # Moves received from the planner
        self.collected_history = {}         # Coords of collected objectives
        self.step = 0

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
        if move == "UP":
            x -= 1
        elif move == "RIGHT":
            y += 1
        elif move == "DOWN":
            x += 1
        elif move == "LEFT":
            y -= 1
        else:
            print("update_coord(): Unknown move.")

        assert x >= 0 and y >= 0 \
            and x < self.maze.height and y < self.maze.width, \
            "Illegal move. (x = {} y = {} move = {})".format(x, y, move)

        # Update the cell content at the new coords
        ct[x][y].content.append(robot)
        self.robots_coord[robot] = x, y

    def one_step_forward(self, window):
        """Process the next move in the move_list.
        Refresh the curses window when it's done.
        """
        assert self.move_list != []
        move = self.move_list[self.step]
        self.step += 1
        temp = move.split(' ')
        robot, move = temp[0], temp[1]
        self.update_coord(robot, move)
        ascii_maze = str(self.maze)
        window.clear()
        window.addstr(ascii_maze)
        window.refresh()

    def one_step_backward(self, window):
        """Cancel the last move done.
        Refresh the curses window when it's done.
        """
        assert self.move_list != []
        self.step -= 1
        move = self.move_list[self.step]
        robot, move = reverse_move(move)
        self.update_coord(robot, move, forward=False)
        ascii_maze = str(self.maze)
        window.clear()
        window.addstr(ascii_maze)
        window.refresh()

    def can_move_forward(self):
        return self.step < len(self.move_list)

    def can_move_backward(self):
        return self.step > 0


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
    # Main curses window init
    stdscr = curses.initscr()
    curses.curs_set(0)  # Set cursor to invisible

    ascii_maze = str(simulator.maze)

    # Maze window
    begin_x = 4
    begin_y = 4
    height = curses.LINES-10
    width = curses.COLS-1
    maze_w = curses.newwin(height, width, begin_y, begin_x)
    try:
        maze_w.addstr(ascii_maze)
        maze_w.refresh()
    except curses.error:
        sys.exit()

    # Shortcuts window
    begin_x = 0
    begin_y = curses.LINES-2
    height = 10
    width = curses.COLS-1
    bottom_w = curses.newwin(height, width, begin_y, begin_x)
    bottom_w.addstr(
        "Q: Reculer d'une etape\t\tX: Quitter\nD: Avancer d'une etape\t\t",
        curses.A_BOLD)
    bottom_w.refresh()

    # The different actions possible
    while True:
        c = stdscr.getch()
        if c == ord('x'):
            break
        elif c == ord('d') and simulator.can_move_forward():
            simulator.one_step_forward(maze_w)
        elif c == ord('q') and simulator.can_move_backward():
            simulator.one_step_backward(maze_w)


def main():
    print("Configure server parameters :")
    IPAdr = input("IP : ")
    port = int(input("Port : "))
    print("Waiting for planner to connect...")
    objectives_coord, static_obj_coord, \
        robots_coord, move_list, config_file = server.start_server(IPAdr, port)
    simu = Simulator('./mazes/' + config_file,
                     robots_coord, objectives_coord,
                     static_obj_coord,
                     move_list)
    return simu


if __name__ == "__main__":
    simu = main()
    try:
        wrapper(print_with_curses, simu)
    except SystemExit:
        print("Curses error: Maze was too big for the terminal.")
