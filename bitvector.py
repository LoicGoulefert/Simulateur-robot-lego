#! /usr/bin/python3

""" """

# Libs
from bitarray import bitarray

# Others


def get_bitvector(conf_list):
    """Return a bitvector build with the conf_list details.

    The bitvector has (number of cells)² bits. They represent the 'allowed'
    preconditions that are present in conf_list[0]'s list of tuples.

    +---+---+
    | X |   |
    +---+   + => 0 0 0 0 0 0 1 0 0 1 0 0 1 0 0 1
    |       |       'allowed' preconditions
    +---+---+

    Parameters:
        conf_list: tuple of (list*strings, int width, int height)

    """
    width = conf_list[1]
    height = conf_list[2]
    nb_cells = width * height
    res_bv = bitarray(nb_cells*nb_cells)
    res_bv.setall(False)

    for s in conf_list[0]:
        if s[0] == 'allowed':
            # Encoding 'allowed' states in bitvector
            c1 = get_index_of_cell(s[1], width)
            c2 = get_index_of_cell(s[2], width)
            index = c1*nb_cells + c2
            res_bv[index] = 1

    return res_bv


def get_index_of_cell(cell, width):
    """Returns the position of a cell in the maze.

    Parameters:
        cell: string representing a cell ('c-0-0')
        width: integer, the width of the maze
    """
    x, y = get_coord_from_cell(cell)
    return x*width + y


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


def get_cell_tab_from_bv(bv, width, heigth):
    # Create empty width * heigth matrix
    res = [[0 for x in range(width)] for y in range(heigth)]
    return res
