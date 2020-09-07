import json
import re

from cards_and_enemies import *
# from cards_and_enemies import tiger
from utils import *


class Fight():
    def __init__(self, player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.hand = []
        self.inspiration = self.enemy.numberOfInsp

    @property
    def show_hand(self):
        cards = "\033[1;32;40m YOUR HAND:\033[1;37;40m\n"

        if len(self.hand) == 0:
            return cards + " You have no cards in your hand!"

        return cards + "\n".join(card.description for card in self.hand) + "\n"

    @property
    def hand_damage(self):
        return sum(card.attack for card in self.hand)

    def fight_info(self):
        text = f" Your current might is \033[1;31;40m{self.hand_damage}\033[1;37;40m/\033[1;31;40m{self.enemy.HP}\033[1;37;40m."
        text += f"\n Your current health is \033[1;33;40m{self.player.HP}\033[1;37;40m/\033[1;33;40m24\033[1;37;40m."

        plural_draw_pile = "s" if len(self.player.draw_pile) > 1 else ""
        plural_discard_pile = "s" if len(self.player.discard_pile) > 1 else ""

        text += f"\n You currently have \033[1;33;40m{len(self.player.draw_pile)} \033[1;37;40mcard{plural_draw_pile} remaining in your draw pile,"
        text += f" and \033[1;33;40m{len(self.player.discard_pile)} \033[1;37;40mcard{plural_discard_pile} remaining in your discard pile."

        if self.inspiration > 0:
            text += f"\n You have \033[1;32;40m{self.inspiration}\033[1;37;40m/\033[1;32;40m{self.enemy.numberOfInsp}\033[1;37;40m Inspiration remaining."
        else:
            text += "\n \033[1;31;40m⚠\033[1;37;40m You have spent all your Inspiration! You will lose \033[1;33;40m1\033[1;37;40m HP per additional card draw."

        return text + "\n"

    def user_move(self):
        choice = input(" Please type what you wish to do next:\n").lower()

        if choice in ("d", "draw"):
            self.draw_card()
        elif choice in ("a", "abandon"):
            self.abandon_battle()
        elif choice in self.hand:
            pass
        else:
            printLine()
            print(' Error: Invalid action selected. Please type "d" to draw a card, "a" to abandon this combat, or type the name of the card you wish to use.')

    def draw_card(self):
        if self.inspiration > 0:
            self.inspiration -= 1
        else:
            self.player.HP -= 1
            if self.player.HP <= 0:
                print("\n".join(dialogs["fight"]["death"]))
                input(dialogs["gameover"])
                exit()


        if len(self.player.draw_pile) == 0:
            print(dialogs["fight"]["reshuffle"])
            self.player.draw_pile = self.player.discard_pile[:]
            random.shuffle(self.player.draw_pile)

        self.hand.append(self.player.draw_pile.pop())

    def abandon_battle(self):
        difference = self.enemy.HP - self.hand_damage
        self.player.HP -= difference

        print(dialogs["fight"]["abandon"])
        print(f" You have lost {difference} health points. Your current health is {self.player.HP}.")
        input(dialogs["pause"])

        # TODO forget some card

    def fight(self):
        printLine()
        print("\033[1;34;40m" + self.enemy.desc)
        printLine()
        input(dialogs["pause"])

        while True:
            printLine()
            print(self.enemy.stats)
            print(self.enemy.reward.description)
            printLine()
            print(self.show_hand)

            if self.hand_damage >= self.enemy.HP:
                self.battle_won()
                return

            printLine()
            print()

            print(self.fight_info())

            self.user_move()

    def battle_won(self):
        print(dialogs["fight"]["win"].format(self.enemy.name))
        input(dialogs["pause"])
