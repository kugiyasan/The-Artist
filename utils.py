import curses
import json
import logging
import re
import time

with open("dialogs.json") as jsonFile:
    dialogs = json.load(jsonFile)


class Window():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        y, x = self.stdscr.getmaxyx()
        if x < 80 or y < 24:
            raise Exception("The terminal should be at least of size 80x24, resize it to meet the requirements")

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def clear(self):
        self.stdscr.clear()

    def print_double_line(self, text=""):
        self.smooth_print("=" * 49 + text)

    def smooth_print(self, text=""):
        # e.g. 1;31;40m
        # 1 is for light color for fg, 31 is fg(red), 40 is bg(black)

        # even index are text, odd one are the ansi escape code
        text_and_ansi = re.split("(\x1b\\[(?:\\d|;)*m)", text)
        text_and_ansi.append("\n")
        color = 7

        # could optimize by only printing the odd
        for i in range(len(text_and_ansi)):            
            if re.match("^\033\\[(\\d|;)*m$", text_and_ansi[i]):
                m = text_and_ansi[i][2:-1]
                color = self.ansi_to_color_int(m)
                continue
            for c in text_and_ansi[i]:
                self.stdscr.addch(c, curses.color_pair(color) | curses.A_BOLD)
                self.stdscr.refresh()
                time.sleep(1/300)

            #! should handle overflow, either by clearing and writing, or scrolling the already written text
            # try:
                # self.stdscr.addstr(text_and_ansi[i], curses.color_pair(color) | curses.A_BOLD)
            # except:
            #     self.stdscr.clear()
            #     self.stdscr.addstr(
            #         text_and_ansi[i], curses.color_pair(color) | curses.A_BOLD)

        # self.stdscr.refresh()

    def ansi_to_color_int(self, ansi):
        # I was too lazy and this is a great patch
        if re.match("^1;3\d;40$", ansi):
            color = int(ansi[3])
            if color < 1 or color > 7:
                raise ValueError(
                    "The ANSI escape sequence should have a valid fg color")
            return color
        # elif ansi == "1;30;47":
        #     return 8
        return 8

    def user_input(self, text="") -> str:
        if len(text) > 0 and text[-1] == "\n":
            text = text[:-1]
        self.smooth_print(text)

        # curses.flushinp()

        curses.nocbreak()
        curses.echo()
        # inp = self.stdscr.getch()
        inp = self.stdscr.getstr().decode("utf-8")
        curses.noecho()
        curses.cbreak()
        
        # patch for windows, unix-like terminal are able to raise KeyboardInterrupt normally
        #          Ctrl+c, Ctrl+d, Ctrl+z
        if inp in ("\x03", "\x04", "\x1a"):
            raise KeyboardInterrupt

        logging.info(repr(inp))
        self.smooth_print()
        return inp
