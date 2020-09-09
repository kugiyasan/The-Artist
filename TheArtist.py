# AUTHOR: JULIEN ROBERT

import random  # Praise RNGesus
import re
import sys
import time

from cards_and_enemies import *
from fight import Fight
from utils import *


class Player():
    def __init__(self):
        self.__HP = 20
        self.maxHP = 24
        self.discard_pile = []
        self.world = 1
        self.room = 0
        self.next_event = 5

        # Initial player's deck, will be modified after
        self.draw_pile = [red, yellow, blue, dawn,
                          beginning, beginning] + [canvas] * 7
        random.shuffle(self.draw_pile)  # initial shuffle

        # honor = 0

    @property
    def HP(self):
        return self.__HP

    @HP.setter
    def HP(self, value):
        self.__HP = min(value, self.maxHP)

        if self.__HP <= 0:
            print("\n".join(dialogs["death"]))
            input(dialogs["gameover"])
            exit()


def mainmenu():
    while True:
        printLine()
        print("\n".join(dialogs["title"]["warnings"]))
        printLine()
        print("\n".join(dialogs["title"]["asciiArt"]))
        printLine()

        startchoice = input(dialogs["title"]["prompt"])

        if startchoice in ("1", "2", "3", "4"):
            break

        printLine()
        print(dialogs["error"])
        printLine()
        input()

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
    printLine()
    print("\n".join(dialogs["intro"]["text1"]))
    printLine()
    input(dialogs["pause"])
    printLine()
    print("\n".join(dialogs["intro"]["text2"]))

    while True:
        print(dialogs["intro"]["question"])
        printLine()
        print("\n".join(dialogs["intro"]["choices"]))
        dest = input()
        if dest in ("1", "2"):
            break
        printLine()
        print(" Error: Invalid option selected.")
        printLine()

    if dest == "1":
        Monastery()
    else:  # dest == "2"
        Observatory()


def Monastery():
    printLine()
    print("\n".join(dialogs["monastery"]["intro"]))
    printLine()
    input(dialogs["pause"])
    # EncounterM()

    printLine()
    print("\n".join(dialogs["monastery"]["first_battle"]))
    printLine()

    for i in range(5):
        print(
            f"\n Paintings remaining before next event: \033[1;33;40m{player.next_event - player.room}\033[1;37;40m\n")
        input(dialogs["pause"])

        enemy = choose_opponent()
        fight = Fight(player, enemy)
        fight.fight()
        player.room += 1

        if i != 4:
            printLine()
            print("\n".join(dialogs["monastery"]["interlude1"]))
            printLine()

    EncounterAcolyte()
    player.room += 1
    player.next_event = 11

    for i in range(5):
        print(
            f"\n Paintings remaining before meeting the Master: \033[1;33;40m{player.next_event - player.room}\033[1;37;40m\n")
        input(dialogs["pause"])

        enemy = choose_opponent()
        fight = Fight(player, enemy)
        fight.fight()
        player.room += 1

        if i != 4:
            printLine()
            print("\n".join(dialogs["monastery"]["interlude2"]))
            printLine()

    Bossfight()
    ending()


def choose_opponent():
    random.shuffle(fight1pool)
    x = fight1pool[0]
    y = fight1pool[1]

    printLine()
    print(x.stats)
    print(x.reward.description)

    printLine()
    print(y.stats)
    print(y.reward.description)

    printLine()
    print("[1] " + x.name)
    print("[2] " + y.name)
    encount1 = input(
        "\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")

    if encount1 in ("1", "2"):
        encount1 = int(encount1) - 1
    else:
        printLine()
        print(" Error: Invalid option selected. Selecting random encounter...")
        encount1 = random.randint(0, 1)

    return fight1pool.pop(encount1)


