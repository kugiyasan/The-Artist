# AUTHOR: JULIEN ROBERT

import curses
import logging
import random  # Praise RNGesus
import re
import sys
import time

from cards_and_enemies import starter_draw_pile, flaw_pile, fight1pool, master, acolyteE, master1E, master2E, master3E
from fight import Fight
from utils import dialogs, Window


#! A lot of death should be handled by Player itself
class Player():
    # TODO be able to set the Player value and therefore load the game from this data
    def __init__(self):
        self.__HP = 20
        self.maxHP = 24
        self.discard_pile = []
        self.world = 1
        self.room = 0
        self.next_event = 5

        # Initial player's deck, will be modified after
        self.draw_pile = starter_draw_pile
        random.shuffle(self.draw_pile)  # initial shuffle

        # self.honor = 0

    @property
    def HP(self):
        return self.__HP

    @HP.setter
    def HP(self, value):
        self.__HP = min(value, self.maxHP)

        if self.__HP <= 0:
            window.print_double_line()
            window.smooth_print("\n".join(dialogs["death"]))
            window.print_double_line()
            window.user_input(dialogs["gameover"])
            exit()

    def draw_pile_pop(self):
        if len(self.draw_pile) == 0:
            if len(self.discard_pile) == 0:
                window.print_double_line()
                window.smooth_print("\n".join(dialogs["fight"]["no_card"]))
                window.print_double_line()
                window.user_input(dialogs["gameover"])
                exit()

            window.print_double_line()
            window.smooth_print("\n".join(dialogs["fight"]["reshuffle"]))
            window.print_double_line("\n")
            window.user_input(dialogs["pause"])

            self.draw_pile = self.discard_pile[:]
            self.discard_pile = []
            self.draw_pile.append(next(flaw_pile))
            random.shuffle(self.draw_pile)

        return self.draw_pile.pop()


def mainmenu():
    while True:
        window.stdscr.clear()
        window.print_double_line()
        window.smooth_print("\n".join(dialogs["title"]["warnings"]))
        window.print_double_line()
        #! need a width of 90, or the ASCII art will be destroyed
        window.smooth_print("\n".join(dialogs["title"]["asciiArt"]))
        window.print_double_line()

        startchoice = window.user_input(dialogs["title"]["prompt"])

        if startchoice in ("1", "2", "3", "4"):
            break

        window.print_double_line()
        window.smooth_print(dialogs["error"])
        window.print_double_line()
        window.user_input()

    if startchoice == "1":
        intro()
    elif startchoice == "2":
        raise NotImplementedError
        # Tutorial()
    elif startchoice == "3":
        raise NotImplementedError
        # Continue()
        # rose, lilac, daffodil...
    elif startchoice == "4":
        raise NotImplementedError
        # Credits()


def intro():
    window.stdscr.clear()
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["intro"]["text1"]))
    window.print_double_line()
    window.user_input(dialogs["pause"])
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["intro"]["text2"]))

    while True:
        window.smooth_print(dialogs["intro"]["question"])
        window.print_double_line()
        window.smooth_print("\n".join(dialogs["intro"]["choices"]))
        dest = window.user_input()
        if dest in ("1", "2"):
            break
        window.print_double_line()
        window.smooth_print(" Error: Invalid option selected.")
        window.print_double_line()
        
        # 11 should be calculated with \n
        y, x = window.stdscr.getyx()
        window.stdscr.move(y-11, x)

    if dest == "1":
        Monastery()
    else:  # dest == "2"
        Observatory()


def Monastery():
    window.stdscr.clear()
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["intro"]))
    window.print_double_line()
    window.user_input(dialogs["pause"])

    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["first_battle"]))
    window.print_double_line()

    for i in range(5):
        window.smooth_print(
            f"\n Paintings remaining before next event: \033[1;33;40m{player.next_event - player.room}\033[1;37;40m\n")
        window.user_input(dialogs["pause"])

        enemy = choose_opponent()
        fight = Fight(window, player, enemy)
        fight.fight()
        player.room += 1

        if i != 4:
            window.print_double_line()
            window.smooth_print("\n".join(dialogs["monastery"]["interlude1"]))
            window.print_double_line()

    EncounterAcolyte()
    player.room += 1
    player.next_event = 11

    for i in range(5):
        window.smooth_print(
            f"\n Paintings remaining before meeting the Master: \033[1;33;40m{player.next_event - player.room}\033[1;37;40m\n")
        window.user_input(dialogs["pause"])

        enemy = choose_opponent()
        fight = Fight(window, player, enemy)
        fight.fight()
        player.room += 1

        if i != 4:
            window.print_double_line()
            window.smooth_print("\n".join(dialogs["monastery"]["interlude2"]))
            window.print_double_line()

    Bossfight()
    ending()


