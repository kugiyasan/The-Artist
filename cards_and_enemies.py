import random
import re

from utils import dialogs


class Card:
    def __init__(self, name: str, attack: int, effect="No effect.",
                 heal=0, draw=0, discard=0, forget=0,
                 use=None, is_animal=False, is_flaw=False):
        self.name = name
        self.attack = attack
        self.effect = effect
        self.heal = heal
        self.draw = draw
        self.discard = discard
        self.forget = forget
        self.usable = use
        # should replace the next var by self.family, which may contain a Enum
        self.is_animal = is_animal
        self.is_flaw = is_flaw

        self.short_name = self.name[4:].lower() if self.name.startswith(
            "The ") else self.name.lower()

    @property
    def description(self):
        if self.attack > 0:  # Positive values displayed in green
            color = 32
        elif self.attack == 0:  # 0 displayed in yellow
            color = 33
        else:  # Negative values displayed in red
            color = 31

        if self.usable == True:
            use_state = "\033[1;32;40m*\033[1;37;40m"
        elif self.usable == False:
            use_state = "\033[1;31;40m- USED\033[1;37;40m"
        else:
            use_state = ""

        return " {0.name} (\033[1;{1};40m{0.attack}\033[1;37;40m) - {0.effect} {2}".format(self, color, use_state)

    def at_draw(self, fight, enemy):
        if self.usable != None:
            self.usable = True

    def at_turn_update(self, hand):
        """at_turn_update is called at each turn when the Card is in the hand"""
        pass

    def at_fight_end(self, hand, player):
        """at_fight_end is called at the end of the fight"""
        if self.heal > 0 and self.usable:
            # TODO remove the print or make something nicer
            print(f"{self.name} is healing you\n\n")
            player.HP += self.heal

    def use_card(self, fight, player, enemy):
        """default behavior of a Card, override for custom behavior"""
        if self.usable != True:
            # TODO remove the print or make something nicer
            print("\nCan't use that card!\n")
            return

        self.usable = False

        player.HP += self.heal

        for _ in range(self.draw):
            fight._draw_card()

        if self.discard > 0:
            fight.discard_cards(self.discard)

        if self.forget > 0:
            fight.forget_cards(self.forget)


class Crane(Card):
    def at_turn_update(self, hand):
        self.attack = -2
        for card in hand:
            if card.attack < 0:
                self.attack += 2


class Monkey(Card):
    def at_draw(self, fight, enemy):
        if enemy.HP >= 10:
            fight.inspiration += 1


class Snake(Card):
    def use_card(self, fight, player, enemy):
        player.HP -= 1
        self.attack += 1


class Spider(Card):
    def at_fight_end(self, hand, player):
        player.HP -= 2


class Stag(Card):
    def at_turn_update(self, hand):
        self.attack = len(hand) - 5


class Swan(Card):
    def at_turn_update(self, hand):
        if len(hand) == 1:
            self.attack = 4
        else:
            self.attack = 0


class Tiger(Card):
    def at_turn_update(self, hand):
        self.attack = len(hand) // 2


class Turtle(Card):
    def at_fight_end(self, hand, player):
        hand.remove(self)
        player.draw_pile.append(self)


class Acolyte(Card):
    def at_turn_update(self, hand):
        self.attack = 2
        for card in hand:
            if card.is_animal:
                self.attack += 1


class Dusk(Card):
    def at_fight_end(self, hand, player):
        hand.pop(random.randrange(0, len(hand)))
        player.HP -= 1


class Deceased(Card):
    def at_fight_end(self, hand, player):
        player.HP = 0


beginning = Card("The Beginning", 1)
canvas = Card("The Canvas", 0)
red = Card("Red", 2)
blue = Card("Blue", 0, "Heal 2 HP.", heal=2, use=True)
yellow = Card("Yellow", 1, "Draw 1 card.", heal=0, draw=1, use=True)
dawn = Card("The Dawn", 2, "Heal 2 HP. Draw 2 cards.",
            heal=2, draw=2, use=True)

crane = Crane("The Crane", -2, "This card's value increases by 2 for every card with a negative value in your hand.",
              is_animal=True)
crow = Card("The Crow", 2, "Discard 1 card.",
            discard=1, use=True, is_animal=True)
dragon = Card("The Dragon", 4, is_animal=True)
frog = Card("The Frog", 0, "Forget 1 card.",
            forget=1, use=True, is_animal=True)
