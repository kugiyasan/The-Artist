import random
import re

from utils import dialogs

class Card:
    def __init__(self, name: str, attack: int, effect="No effect.", heal=0, draw=0, discard=0, forget=0, use=None, isanimal=False):
        self.name = name # Nom de la carte
        self.attack = attack # Valeur numérique de la carte
        self.effect = effect # Effet de la carte
        self.heal = heal
        self.draw = draw
        self.discard = discard
        self.forget = forget
        self.usable =  use

        self.short_name = self.name[4:].lower() if self.name.startswith("The ") else self.name.lower()

    def at_turn_update(self, hand):
        """at_turn_update is called at each turn when the Card is in the hand"""
        pass

    def at_fight_end(self, hand, player):
        """at_fight_end is called at the end of the fight"""
        if self.heal > 0 and self.usable:
            print(f"{self.name} is healing you\n\n")
            player.HP += self.heal

    @property
    def description(self):
        if self.attack > 0: # Positive values displayed green
            color = 32
        elif self.attack == 0: # 0 displayed yellow
            color = 33
        else: # Negative values displayed red
            color = 31

        if self.usable == True:
            use_state = "\033[1;32;40m*\033[1;37;40m"
        elif self.usable == False:
            use_state = "\033[1;31;40m- USED\033[1;37;40m"
        else:
            use_state = ""

        return " {0.name} (\033[1;{1};40m{0.attack}\033[1;37;40m) - {0.effect} {2}".format(self, color, use_state)

    def use_card(self, fight, player, enemy):
        if self.usable == False:
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


red = Card("Red", 2)
blue = Card("Blue", 0, "Heal 2 HP.", heal=2, use=True)
yellow = Card("Yellow", 1, "Draw 1 card.", heal=0, draw=1, use=True)
beginning = Card("The Beginning", 1)
dawn = Card("The Dawn", 2, "Heal 2 HP. Draw 2 cards.", heal=2, draw=2, use=True)
canvas = Card("The Canvas" , 0)

class Tiger(Card):
    def at_turn_update(self, hand):
        self.attack = len(hand) // 2

class Stag(Card):
    def at_turn_update(self, hand):
        self.attack = len(hand) - 5

class Snake(Card):
    def use_card(self, fight, player, enemy):
        player.HP -= 1
        self.attack += 1

class Swan(Card):
    def at_turn_update(self, hand):
        if len(hand) == 1:
            self.attack = 4
        else:
            self.attack = 0

class Crane(Card):
    def at_turn_update(self, hand):
        self.attack = -2
        for card in hand:
            if card.attack < 0:
                self.attack += 2

class Turtle(Card):
    def at_fight_end(self, hand, player):
        hand.remove(self)
        player.draw_pile.append(self)

class Spider(Card):
    def at_fight_end(self, hand, player):
        player.HP -= 2

class Acolyte(Card):
    def at_turn_update(self, hand):
        self.attack = 2
        for card in hand:
            if card.isanimal:
                self.attack += 1

class Dusk(Card):
    def at_fight_end(self, hand, player):
        # random.shuffle(hand)
        # hand.pop()
        hand.pop(random.randrange(0, len(hand)))
        player.HP -= 1

class Deceased(Card):
    def at_fight_end(self, hand, player):
        player.HP = 0

tiger = Tiger("The Tiger", 0, "This card's value begins at 0, and increases by 1 for every 2 cards in your hand.", isanimal=True)  #! SPECIAL each turn len(hand)   
stag = Stag("The Stag", -5, "This card's value increases by 1 for every card in your hand.", isanimal=True)  #! SPECIAL each turn len(hand)
dragon = Card ("The Dragon", 4, isanimal=True)
snake = Snake("The Snake", 0, "Reusable. Lose 1 HP. For this combat, this card's value increases by 1.", use=True, isanimal=True) #! SPECIAL use
rabbit = Card ("The Rabbit", 0, "Discard 2 cards. Draw 2 cards.", draw=2, discard=2, use=True, isanimal=True)
leopard = Card("The Leopard", 1, "Draw 1 card.", draw=1, use=True, isanimal=True)
swan = Swan("The Swan", 0, "This card value's is 0. If this is the only card in your hand, the value of this card becomes 4.", isanimal=True) #! SPECIAL each turn len(hand)
crane = Crane("The Crane", -2, "This card's value increases by 2 for every card with a negative value in your hand.", isanimal=True) #! SPECIAL each turn hand
turtle = Turtle ("The Turtle", 1, "At the end of this combat, put this card back in your draw pile.", isanimal=True) #! SPECIAL after battle
mantis = Card ("The Mantis",2,"Heal 1 HP.", heal=1, use=True, isanimal=True)
wolf = Card("The Wolf", 3, "Forget 1 card.", forget=1, use=True, isanimal=True)
monkey = Card("The Monkey", 2,"If the enemy you are facing has a might value equal to or greater than 10, gain 1 bonus inspiration when this card is drawn.", isanimal=True) #! SPECIAL at draw
spider = Spider("The Spider", 3, "At the end of this combat, lose 2 HP.", isanimal=True) #! SPECIAL after battle
crow = Card("The Crow", 2, "Discard 1 card.", discard=1, use=True, isanimal=True)
frog = Card("The Frog", 0, "Forget 1 card.", forget=1, use=True, isanimal=True)

