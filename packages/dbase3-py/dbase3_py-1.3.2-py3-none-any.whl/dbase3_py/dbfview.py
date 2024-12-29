#!/usr/bin/env python3
#-*- coding: utf_8 -*-
# dbfview.py - A simple DBF file viewer using curses

import os, sys
if os.name == 'posix':
    import curses
elif os.name == 'nt':
    import unicurses as curses
else:
    print("Unsupported OS")
    sys.exit(1)

from functools import reduce
try:
    from dbase3_py.dbase3 import DbaseFile
except ImportError:
    from dbase3 import DbaseFile

def show(stdscr, title, subtitle, text):
    max_line_length = reduce(lambda x, y: max(x, len(y)), text, 0)
    curses.cbreak()
    stdscr.keypad(True)

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Unselected text
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)   # Selected text
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)  # Title
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)   # Subtitle

    # Hide the cursor
    curses.curs_set(0)

    # Set default background color to blue
    stdscr.bkgd(' ', curses.color_pair(1))

    # Draw the title and subtitle once
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, title[:width - 1].center(width), curses.color_pair(3))
    stdscr.addstr(1, 0, subtitle[:width - 1].ljust(width).rjust(len(subtitle)+1), curses.color_pair(4))

    index = 0
    start_line = 0  # Line in the list where the visible window starts
    prev_index = -1
    prev_start_line = -1

    while True:
        # Calculate the number of visible lines for scrolling, starting from the third line
        visible_lines = height - 2  # Leave the first 2 lines for the title and subtitle

        # Adjust the start_line to ensure the cursor stays within the visible window
        if index < start_line:
            start_line = index
        elif index >= start_line + visible_lines:
            start_line = index - visible_lines + 1

        # Only redraw lines if scrolling or index changes
        if start_line != prev_start_line or index != prev_index:
            # Redraw visible lines
            for i, line in enumerate(text[start_line:start_line + visible_lines]):
                # Calculate the screen line to draw on (offset by 2 for title and subtitle)
                screen_line = i + 2
                if start_line + i == index:
                    stdscr.addstr(screen_line, 0, line[:width - 1].rjust(max_line_length), curses.color_pair(2))
                else:
                    stdscr.addstr(screen_line, 0, line[:width - 1].rjust(max_line_length), curses.color_pair(1))

            # Update only changed parts of the screen
            curses.doupdate()

        # Update previous state
        prev_index = index
        prev_start_line = start_line

        # Wait for input
        key = stdscr.getch()

        # Handle key inputs
        if key == curses.KEY_UP and index > 0:
            index -= 1
        elif key == curses.KEY_DOWN and index < len(text) - 1:
            index += 1
        elif key == ord('q'):  # Quit on 'q'
            break

def main():
    if len(sys.argv) < 2:
        print("Usage: python dbfview.py <filename.dbf>")
        sys.exit(1)
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        sys.exit(1)
    dbf = DbaseFile(filename)
    title = f"{filename} - {dbf.header.records} records"
    text = dbf.csv().split('\n')
    subtitle = "Use arrow keys to scroll, 'q' to quit"
    curses.wrapper(lambda stdscr: show(stdscr, title, subtitle, text))


if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
