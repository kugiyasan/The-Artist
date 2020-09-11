import json
import re
import sys
import time

with open("dialogs.json") as jsonFile:
    dialogs = json.load(jsonFile)


def print_double_line(s=""):
    print("\u001b[1;37;40m" + "=" * 49 + str(s))


def smooth_print(value):
    # print(value)
    # return

    number_of_lines = value.count("\n")

    # just print if it's two line or half the letter aren't from the alphabet
    if number_of_lines < 2 or len(re.findall("[A-Za-z]", value)) < len(value) // 2:
        print(value)
        return

    sys.stdout.write("\n" * number_of_lines + "\033[A" * number_of_lines)

    for c in value:
        # sys.stdout.write(c)
        # sys.stdout.flush()
        print(c, end="")
        if re.match("[A-Za-z0-9]", c):
            time.sleep(0.01)

    sys.stdout.write("\n")

# def move (y, x):
#     print("\033[%d;%dH" % (y, x))


def user_input(text="") -> str:
    print(text)
    return input()
