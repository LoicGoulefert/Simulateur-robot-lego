# -*- coding: utf-8 -*-

""" """

#Libs
import curses
from curses import wrapper

#Others
from maze import *

stdscr = curses.initscr()

def main(stdscr):
    m = Maze('./mazes/m1.txt')
    
    
    #Testing curses    
    # useless with wrapper ?
    #curses.noecho()
    #curses.cbreak()
    #stdscr.keypad(True)

    #Maze in ASCII
    s = str(m)

    #Maze window
    begin_x = 1; begin_y = 1
    height = curses.LINES-10; width = curses.COLS-1
    maze_w = curses.newwin(height, width, begin_y, begin_x)
    maze_w.addstr(s)
    maze_w.refresh()

    #Shortcuts window
    begin_x = 0; begin_y = curses.LINES-2
    height = 10; width = curses.COLS-1
    bottom_w = curses.newwin(height, width, begin_y, begin_x)
    bottom_w.addstr("Q: Reculer d'une étape\t\tX: Quitter\nD: Avancer d'une étape\t\tR: Rafraîchir", curses.A_BOLD)
    bottom_w.refresh()

    while True:
        c = stdscr.getch()
        if c == ord('x'):
            break;
        elif c == ord('r'):
            m.maze[0][0].content = 'A'
            m.maze[4][4].content = 'X'
            m.maze[2][1].content = 'a'
            s = str(m)
            maze_w.clear()
            maze_w.addstr(s)
            maze_w.refresh()
    
    # useless with wrapper ?
    #curses.nocbreak()
    #stdscr.keypad(False)
    #curses.echo()
    #curses.endwin()

if __name__ == "__main__":
    wrapper(main)




