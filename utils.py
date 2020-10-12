import json
import logging
import re
import sys
import time

with open("dialogs.json") as jsonFile:
    dialogs = json.load(jsonFile)


class Window():
    def clear(self):
        """Method specific to the curses branch"""
        pass

    def print_double_line(self, text=""):
        self.smooth_print("=" * 49 + text)

    def smooth_print(self, text=""):
        number_of_lines = text.count("\n")

        # just print if it's two line or half the letter aren't from the alphabet
        if number_of_lines < 2 or len(re.findall("[A-Za-z]", text)) < len(text) // 2:
            print(text)
            return

        sys.stdout.write("\n" * number_of_lines + "\033[A" * number_of_lines)

        for c in text:
            sys.stdout.write(c)
            sys.stdout.flush()
            # print(c, end="")
            if re.match("[A-Za-z0-9]", c):
                time.sleep(0.01)
        
        print()

    def user_input(self, text="") -> str:
        return input(text + "\n")