def EncounterAcolyte():
    printLine()
    print("\n".join(dialogs["monastery"]["acolyte"]["text1"]))
    printLine()

    plural_draw_pile = "s" if len(player.draw_pile) > 1 else ""

    print(
        f" Your current health is \033[1;33;40m{player.HP}\033[1;37;40m/\033[1;33;40m{player.maxHP}\033[1;37;40m.")
    print("[1] \033[1;32;40mBreathe\033[1;37;40m (Heal 5 HP)")
    print("[2] \033[1;31;40mDraw\033[1;37;40m (Challenge the Acolyte)")
    print(
        f"[3] \033[1;36;40mReflect\033[1;37;40m (Shuffle your discard pile back into your draw pile without adding a \033[1;31;40mFlaw\033[1;37;40m, and forget up to 3 cards in your deck. You currently have \033[1;33;40m{len(player.draw_pile)} \033[1;37;40mcard{plural_draw_pile} remaining in your draw pile.)")
    printLine()
    eventchoice = input(
        " Please enter the number corresponding to your choice to proceed:\n")
    if eventchoice == "1":
        printLine()
        print("\n".join(dialogs["monastery"]["acolyte"]["breathe"]))
        printLine()
        player.HP += 5
        print(
            f" You have gained 5 health points. Your current health is \033[1;33;40m{player.HP}\033[1;37;40m/\033[1;33;40m{player.maxHP}\033[1;37;40m.")
        input(dialogs["pause"])
    elif eventchoice == "2":
        fight = Fight(player, acolyteE)
        fight.fight()
    elif eventchoice == "3":
        player.draw_pile.extend(player.discard_pile)
        player.discard_pile = []

        forget = 3
        choice = ""
        while choice != "exit" and forget > 0:
            print(
                "\033[1;34;40m\n As I listen to the bright red leaves hitting the soil, I lose myself in my thoughts.\033[1;37;40m")
            for card in player.draw_pile:
                print(card.description)

            plural = "s" if forget > 1 else ""
            choice = input(
                f"\n Type the name of the card you wish to forget. You may forget \033[1;33;40m{forget}\033[1;37;40m more card{plural}. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
            choice = choice.lower()

            for card in player.draw_pile:
                if choice == card.short_name:
                    player.draw_pile.remove(card)
                    if card.is_flaw and forget > 1:
                        forget -= 2
                    else:
                        printLine()
                        print(
                            " Error: You do not have enough cards left to forget to select a \033[1;31;40mFlaw\033[1;37;40m!")
                        printLine()
                    break
            else:
                printLine()
                print(" Error: Invalid card name selected. Please type the name of the card you wish to forget(ex: \"canvas\"). The card must be in your current hand (shown below).")
                printLine()

        printLine()
        print("\n".join(dialogs["monastery"]["acolyte"]["fight"]))
        printLine()
        player.room += 1
        input(dialogs["pause"])
    else:
        printLine()
        print("\n".join(dialogs["monastery"]["acolyte"]["hesitation"]))
        printLine()
        player.HP += 5
        print(
            f" You have gained 5 health points. Your current health is \033[1;33;40m{player.HP}\033[1;37;40m/\033[1;33;40m{player.maxHP}\033[1;37;40m.")
        input(dialogs["pause"])

    printLine()
    print("\n".join(dialogs["monastery"]["acolyte"]["ending"]))
    printLine()


def Bossfight():
    printLine()
    print("\n".join(dialogs["monastery"]["boss1"]))
    printLine()
    input(dialogs["pause"])
    printLine()
    print("\n".join(dialogs["monastery"]["boss2"]))
    printLine()
    input(" Press enter to open your sketchbook and FIGHT.\n")

    dialogs["fight"]["win"] = "\033[1;34;40m\n \"Excellent work, disciple! However, I am only getting started...\"\033[1;37;40m"
    dialogs["fight"]["abandon"] = "\033[1;34;40m \"Hmm, this is concerning. Perhaps you just weren't warmed up yet.\""
    fight = Fight(player, master1)
    fight.fight()

    dialogs["fight"]["win"] = "\033[1;34;40m\n \"How splendid! It seems you are ready for your true ultimate trial.\"\033[1;37;40m"
    dialogs["fight"]["abandon"] = "\033[1;34;40m \"What is this? Gather your equipment, and prove that you are worthy of my teachings!\""
    fight = Fight(player, master2)
    fight.fight()

    dialogs["fight"]["win"] = "\033[1;34;40m\n \"Absolutely outstanding! Please follow me inside the monastery, and we shall discuss about your performance.\"\033[1;37;40m"
    dialogs["fight"]["abandon"] = "\033[1;34;40m \"This final trial was intended to be difficult. I am disappointed, but not surprised. Follow me inside the monastery, and we shall discuss of your performance.\""
    fight = Fight(player, master3)
    fight.fight()


def ending():
    printLine()
    print("\n".join(dialogs["monastery"]["ending"]["text1"]))
    printLine()
    input(" Press enter to receive the results of your evaluation.\n")

    #! should keep track of honor during the bossfight
    honor = 3
    if honor < 0 or honor > 3:
        raise GameError("You're not supposed to have more than 3 honor points")

    printLine()
    print("\n".join(dialogs["monastery"]["ending"][f"honor{honor}"]))
    printLine()
    if honor == 0:
        input(" Game over. Press enter to terminate the program.\n")
        exit()
    elif honor != 1:
        player.discard_pile.append(master)

    input(dialogs["pause"])

    printLine()
    print("\n".join(dialogs["monastery"]["ending"]["text1"]))
    printLine()

    # this part should be in the world selection
    print("[1] \033[1;33;40m The Golden Hive")
    print("\033[1;37;40m[2] \033[1;35;40m The Theatre of Virtuosos")
    dest1 = input(
        "\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")

    raise NotImplementedError


def Observatory():
    printLine()
    print("\n".join(dialogs["observatory"]))
    printLine()
    input(dialogs["pause"])
    raise NotImplementedError


def Hive():
    printLine()
    print(dialogs["hive"])
    printLine()
    input(dialogs["pause"])
    raise NotImplementedError


class GameError(Exception):
    pass


if __name__ == "__main__":
    player = Player()
    mainmenu()
