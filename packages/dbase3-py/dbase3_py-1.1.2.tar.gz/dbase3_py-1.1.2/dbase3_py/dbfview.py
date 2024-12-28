import curses, os, sys
from functools import reduce
from dbase3 import DbaseFile

def show(stdscr, title, text):
    max_line_length = reduce(lambda x, y: max(x, len(y)), text, 0) + 2
    curses.cbreak()
    stdscr.keypad(True)

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Unselected text
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)   # Selected text
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE) # Title
    
    # Set default background color to blue
    stdscr.bkgd(' ', curses.color_pair(1))

    # Get the size of the screen
    height, width = stdscr.getmaxyx()
    # Display the title on the first line, centered
    # stdscr.addstr(0, max(0, (width - len(title)) // 2), title[:width - 1], curses.color_pair(3))
    stdscr.addstr(0, 0, title.center(width), curses.color_pair(3))
    stdscr.refresh()
        
    index = 0
    start_line = 0  # Line in the list where the visible window starts
    prev_index = -1
    prev_start_line = -1

    while True:
        stdscr.clear()

        # Calculate the number of visible lines, excluding the last row for the cursor
        visible_lines = height - 2

        # Adjust the start_line to ensure the cursor stays within the visible window
        if index < start_line:
            start_line = index
        elif index >= start_line + visible_lines:
            start_line = index - visible_lines + 1

        # Display the part of the list within the current view
        if start_line != prev_start_line or index != prev_index:
            stdscr.addstr(0, 0, title.center(width), curses.color_pair(3))
            for i, line in enumerate(text[start_line:start_line + visible_lines]):
                if start_line + i == index:
                    # stdscr.addstr(i, 0, line[:width - 1].rjust(max_line_length), curses.A_REVERSE)
                    stdscr.addstr(i + 1, 0, line[:width - 1].rjust(max_line_length), curses.color_pair(2))
                else:
                    # stdscr.addstr(i, 0, line[:width - 1].rjust(max_line_length))
                    stdscr.addstr(i + 1, 0, line[:width - 1].rjust(max_line_length), curses.color_pair(1))
            stdscr.refresh()

        # Update previous state
        prev_index = index
        prev_start_line = start_line

        key = stdscr.getch()

        # Handle key inputs
        if key == curses.KEY_UP and index > 0:
            index -= 1
        elif key == curses.KEY_DOWN and index < len(text) - 1:
            index += 1
        elif key == ord('q'):  # Quit on 'q'
            break

def main():
    # numlines = 30
    # if len(sys.argv) > 1 and sys.argv[1].isdigit():
    #     numlines = int(sys.argv[1]) 
    # text = [f"Line {i + 1}" for i in range(numlines)]
    # title = "Select a line"
    if len(sys.argv) < 2:
        print("Usage: python dbfview.py <filename.dbf>")
        sys.exit(1)
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        sys.exit(1)
    dbf = DbaseFile(filename)
    title = filename
    text = dbf.csv().split('\n')
    curses.wrapper(lambda stdscr: show(stdscr, title, text))


if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