def choose_opponent():
    window.stdscr.clear()
    random.shuffle(fight1pool)
    x = fight1pool[0]
    y = fight1pool[1]

    window.print_double_line()
    window.smooth_print(x.stats)
    window.smooth_print(x.reward.description)

    window.print_double_line()
    window.smooth_print(y.stats)
    window.smooth_print(y.reward.description)

    window.print_double_line()
    window.smooth_print("[1] " + x.name)
    window.smooth_print("[2] " + y.name)
    encount1 = window.user_input(
        "\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")

    if encount1 in ("1", "2"):
        encount1 = int(encount1) - 1
    else:
        window.print_double_line()
        window.smooth_print(
            " Error: Invalid option selected. Selecting random encounter...")
        encount1 = random.randint(0, 1)

    return fight1pool.pop(encount1)


def EncounterAcolyte():
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["acolyte"]["text1"]))
    window.print_double_line()

    plural_draw_pile = "s" if len(player.draw_pile) > 1 else ""

    window.smooth_print(
        f" Your current health is \033[1;33;40m{player.HP}\033[1;37;40m/\033[1;33;40m{player.maxHP}\033[1;37;40m.")
    window.smooth_print("[1] \033[1;32;40mBreathe\033[1;37;40m (Heal 5 HP)")
    window.smooth_print(
        "[2] \033[1;31;40mDraw\033[1;37;40m (Challenge the Acolyte)")
    window.smooth_print(
        f"[3] \033[1;36;40mReflect\033[1;37;40m (Shuffle your discard pile back into your draw pile without adding a \033[1;31;40mFlaw\033[1;37;40m, and forget up to 3 cards in your deck. You currently have \033[1;33;40m{len(player.draw_pile)} \033[1;37;40mcard{plural_draw_pile} remaining in your draw pile.)")
    window.print_double_line()
    eventchoice = window.user_input(
        " Please enter the number corresponding to your choice to proceed:\n")
    if eventchoice == "1":
        window.print_double_line()
        window.smooth_print(
            "\n".join(dialogs["monastery"]["acolyte"]["breathe"]))
        window.print_double_line()
        player.HP += 5
        window.smooth_print(
            f" You have gained 5 health points. Your current health is \033[1;33;40m{player.HP}\033[1;37;40m/\033[1;33;40m{player.maxHP}\033[1;37;40m.")
        window.user_input(dialogs["pause"])
    elif eventchoice == "2":
        fight = Fight(window, player, acolyteE)
        fight.fight()
    elif eventchoice == "3":
        player.draw_pile.extend(player.discard_pile)
        player.discard_pile = []

        forget_cards()
    else:
        window.print_double_line()
        window.smooth_print(
            "\n".join(dialogs["monastery"]["acolyte"]["hesitation"]))
        window.print_double_line()
        player.HP += 5
        window.smooth_print(
            f" You have gained 5 health points. Your current health is \033[1;33;40m{player.HP}\033[1;37;40m/\033[1;33;40m{player.maxHP}\033[1;37;40m.")
        window.user_input(dialogs["pause"])

    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["acolyte"]["ending"]))
    window.print_double_line()