leopard = Card("The Leopard", 1, "Draw 1 card.",
               draw=1, use=True, is_animal=True)
mantis = Card("The Mantis", 2, "Heal 1 HP.", heal=1, use=True, is_animal=True)
monkey = Monkey("The Monkey", 2, "If the enemy you are facing has a might value equal to or greater than 10, gain 1 bonus inspiration when this card is drawn.",
                is_animal=True)
rabbit = Card("The Rabbit", 0, "Discard 2 cards. Draw 2 cards.",
              draw=2, discard=2, use=True, is_animal=True)
snake = Snake("The Snake", 0, "Reusable. Lose 1 HP. For this combat, this card's value increases by 1.",
              use=True, is_animal=True)
spider = Spider("The Spider", 3, "At the end of this combat, lose 2 HP.",
                is_animal=True)
stag = Stag("The Stag", -5, "This card's value increases by 1 for every card in your hand.",
            is_animal=True)
swan = Swan("The Swan", 0, "This card value's is 0. If this is the only card in your hand, the value of this card becomes 4.",
            is_animal=True)
tiger = Tiger("The Tiger", 0, "This card's value begins at 0, and increases by 1 for every 2 cards in your hand.",
              is_animal=True)
turtle = Turtle("The Turtle", 1, "At the end of this combat, put this card back in your draw pile.",
                is_animal=True)
wolf = Card("The Wolf", 3, "Forget 1 card.",
            forget=1, use=True, is_animal=True)

starter_draw_pile = [red, yellow, blue, dawn,
                     beginning, beginning] + [canvas] * 7

# ! SPECIAL each turn
acolyte = Acolyte("The Acolyte", 2,
                  "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.")
# ! SPECIAL each turn
master = Acolyte("The Acolyte", 2,
                 "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.")


def flaw_pile_generator():
    shamed = Card("The Shamed", -2, "Flaw. No effect.", is_flaw=True)
    dusk = Dusk("The Dusk", -1, "Flaw. At the end of this combat, forget a random card in your hand and lose 1 HP.",
                is_flaw=True)

    desperate = Card("The Desperate", 0, "Flaw. No effect.", is_flaw=True)
    deceased = Deceased("The Deceased", -99,
                        "Flaw. At the end of this combat, die.", is_flaw=True)

    flaws = [shamed, dusk]
    random.shuffle(flaws)

    yield flaws.pop()
    yield flaws.pop()

    yield desperate
    while True:
        yield deceased


flaw_pile = flaw_pile_generator()


class Enemy:
    def __init__(self, name, HP, number_of_insp, effect, reward, short_name=None):
        """
        The default Enemy Class, to inherit to create an enemy with particular effect
        name should begins with "The "
        If you let desc to None, be sure to provide a description inside dialogs.json
        """
        self.name = name
        self.HP = HP  # HP can be a int or a str
        self.effect = effect
        self.number_of_insp = number_of_insp
        self.reward = reward

        if short_name is None:
            if not self.name.startswith("The "):
                raise ValueError(
                    "name should begin with 'The ' or specify a short_name")
            short_name = self.name[4:].lower()
        self.desc = "\n ".join(dialogs["enemies"].get(
            short_name, [f"A wild {self.name} appeared!"]))

    @property
    def stats(self):
        text = """\033[1;36;40m {0.name}\033[1;37;40m
        Might: \033[1;31;40m{0.HP}\033[1;37;40m
        Inspiration: \033[1;32;40m{0.number_of_insp}\033[1;37;40m
        Effects: \033[1;33;40m{0.effect}\033[1;37;40m
        
        \033[1;34;40mREWARD:\033[1;37;40m
        """.strip().format(self)
        return re.sub("\n +", "\n ", text)

    def at_turn_update(self, fight, hand, player):
        pass

    def at_fight_beginning(self, fight, player):
        pass

    def at_fight_end(self, fight, hand, player):
        pass


class CrowE(Enemy):
    def at_turn_update(self, fight, hand, player):
        fight.hand_damage += len(hand)


class CraneE(Enemy):
    def at_fight_beginning(self, fight, player):
        #! need to update in battle if a flaw is removed from the deck
        self.HP = 0
        for card in player.draw_pile + player.discard_pile:
            if card.is_flaw:
                self.HP += 1


class DragonE(Enemy):
    def at_turn_update(self, fight, hand, player):
        fight.hand_damage += len(hand)

