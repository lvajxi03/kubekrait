#!/usr/bin/env python3

"""
Krait UI Windows module
"""


import curses


class MainWindow:
    """
    Main window class
    """
    def __init__(self):
        """
        Default MainWindow constructor
        """
        self.window = curses.newwin(0, 0, 0, 0)

    def show(self):
        """
        Show the main window
        """
        self.window.box()
        self.window.addstr(1, 1, "Krait UI")
        self.window.refresh()


class AboutWindow:
    """
    About window class
    """
    def __init__(self):
        """
        Default About constructor
        """
        self.window = curses.newwin(10, 40, 5, 5)

    def show(self):
        """
        Show the about window
        """
        self.window.box()
        self.window.addstr(1, 1, "Krait UI - Version 1.0")
        self.window.refresh()