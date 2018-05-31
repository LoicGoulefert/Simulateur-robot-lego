#! /usr/bin/python3

# Libs

# Others
from cell import Cell

"""This module represent the maze that is being simulated."""


class Maze:

    def __init__(self, conf_list):
        """Init the cell_tab attribute from the conf_list
        received from the planner.
        Init the width and height of the maze.

        Parameters:
            conf_list: list of tuple of 'at' and 'allowed' preconditions
                       (ex : ['allowed', 'c-0-0', 'c-0-1'])
        """
        self.cell_tab = list()
        self.at_s, self.allowed_s = split_conf_list(conf_list)
        self.width, self.height = get_dimensions(self.allowed_s)
        for i in range(self.height):
            cell_line = list()
            for j in range(self.width):
                cell = build_cell_string(i, j, self.allowed_s)
                cell_line.append(Cell(cell))
            self.cell_tab.append(cell_line)

    def __str__(self):
        """Return maze table in ASCII.

        A cell can have more than 1 robot (or objective),
        but we display max. 2 objects per cell.
        """
        result = '.' + self.width * '___.'
        result += '\n'

        for line in self.cell_tab:
            result += '|'

            # First "line" of the line
            for cell in line:
                content = cell.content
                if content == [] or len(content) == 1:
                    result += '   '
                elif len(content) > 1:
                    result += ' {} '.format(content[1])
                if not cell.RIGHT:
                    result += '|'
                else:
                    result += ' '
            result += '\n|'

            # Seconde "line" of the line
            for cell in line:
                content = cell.content
                if not cell.DOWN:
                    if content == []:
                        result += '___'
                    else:
                        result += '_{}_'.format(content[0])
                elif content != []:
                    result += ' {} '.format(content[0])
                else:
                    result += '   '
                if not cell.RIGHT:
                    result += '|'
                else:
                    result += '.'

            result += '\n'
        return result


def split_conf_list(conf_list):
    """Split the conf_list into 2 sets : 1 set of 'at' preconditions,
    1 set of 'allowed' precondition.
    Set of tuples :
    - at_set : (i_in_conf_list, robot_name, x, y)
    - allowed_set : (i_in_conf_list, x1, y1, x2, y2)

    Parameters:
        conf_list: list of tuple of 'at' and 'allowed' preconditions
    """
    at_set = set()
    allowed_set = set()
    i = 0
    for t in conf_list:
        if t[0] == 'at':
            tmp = (i, t[1], *get_coord_from_cell(t[2]))
            at_set.add(tmp)
        else:
            tmp = (i, *get_coord_from_cell(t[1]), *get_coord_from_cell(t[2]))
            allowed_set.add(tmp)
        i += 1
    return at_set, allowed_set


def get_coord_from_cell(cell):
    """From a string representing a cell in pddl format,
    returns the x and y coordinates.

    Parameter:
        cell: a string representing a cell.
              ex : 'c-0-0'
    """
    coord = cell.split('-')
    x, y = int(coord[1]), int(coord[2])
    return x, y


def get_dimensions(allowed_set):
    """Return the width and height of a maze,
    according to the allowed preconditions.

    Parameters:
        allowed_set: set of tuple of 'allowed' preconditions
    """
    h = -1
    w = -1
    for e in allowed_set:
        h = max(h, e[1], e[3])
        w = max(w, e[2], e[4])
    return w+1, h+1


def build_cell_string(x, y, allowed_s):
    """Build a string representing the cell walls
    at coords. (x, y).

    Parameters:
        x, y: integers, coords of the cell
        allowed_s: set of allowed preconditions
    """
    tab = [0 for x in range(4)]
    res = ""
    subset = {e for e in allowed_s if e[1] == x and e[2] == y}
    for e in subset:
        if e[3] == x-1 and e[4] == y:  # UP
            tab[0] = 1
        elif e[3] == x and e[4] == y+1:  # RIGHT
            tab[1] = 1
        elif e[3] == x+1 and e[4] == y:  # DOWN
            tab[2] = 1
        elif e[3] == x and e[4] == y-1:  # LEFT
            tab[3] = 1
    for t in tab:
        res += str(t)
    return res
