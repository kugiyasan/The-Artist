import json
import re

from cards_and_enemies import *
from utils import *


class Fight():
    def __init__(self, player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.hand = []
        self.inspiration = self.enemy.number_of_insp
        self.hand_damage = 0
        self.win = False

    def show_hand(self):
        cards = "\033[1;32;40m YOUR HAND:\033[1;37;40m\n"

        if len(self.hand) == 0:
            return cards + " You have no cards in your hand!"

        return cards + "\n".join(card.description for card in self.hand)

    def fight_info(self):
        text = f" Your current might is \033[1;31;40m{self.hand_damage}\033[1;37;40m/\033[1;31;40m{self.enemy.HP}\033[1;37;40m."
        text += f"\n Your current health is \033[1;33;40m{self.player.HP}\033[1;37;40m/\033[1;33;40m{self.player.maxHP}\033[1;37;40m."

        plural_draw_pile = "s" if len(self.player.draw_pile) > 1 else ""
        plural_discard_pile = "s" if len(self.player.discard_pile) > 1 else ""

        text += f"\n You currently have \033[1;33;40m{len(self.player.draw_pile)} \033[1;37;40mcard{plural_draw_pile} remaining in your draw pile,"
        text += f" and \033[1;33;40m{len(self.player.discard_pile)} \033[1;37;40mcard{plural_discard_pile} remaining in your discard pile."

        if self.inspiration > 0:
            text += f"\n You have \033[1;32;40m{self.inspiration}\033[1;37;40m/\033[1;32;40m{self.enemy.number_of_insp}\033[1;37;40m Inspiration remaining."
        else:
            text += "\n \033[1;31;40m⚠\033[1;37;40m You have spent all your Inspiration! You will lose \033[1;33;40m1\033[1;37;40m HP per additional card draw."

        return text + "\n"

    def user_move(self) -> bool:
        """Returns True if the fight is over"""
        choice = input(" Please type what you wish to do next:\n").lower()

        if choice in ("d", "draw"):
            self.draw_card()
            return
        elif choice in ("a", "abandon"):
            self.abandon_battle()
            return True

        for card in self.hand:
            if choice == card.short_name:
                card.use_card(self, self.player, self.enemy)
                return

        printLine()
        print(' Error: Invalid action selected. Please type "d" to draw a card, "a" to abandon this combat, or type the name of the card you wish to use.')

    def draw_card(self):
        """
        This is the conventionnal way to draw a card,
        use self._draw_card if you don't want to pay inspiration points
        """
        if self.inspiration > 0:
            self.inspiration -= 1
        else:
            self.player.HP -= 1
            if self.player.HP <= 0:
                print("\n".join(dialogs["fight"]["death"]))
                input(dialogs["gameover"])
                exit()

        self._draw_card()

    def _draw_card(self):
        if len(self.player.draw_pile) == 0:
            if len(self.player.discard_pile) == 0:
                print("\n".join(dialogs["fight"]["no_card"]))
                input(dialogs["gameover"])
                exit()

            printLine()
            print("\n".join(dialogs["fight"]["reshuffle"]))
            printLine("\n")
            input(dialogs["pause"])

            self.player.draw_pile = self.player.discard_pile[:]
            self.player.discard_pile = []
            random.shuffle(self.player.draw_pile)

        card = self.player.draw_pile.pop()
        self.hand.append(card)

    def abandon_battle(self):
        printLine()
        print(self.enemy.stats)
        print(self.enemy.reward.description)
        printLine()
        print(self.show_hand())

        difference = self.enemy.HP - self.hand_damage
        self.player.HP -= difference
        HPplural = "s" if difference > 1 else ""

        print(dialogs["fight"]["abandon"])
        print(
            f"\n You have lost \033[1;33;40m{difference}\033[1;37;40m health point{HPplural}. Your current health is \033[1;33;40m{self.player.HP}\033[1;37;40m.\n")
        input(dialogs["pause"])

        self.forget_cards(difference)

    def forget_cards(self, repeat):
        card_to_forget = ""

        while card_to_forget != "exit" and repeat > 0:
            print(dialogs["fight"]["forget_cards"])
            print(self.show_hand())
            if len(self.hand) == 0:
                break

            card_to_forget = input(
                "\n".join(dialogs["fight"]["forget_cards_prompt"]).format(repeat))

            for card in self.hand:
                if card.short_name == card_to_forget:
                    # TODO handle flaw card as x2
                    self.hand.remove(card)
                    repeat -= 1
                    break

        printLine()
        print(dialogs["fight"]["forget_end"])
        printLine("\n")
        input(dialogs["pause"])

    def discard_cards(self, repeat):
        card_to_discard = ""

        #? Should we let the user exit a discard move?
        while card_to_discard != "exit" and repeat > 0:
            printLine()
            print(self.show_hand())
            if len(self.hand) == 0:
                break

            plural = "s" if repeat > 1 else ""
            print(
                f"\n You may discard \033[1;33;40m{repeat}\033[1;37;40m more card{plural}.\n")
            printLine()

            card_to_discard = input(
                " Type the name of the card you wish to discard.\n")

            for card in self.hand:
                if card.short_name == card_to_discard:
                    self.hand.remove(card)
                    self.player.discard_pile.append(card)
                    repeat -= 1
                    break
            else:
                print(dialogs["monastery"]["fight"]["discard_error"])

    def fight(self):
        printLine()
        print("\033[1;34;40m" + self.enemy.desc)
        printLine()
        input(dialogs["pause"])

        self.enemy.at_fight_beginning(self.player)

        while True:
            printLine()
            print(self.enemy.stats)
            print(self.enemy.reward.description)
            printLine()
            print(self.show_hand())

            if self.hand_damage >= self.enemy.HP:
                self.battle_won()
                break

            printLine("\n")
            print(self.fight_info())

            abandoned = self.user_move()
            if abandoned:
                break

            for card in self.hand:
                card.at_turn_update(self.hand)

            self.hand_damage = sum(card.attack for card in self.hand)
            self.enemy.at_turn_update(self, self.hand, self.player)

        # End of the battle
        self.enemy.at_fight_end(self, self.hand, self.player)
        for card in self.hand:
            card.at_fight_end(self.hand, self.player)
        self.player.discard_pile.extend(self.hand)

    def battle_won(self):
        print(dialogs["fight"]["win"].format(self.enemy.name))
        input(dialogs["pause"])

        self.player.discard_pile.append(self.enemy.reward)
        self.win = True
