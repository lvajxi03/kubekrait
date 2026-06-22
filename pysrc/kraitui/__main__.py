#!/usr/bin/env python3

"""
Krait UI module
"""

import curses
from .ui import MainWindow


def main(stdscr):
    """
    Main function to run the Krait UI
    """
    curses.curs_set(0)  # Hide the cursor
    main_window = MainWindow()
    main_window.show()
    stdscr.getch()  # Wait for user input


if __name__ == "__main__":
    curses.wrapper(main)