# TODO tell which card has been pop


class LeopardE(Enemy):
    def at_turn_update(self, fight, hand, player):
        if len(hand) > 3:
            card = hand.pop(random.randrange(len(hand)))
            player.discard_pile.append(card)
            fight.hand_damage -= card.attack


class MantisE(Enemy):
    def at_fight_end(self, fight, hand, player):
        player.HP += fight.inspiration

# TODO better explanation to the user of what's happening
# Like showing the stolen card
# Bonus: The Monkey should leave with the card if the player loses


class MonkeyE(Enemy):
    def at_fight_beginning(self, fight, player):
        self.monkey_steal = player.draw_pile_pop()
        self.HP = self.monkey_steal.attack

    def at_fight_end(self, fight, hand, player):
        player.discard_pile.append(self.monkey_steal)


class WolfE(Enemy):
    def at_fight_end(self, fight, hand, player):
        if not fight.win:
            #! pop on empty list
            hand.pop(random.randrange(len(hand)))


#might, inspiration
craneE = CraneE("The Crane", 0, 1,
                "This enemy's might is equal to the number of Flaw cards you have in your deck.", crane)
crowE = CrowE("The Crow", 2, 3,
              "Whenever you use the active effect of a card, discard it.", crow)
dragonE = DragonE("The Dragon", 10, 5,
                  "Each card in your hand adds 1 to your total might.", dragon)
frogE = Enemy("The Frog", 1, 1, "No effects.", frog)
leopardE = LeopardE("The Leopard", 2, 3,
                    "You may not have more than 3 cards in your hand. Exceeding this limit will cause a random card to be discarded.", leopard)
mantisE = MantisE("The Mantis", 3, 3,
                  "Each unused point of inspiration after this combat heals you for 1 HP.", mantis)
monkeyE = MonkeyE("The Monkey", "?", 1,
                  "This enemy's might is equal to the value of a random card taken away from your deck. The card will be put back at the end of the combat.", monkey)
rabbitE = Enemy("The Rabbit", 0, 0, "No effects.", rabbit)
snakeE = Enemy("The Snake", 1, 1, "No effects.", snake)
spiderE = Enemy("The Spider", 0, 0, "No effects.", spider)
stagE = Enemy("The Stag", 2, 3, "No effects.", stag)
swanE = Enemy("The Swan", 0, 0, "No effects.", swan)
tigerE = Enemy("The Tiger", 4, 4, "No effects.", tiger)
turtleE = Enemy("The Turtle", 2, 2, "No effects.", turtle)
wolfE = WolfE("The Wolf", 4, 4,
              "If you lose this combat, forget a random card in your hand.", wolf)

fight1pool = [tigerE, swanE, dragonE, craneE, leopardE, snakeE, monkeyE,
              stagE, mantisE, wolfE, rabbitE, turtleE, spiderE, crowE, frogE]


class AcolyteE(Enemy):
    def at_turn_update(self, fight, hand, player):
        fight.hand_damage += sum(1 for card in hand if card.is_animal)


class Master1E(Enemy):
    def at_turn_update(self, fight, hand, player):
        self.HP += sum(1 for card in hand if card.is_animal)


class Master2E(Enemy):
    def at_fight_end(self, fight, hand, player):
        difference = fight.inspiration - self.HP
        player.HP += difference


class Master3E(Enemy):
    def at_fight_beginning(self, fight, player):
        fight.inspiration += sum(1 for card in player.draw_pile if card.is_flaw)


acolyteE = AcolyteE("The Acolyte", 8, 5, "Every card in your hand which contains the name of an animal increases your total might by 1.",
                    acolyte, short_name="acolyte")
master1E = Master1E("The Master \033[1;37;40m(\033[1;32;40m███\033[1;37;40m)", 8, 5,
                    "Every card in your hand which contains the name of an animal increases The Master's total might by 1.", master, short_name="master1")
master2E = Master2E("The Master \033[1;37;40m(\033[1;32;40m██\033[1;31;40m█\033[1;37;40m)", 4, 1,
                    "At the end of this combat, heal 1 HP for every point of might exceeding the required total.", master, short_name="master2")
master3E = Master3E("The Master \033[1;37;40m(\033[1;32;40m█\033[1;31;40m██\033[1;37;40m)", 10, 3,
                    "At the start of this combat, gain 1 inspiration for every Flaw present in your deck.", master, short_name="master3")
