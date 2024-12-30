import curses

def select_item(options):
    def main(stdscr):
        # Enable mouse input
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        curses.curs_set(0)  # Hide the cursor

        selected_index = -1

        def draw_menu():
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            for idx, option in enumerate(options):
                x = w // 2 - len(option) // 2
                y = h // 2 - len(options) - 1 + (idx * 3)  # Add 2 newlines (3-row spacing)
                if idx == selected_index:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, option)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, option)
            stdscr.refresh()

        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        while True:
            draw_menu()
            key = stdscr.getch()

            if key == curses.KEY_MOUSE:
                _, mx, my, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON1_CLICKED:
                    h, w = stdscr.getmaxyx()
                    for idx, option in enumerate(options):
                        x = w // 2 - len(option) // 2
                        y = h // 2 - len(options) - 1 + (idx * 3)  # Add 2 newlines
                        if y == my and x <= mx <= x + len(option):
                            return options[idx]

    # Run the curses application
    return curses.wrapper(main)