acolyte = Acolyte("The Acolyte", 2, "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.") #! SPECIAL each turn
master = Acolyte("The Acolyte", 2, "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.") #! SPECIAL each turn

god = Card("The God", 420)

def flaw_pile_generator():
    shamed = Card("The Shamed", -2, "Flaw. No effect.")
    dusk = Dusk("The Dusk", -1, "Flaw. At the end of this combat, forget a random card in your hand and lose 1 HP.") #! SPECIAL after battle

    desperate = Card("The Desperate", 0, "Flaw. No effect.")
    deceased = Deceased("The Deceased", -99, "Flaw. At the end of this combat, die.") #! SPECIAL after battle

    flaws = [shamed, dusk]
    random.shuffle(flaws)

    yield flaws.pop()
    yield flaws.pop()

    yield desperate
    while True:
        yield deceased

flaw_pile = flaw_pile_generator()

animalpool = [tiger, stag, dragon, snake, rabbit, leopard, swan, crane, turtle, mantis, wolf, monkey, spider, crow, frog]


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

        if not short_name:
            if not self.name.startswith("The "):
                raise ValueError("name should begin with 'The ' or specify a short_name")
            short_name = self.name[4:].lower()
        self.desc = "\n ".join(dialogs["enemies"][short_name])

    @property
    def stats(self):
        text = """\033[1;36;40m {0.name}\033[1;37;40m
        Might: \033[1;31;40m{0.HP}\033[1;37;40m
        Inspiration: \033[1;32;40m{0.number_of_insp}\033[1;37;40m
        Effects: \033[1;33;40m{0.effect}\033[1;37;40m
        
        \033[1;34;40mREWARD:\033[1;37;40m
        """.strip().format(self)
        return re.sub("\n +", "\n ", text)

# TODO each enemy should be derived from the Enemy class, and they should implement the custom fight mechanics
#might, inspiration
tigerE = Enemy("The Tiger", 4, 4, "No effects.", tiger)
swanE = Enemy("The Swan", 0, 0, "No effects.", swan)
dragonE = Enemy("The Dragon", 10, 5, "Each card in your hand adds 1 to your total might.", dragon) #! SPECIAL each turn hand
craneE = Enemy("The Crane", 0, 1, "This enemy's might is equal to the number of Flaw cards you have in your deck.", crane) #! SPECIAL first turn player
leopardE = Enemy("The Leopard", 2, 3, "You may not have more than 3 cards in your hand. Exceeding this limit will cause a random card to be discarded.", leopard) #! SPECIAL each turn hand
snakeE = Enemy("The Snake", 1, 1, "No effects.", snake)
monkeyE = Enemy("The Monkey", "?", 1, "This enemy's might is equal to the value of a random card taken away from your deck. The card will be put back at the end of the combat.",monkey) #! SPECIAL first turn player + end battle
stagE = Enemy("The Stag", 2, 3, "No effects.", stag)
mantisE = Enemy("The Mantis", 3, 3, "Each unused point of inspiration after this combat heals you for 1 HP.", mantis) #! SPECIAL end battle hand player
wolfE = Enemy("The Wolf", 4, 4, "If you lose this combat, forget a random card in your hand.", wolf)  #! SPECIAL end battle win/lose hand
rabbitE = Enemy("The Rabbit",0,0,"No effects.", rabbit)
turtleE = Enemy ("The Turtle",2,2,"No effects.",turtle)
spiderE = Enemy("The Spider",0,0,"No effects.",spider)
#? Reaction of The Crow vs Snake (discard or not)(plz not discard easier)
crowE = Enemy("The Crow", 2,3,"Whenever you use the active effect of a card, discard it.",crow) #! SPECIAL each turn hand 
frogE = Enemy("The Frog", 1,1,"No effects.",frog)

fight1pool = [tigerE, swanE, dragonE, craneE, leopardE, snakeE, monkeyE, stagE, mantisE, wolfE, rabbitE, turtleE,spiderE,crowE,frogE]

acolyteE = Enemy("The Acolyte", 8,5, "Every card in your hand which contains the name of an animal increases your total might by 1.", acolyte, short_name="acolyte") #! SPECIAL each turn hand
master1 = Enemy("The Master \033[1;37;40m(\033[1;32;40m███\033[1;37;40m)", 8, 5, "Every card in your hand which contains the name of an animal increases The Master's total might by 1.", master, short_name="master1") #! SPECIAL each turn hand
master2 = Enemy("The Master \033[1;37;40m(\033[1;32;40m██\033[1;31;40m█\033[1;37;40m)", 4, 1, "At the end of this combat, heal 1 HP for every point of might exceeding the required total.", master, short_name="master2") #! SPECIAL end battle player enemy hand
master3 = Enemy("The Master \033[1;37;40m(\033[1;32;40m█\033[1;31;40m██\033[1;37;40m)", 10, 3, "At the start of this combat, gain 1 inspiration for every Flaw present in your deck.", master, short_name="master3") #! SPECIAL first turn player self