def forget_cards():
    forget = 3
    choice = ""
    while choice != "exit" and forget > 0:
        window.smooth_print(
            "\033[1;34;40m\n As I listen to the bright red leaves hitting the soil, I lose myself in my thoughts.\033[1;37;40m")
        for card in player.draw_pile:
            window.smooth_print(card.description)

        plural = "s" if forget > 1 else ""
        choice = window.user_input(
            f"\n Type the name of the card you wish to forget. You may forget \033[1;33;40m{forget}\033[1;37;40m more card{plural}. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
        choice = choice.lower()

        for card in player.draw_pile:
            if choice == card.short_name:
                player.draw_pile.remove(card)
                if card.is_flaw and forget > 1:
                    forget -= 2
                else:
                    window.print_double_line()
                    window.smooth_print(
                        " Error: You do not have enough cards left to forget to select a \033[1;31;40mFlaw\033[1;37;40m!")
                    window.print_double_line()
                break
        else:
            window.print_double_line()
            window.smooth_print(
                " Error: Invalid card name selected. Please type the name of the card you wish to forget(ex: \"canvas\"). The card must be in your current hand (shown below).")
            window.print_double_line()

    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["acolyte"]["fight"]))
    window.print_double_line()
    player.room += 1
    window.user_input(dialogs["pause"])


def Bossfight():
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["boss1"]))
    window.print_double_line()
    window.user_input(dialogs["pause"])
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["boss2"]))
    window.print_double_line()
    window.user_input(" Press enter to open your sketchbook and FIGHT.\n")

    dialogs["fight"]["win"] = "\033[1;34;40m\n \"Excellent work, disciple! However, I am only getting started...\"\033[1;37;40m\n"
    dialogs["fight"]["abandon"] = "\033[1;34;40m \"Hmm, this is concerning. Perhaps you just weren't warmed up yet.\""
    fight = Fight(window, player, master1E)
    fight.fight()

    dialogs["fight"]["win"] = "\033[1;34;40m\n \"How splendid! It seems you are ready for your true ultimate trial.\"\033[1;37;40m\n"
    dialogs["fight"]["abandon"] = "\033[1;34;40m \"What is this? Gather your equipment, and prove that you are worthy of my teachings!\""
    fight = Fight(window, player, master2E)
    fight.fight()

    dialogs["fight"]["win"] = "\033[1;34;40m\n \"Absolutely outstanding! Please follow me inside the monastery, and we shall discuss about your performance.\"\033[1;37;40m\n"
    dialogs["fight"]["abandon"] = "\033[1;34;40m \"This final trial was intended to be difficult. I am disappointed, but not surprised. Follow me inside the monastery, and we shall discuss of your performance.\""
    fight = Fight(window, player, master3E)
    fight.fight()


def ending():
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["ending"]["text1"]))
    window.print_double_line()
    window.user_input(
        " Press enter to receive the results of your evaluation.\n")

    #! should keep track of honor during the bossfight
    honor = 3
    if honor < 0 or honor > 3:
        raise ValueError(
            "You're not supposed to have more than 3 honor points")

    window.print_double_line()
    window.smooth_print(
        "\n".join(dialogs["monastery"]["ending"][f"honor{honor}"]))
    window.print_double_line()

    #! The game will exit as soon as the player hits 0HP,
    #! so unless he'd abandoned, he won't see this message
    if honor == 0:
        window.user_input(
            " Game over. Press enter to terminate the program.\n")
        exit()
    elif honor != 1:
        player.discard_pile.append(master)

    window.user_input(dialogs["pause"])

    window.print_double_line()
    window.smooth_print("\n".join(dialogs["monastery"]["ending"]["text2"]))
    window.print_double_line()

    # this part should be in the world selection
    window.smooth_print("[1] \033[1;33;40m The Golden Hive\033[1;37;40m")
    window.smooth_print("[2] \033[1;35;40m The Theatre of Virtuosos")
    window.user_input(
        "\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")

    raise NotImplementedError


def Observatory():
    window.print_double_line()
    window.smooth_print("\n".join(dialogs["observatory"]))
    window.print_double_line()
    window.user_input(dialogs["pause"])
    raise NotImplementedError


def Hive():
    window.print_double_line()
    window.smooth_print(dialogs["hive"])
    window.print_double_line()
    window.user_input(dialogs["pause"])
    raise NotImplementedError


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(__file__ + ".log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    player = Player()

    def wrapped_main(stdscr):
        global window
        window = Window(stdscr)
        mainmenu()

    curses.wrapper(wrapped_main)
