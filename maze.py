#! /usr/bin/python3

# Libs

# Others
from cell import Cell

"""This module represent the maze that is being simulated."""


class Maze:

    def __init__(self, configfile_path, bitvector):
        """Init the cell_tab attribute from the config file.
        Init the width and height of the maze.
        """
        self.cell_tab = list()
        # extraire bitvector de conf_list => à faire dans le simu
        # Donc ici j'ai le bitvector de allowed
        # j'en fait un tableau de string '0110'
        # init avec cell_tab pareil
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
