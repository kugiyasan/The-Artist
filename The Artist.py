# AUTHOR: JULIEN ROBERT

# crow as enemy, can discard any card in the hand
# reshuffle doesn't remove inspiration (vs wolf, drawed swan)

import json
import random # Praise RNGesus
import re
import sys
import time

with open("dialogs.json") as jsonFile:
    dialogs = json.load(jsonFile)

godmode = False

if godmode:
    print("GODMODE IS ACTIVATED\n\n")

room = 0
HP = 20
honor = 0
boss = 0

def printLine():
    # print("=" * 49)
    # the line below will hide a lot of visual glitches,
    # however I think it's a good practice to put back the default color in the json file
    # that would also make it easier to remove the separator lines in the case of a more sophisticated ui
    print("\u001b[1;37;40m" + "=" * 49)

    # print("\u001b[1;37;40m")
    # for _ in range(49):
    #     sys.stdout.write("=")
    #     sys.stdout.flush()
    #     time.sleep(0.01)
    
    # print()

class Card:
    def __init__(self, name:str, val:int, effect="No effect.", heal=0, draw=0, discard=0, forget=0, use=False):
        self.name = name # Nom de la carte
        self.val = val # Valeur numérique de la carte
        self.effect = effect # Effet de la carte
        self.heal = heal
        self.draw = draw
        self.use = "\033[1;32;40m*\033[1;37;40m" if use else ""
        self.discard = discard
        self.forget = forget
    def show(self):
        if self.val > 0: #Valeurs positives en vert
            color = 32
        elif self.val == 0: #Valeurs de 0 en jaune
            color = 33
        else: #Valeurs négatives en rouge
            color = 31
        print(" {0.name} (\033[1;{1};40m{0.val}\033[1;37;40m) - {0.effect} {0.use}".format(self, color))


hand = []
discard = []

handlength = 0

shamed = Card("The Shamed", -2, "Flaw. No effect.")
dusk = Card("The Dusk", -1, "Flaw. At the end of this combat, forget a random card in your hand and lose 1 HP.")

desperate = Card("The Desperate", 0, "Flaw. No effect.")
deceased = Card("The Deceased", -99, "Flaw. At the end of this combat, die.")

# TODO change Flaw into an iterator, and call next() instead of .pop(0)
Flaw = [shamed, dusk]
random.shuffle(Flaw)
Flaw.append(desperate)
for x in range (50):
    Flaw.append(deceased)

red = Card("Red", 2)
blue = Card("Blue", 0, "Heal 2 HP.", heal=2, use=True)
yellow = Card("Yellow", 1, "Draw 1 card.", heal=0, draw=1, use=True)
beginning = Card("The Beginning", 1)
dawn = Card("The Dawn", 2, "Heal 2 HP. Draw 2 cards.", heal=2, draw=2, use=True)
canvas = Card("The Canvas" , 0)

tiger = Card("The Tiger", 0, "This card's value begins at 0, and increases by 1 for every 2 cards in your hand.")
stag = Card("The Stag", -5, "This card's value increases by 1 for every card in your hand.")
dragon = Card ("The Dragon", 4)
snake = Card("The Snake", 0, "Reusable. Lose 1 HP. For this combat, this card's value increases by 1.", use=True)
rabbit = Card ("The Rabbit", 0, "Discard 2 cards. Draw 2 cards.", draw=2, discard=2, use=True)
leopard = Card("The Leopard", 1, "Draw 1 card.", draw=1, use=True)
swan = Card("The Swan", 0, "This card value's is 0. If this is the only card in your hand, the value of this card becomes 4.")
crane = Card("The Crane", -2, "This card's value increases by 2 for every card with a negative value in your hand.")
turtle = Card ("The Turtle", 1, "At the end of this combat, put this card back in your draw pile.")
mantis = Card ("The Mantis",2,"Heal 1 HP.", heal=1, use=True)
wolf = Card("The Wolf", 3, "Forget 1 card.", forget=1, use=True)
monkey = Card("The Monkey", 2,"If the enemy you are facing has a might value equal to or greater than 10, gain 1 bonus inspiration when this card is drawn.")
spider = Card("The Spider", 3, "At the end of this combat, lose 2 HP.")
crow = Card("The Crow", 2, "Discard 1 card.", discard=1, use=True)
frog = Card("The Frog", 0, "Forget 1 card.", forget=1, use=True)

acolyte = Card("The Acolyte", 2, "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.")
master = Card("The Acolyte", 2, "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.")

# Deck du joueur initial, sera modifié par après
pile = [red, yellow, blue, dawn, beginning, beginning] + [canvas] * 7
random.shuffle(pile) # shuffle initial

animalpool = [tiger, stag, dragon, snake, rabbit, leopard, swan, crane, turtle, mantis, wolf, monkey, spider, crow, frog]

monkeycom = False #effet de l'ennemi monkey
moncom = False #effet de la carte monkey

class Enemy:
    def __init__(self, name, val, draw, effect, reward, desc=None):
        self.name = name
        self.val = val # val can be a int or a str
        self.effect = effect
        self.draw = draw
        self.reward = reward
        
        if not desc:
            shortName = name[4:].lower()
            self.desc = "\n ".join(dialogs["enemies"][shortName])
        else:
            self.desc = desc

    def show(self):
        printLine()
        stats = """\033[1;36;40m {0.name}\033[1;37;40m
        Might: \033[1;31;40m{0.val}\033[1;37;40m
        Inspiration: \033[1;32;40m{0.draw}\033[1;37;40m
        Effects: \033[1;33;40m{0.effect}\033[1;37;40m
        
        \033[1;34;40mREWARD:\033[1;37;40m
        """.strip().format(self)
        stats = re.sub("\n +", "\n ", stats)
        print(stats)
        self.reward.show()

    def introduce(self):
        printLine()
        print("\033[1;34;40m" + self.desc)
        printLine()


# TODO each enemy should be derived from the Enemy class, and they should implement the fight mechanic themselves
#might, inspiration
tigerE = Enemy("The Tiger", 4, 4, "No effects.", tiger)
swanE = Enemy("The Swan", 0, 0, "No effects.", swan)
dragonE = Enemy("The Dragon", 10, 5, "Each card in your hand adds 1 to your total might.", dragon)
craneE = Enemy("The Crane", 0, 1, "This enemy's might is equal to the number of Flaw cards you have in your deck.", crane)
leopardE = Enemy("The Leopard", 2, 3, "You may not have more than 3 cards in your hand. Exceeding this limit will cause a random card to be discarded.", leopard)
snakeE = Enemy("The Snake", 1, 1, "No effects.", snake)
monkeyE = Enemy("The Monkey", "?", 1, "This enemy's might is equal to the value of a random card taken away from your deck. The card will be put back at the end of the combat.",monkey)
stagE = Enemy("The Stag", 2, 3, "No effects.", stag)
mantisE = Enemy("The Mantis", 3, 3, "Each unused point of inspiration after this combat heals you for 1 HP.", mantis)
wolfE = Enemy("The Wolf", 4, 4, "If you lose this combat, forget a random card in your hand.", wolf)
rabbitE = Enemy("The Rabbit",0,0,"No effects.", rabbit)
turtleE = Enemy ("The Turtle",2,2,"No effects.",turtle)
spiderE = Enemy("The Spider",0,0,"No effects.",spider)
crowE = Enemy("The Crow", 2,3,"Whenever you use the active effect of a card, discard it.",crow)
frogE = Enemy("The Frog", 1,1,"No effects.",frog)
fight1pool = [tigerE, swanE, dragonE, craneE, leopardE, snakeE, monkeyE, stagE, mantisE, wolfE, rabbitE, turtleE,spiderE,crowE,frogE]

acolyteE = Enemy("The Acolyte", 8,5, "Every card in your hand which contains the name of an animal increases your total might by 1.", acolyte, "\033[1;34;40m \"I can see that the notion of rest is alien to you\"\n \"For you, every situation is yet another painting waiting to be created, is it not?\"\n \"My apologies, dear Artist, but a sketch of me is not granted\"\n \"It is earned.\"\n I open my sketchbook at its first page, as the Acolyte takes on her battle stance.")
master1 = Enemy("The Master \033[1;37;40m(\033[1;32;40m███\033[1;37;40m)", 8, 5, "Every card in your hand which contains the name of an animal increases The Master's total might by 1.", master, "\n \033[1;31;40mROUND 1\n\n \033[1;34;40m\"Each statue I have carved possesses a soul of its own.\"\n \"However, I am, and will always will be their Master\"\n \"To begin your final test, let us see if you have memorized their lessons.\"")
master2 = Enemy("The Master \033[1;37;40m(\033[1;32;40m██\033[1;31;40m█\033[1;37;40m)", 4, 1, "At the end of this combat, heal 1 HP for every point of might exceeding the required total.", master, "\n \033[1;31;40mROUND 2\n\n \033[1;34;40m\"This next battle should be much easier, now that you have acquainted yourself with my fighting style.\"\n \"However, make sure to keep painting to the best of your ability!\"\n \"I like to grant a special reward to disciples who truly manage to exceed my expectations.\"")
master3 = Enemy("The Master \033[1;37;40m(\033[1;32;40m█\033[1;31;40m██\033[1;37;40m)", 10, 3, "At the start of this combat, gain 1 inspiration for every Flaw present in your deck.", master, "\n \033[1;31;40mFINAL ROUND\n\n \033[1;34;40m\"It is time. Show me the true colors of your power!\"\n \"I wish to see every work of art you have crafted in my grove.\"\n \"Even the worst Flaws can be turned into something beautiful by the most proficient students!\"")


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
        #rose, lilac, daffodil...
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
    else: # dest == "2"
        Observatory()

def Monastery():
    printLine()
    print("\n".join(dialogs["monastery"]["intro"]))
    printLine()
    input(dialogs["pause"])
    EncounterM()
        
def Observatory():
    printLine()
    print("\n".join(dialogs["observatory"]))
    printLine()
    input(dialogs["pause"])
    raise NotImplementedError
    # Encounter()

def Hive():
    printLine()
    print(dialogs["hive"])
    printLine()
    input(dialogs["pause"])
    raise NotImplementedError
    # Encounter()

def CardValueSort(sort): #Pour trier les cartes de la pile dans forget
    return sort.val

class Encounter:
    def __init__ (self, enemy, location):
        self.enemy = enemy
        self.location = location
    def Fight(self):
        global pile
        global discard
        global hand
        global boss
        global handlength
        self.enemy.introduce()
        printLine()
        input(dialogs["pause"])
        insp = self.enemy.draw
        global HP
        global honor
        global room
        global monkeycom
        global moncom
        room += 1
        mastercom = False

        # ! every animal / enemy specific thing should go in their respective class, here it will be the generic fight logic, inherited by the animals
        while True:
            dam = 0
            handlength = len(hand)
            ############################################################################################### EFFETS DÉPART
            tiger.val = handlength // 2 # tiger effect
            stag.val = -5
            stag.val += handlength
            crane.val = -2
            acolyte.val = 2
            if len(hand) == 1:
                swan.val = 4
            else:
                swan.val = 0
            for o in hand:
                if o.val < 0 and o.name != "The Crane":
                    crane.val += 2
                else:
                    continue
            if self.enemy.name == "The Dragon":
                dam += handlength
            if self.enemy.name == "The Leopard":
                if handlength > 3:
                    random.shuffle(hand)
                    shucks = hand.pop()
                    discard.append(shucks)
            if self.enemy.name == "The Acolyte":
                for x in hand:
                    if x in animalpool:
                        dam += 1
            if self.enemy == master1: #Boss Master 1
                self.enemy.val= 8
                for x in hand:
                    if x in animalpool:
                        self.enemy.val += 1
            for x in hand:
                if x in animalpool and acolyte in hand:
                    x.val += 1
            if self.enemy == master3 and mastercom == False:
                if len(pile) > 0:
                    for x in pile:
                        if "Flaw" in x.effect:
                            insp += 1
                if len(discard) > 0:
                    for x in discard:
                        if "Flaw" in x.effect:
                            insp += 1
                mastercom = True
            if self.enemy.name == "The Monkey" and monkeycom == False:
                if len(pile) > 0:
                    monkeysteal = pile.pop()
                    monkeyE.val = monkeysteal.val
                    monkeycom = True
                else:
                    monkeysteal = discard.pop()
                    monkeyE.val = monkeysteal.val
                    monkeycom = True
            if monkey in hand and self.enemy.val >= 10 and moncom == False:
                insp += 1
                moncom = True
            ############################################################################################### EFFETS DÉPART
            if HP > 24:
                HP = 24
            for x in hand:
                dam += x.val
            if godmode == True:
                dam = 999
            if dam >= self.enemy.val:
                self.enemy.show()
                printLine()
                for x in hand:
                    x.show()
                    if x.use != "- \033[1;31;40mUSED\033[1;37;40m" and ("Heal" in x.effect):
                        HP += x.heal
                    x.use = ""
                if boss == 0:
                    discard.append(self.enemy.reward)
                ############################################################################################### EFFETS VICTOIRE
                if spider in hand:
                    HP -= 2
                snake.val = 0
                stag.val = -5
                crane.val = -2
                if self.enemy.name == "The Monkey":
                    discard.append(monkeysteal)
                if self.enemy.name == "The Mantis":
                    HP += insp
                if dusk in hand:
                    HP -= 1
                    hand.remove(dusk)
                    random.shuffle(hand)
                    duskremove = hand.pop()
                    hand.append(dusk)
                    print("\n "+str(duskremove.name)+" has been removed from your deck. (The Dusk)")
                if self.enemy == master2 and dam > self.enemy.val:
                    HP += dam-self.enemy.val
                ############################################################################################### EFFETS VICTOIRE
                discard += hand
                hand.clear()
                if self.enemy == master1:
                    print("\033[1;34;40m\n \"Excellent work, disciple! However, I am only getting started...\"\033[1;37;40m")
                    honor += 1
                elif self.enemy == master2:
                    print("\033[1;34;40m\n \"How splendid! It seems you are ready for your true ultimate trial.\"\033[1;37;40m")
                    honor += 1
                elif self.enemy == master3:
                    print("\033[1;34;40m\n \"Absolutely outstanding! Please follow me inside the monastery, and we shall discuss about your performance.\"\033[1;37;40m")
                    honor += 1
                else:
                    print("\033[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\033[1;37;40m")
                    print("\n \033[1;33;40m"+str(self.enemy.name)+ "\033[1;37;40m has been added to your discard pile.")
                input("\n Press enter to continue.\n") 
                break
            else:
                if len(hand) == 0:
                    self.enemy.show()
                    printLine()
                    print("\033[1;32;40m YOUR HAND:\033[1;37;40m")
                    print(" You have no cards in your hand!")
                    printLine()
                else:
                    self.enemy.show()
                    printLine()
                    print("\033[1;32;40m YOUR HAND:\033[1;37;40m")
                    for x in hand:
                        x.show()
                print("\n Your current might is \033[1;31;40m"+str(dam)+"\033[1;37;40m/\033[1;31;40m"+str(self.enemy.val)+"\033[1;37;40m.")
                print(" Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
                pluralc = "s"
                plurald = "s"
                if len(pile) == 1:
                    pluralc = ""
                if len(discard) == 1:
                    plurald = ""
                print(" You currently have \033[1;33;40m" + str(len(pile))+" \033[1;37;40mcard"+pluralc+" remaining in your draw pile, and \033[1;33;40m"+ str(len(discard))+" \033[1;37;40mcard"+plurald+" remaining in your discard pile.")
                if insp > 0:
                    print(" You have \033[1;32;40m"+str(insp)+"\033[1;37;40m/\033[1;32;40m"+str(self.enemy.draw)+"\033[1;37;40m Inspiration remaining.")
                else:
                    print(" \033[1;31;40m⚠\033[1;37;40m You have spent all your Inspiration! You will lose \033[1;33;40m1\033[1;37;40m HP per additional card draw.")
            choice = input("\n Please type what you wish to do next:\n")
            choice.lower()
            if choice == "draw" or choice == "d":
                if len(pile) > 0:
                    draw = pile.pop()
                    hand.append(draw)
                    if insp > 0:
                        insp -= 1
                        continue
                    else:
                        HP -= 1
                        if HP <= 0:
                            printLine()
                            print("\033[1;34;40m My mind is pained with the struggle of creativity")
                            print(" I keep looking for something new to paint, but nothing comes to mind")
                            print(" Perhaps this dream was all for naught")
                            print(" Perhaps I was never meant to be an artist")
                            print(" It is now time to wake up")
                            print(" I open my eyes")
                            print(" And find myself sitting still")
                            print(" With an empty canvas standing before me")
                            printLine()
                            input(" Game over. Press enter to terminate the program.\n")
                            exit()
                        continue
                else:
                    printLine()
                    print("\033[1;34;40m I have turned the final page of my sketchbook")
                    print(" Now is a good opportunity to add the new drawings I have learned")
                    print(" In the last few steps of my journey")
                    print(" But in the murky depths of my soul")
                    print(" Something which I have been struggling to conceal")
                    print(" Emerges from the darkness")
                    print(" And finds its way into my sketchbook")
                    printLine()
                    pile += discard
                    discard.clear()
                    ohno = Flaw.pop(0)
                    pile.append(ohno)
                    random.shuffle(pile)
                    input("\n Press enter to continue.\n")
                    if len(pile) > 0:        
                        draw = pile.pop()
                        hand.append(draw)
                        continue
                    elif len(pile) == 0:
                        printLine()
                        print(" There are no cards left in your draw pile!")
                        printLine()
                    if len(pile)+len(hand)+len(discard) == 0:
                        printLine()
                        print(" \033[1;34;40mMy sketchbook is somehow empty")
                        print(" Returned to nothing")
                        print(" As consequence for my destructive whims")
                        print(" Nothing can be done now")
                        print(" I open my eyes")
                        print(" And find myself sitting still")
                        print(" With an empty canvas standing before me")
                        printLine()
                        input(" Game over. Press enter to terminate the program.\n")
                        exit()
            elif choice == "forget" or choice == "f":
                HP -= (self.enemy.val-dam)
                self.enemy.show()
                printLine()
                ############################################################################################### EFFETS FORGET AVANT
                if spider in hand:
                    HP -= 2
                snake.val = 0
                if self.enemy.name == "The Monkey":
                    discard.append(monkeysteal)
                stag.val = -5
                crane.val = -2
                if self.enemy.name == "The Mantis":
                    HP += insp
                if self.enemy.name == "The Wolf" and len(hand) > 0:
                    random.shuffle(hand)
                    wolfremove = hand.pop()
                    print("\n "+str(wolfremove.name)+" has been removed from your deck. (The Wolf)\n")
                if dusk in hand:
                    HP -= 1
                    random.shuffle(hand)
                    duskremove = hand.pop()
                    print("\n "+str(duskremove.name)+" has been removed from your deck. (The Dusk)\n")
                ############################################################################################### EFFETS FORGET AVANT
                for x in hand:
                    x.show()
                    x.use = ""
                if HP <= 0:
                    printLine()
                    print(" \033[1;34;40mThis creature is far too strong")
                    print(" My artistic prowess is incapable of impressing it")
                    print(" I feel like every single one of my thoughts")
                    print(" Is being absorbed into a bottomless void")
                    print(" I see it is time to wake up at last")
                    print(" I open my eyes")
                    print(" And find myself sitting still")
                    print(" With an empty canvas standing before me")
                    printLine()
                    input(" Game over. Press enter to terminate the program.\n")
                    exit()
                print("\033[1;34;40m\n Perhaps not all things are meant to be painted. Surely, some of my sketches must be flawed.\033[1;37;40m")
                if self.enemy.val-dam == 1:
                    print("\n You have lost \033[1;33;40m"+str(self.enemy.val-dam)+ "\033[1;37;40m health point. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m.")
                else:
                    print("\n You have lost \033[1;33;40m"+str(self.enemy.val-dam)+ "\033[1;37;40m health points. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m.")
                input("\n Press enter to continue.\n")
                hand.sort(key=CardValueSort)
                forget = (self.enemy.val-dam)
                while forget > 0:
                    if choice == "The " or len(hand) == 0:
                        okay = False
                    print("\033[1;34;40m\n Using my lost life essence, I shall burn away some of these worthless scribbles.\033[1;37;40m")
                    for x in hand:
                        x.show()
                    if forget == 1:
                        selectF = input("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more card. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                    else:
                        selectF = input("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more cards. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                    selectF = selectF.title()
                    if selectF == "C":
                        selectF = "The Canvas"
                    if (not selectF.startswith("The")) and (("Yellow") not in selectF) and (("Blue") not in selectF) and (("Red") not in selectF):
                        selectF = "The " + selectF
                    if selectF == "The Exit":
                        discard += hand
                        hand.clear()
                        break
                
                    for x in hand:
                        if "Flaw" in x.effect and forget <= 1 and selectF == x.name:
                            printLine()
                            print(" Error: You do not have enough cards left to forget to select a \033[1;31;40mFlaw\033[1;37;40m!")
                            printLine()
                            break
                        if selectF == x.name:
                            hand.remove(x)
                            if "Flaw" in x.effect and forget > 1:
                                forget -= 2
                            else:
                                forget -= 1
                            okay = True
                            break
                        else:
                            okay = False
                            continue
                        if okay == False:
                            printLine()
                            print(" Error: Invalid card name selected. Please type the name of the card you wish to forget(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                            printLine()
                        
                        continue
                ############################################################################################### EFFETS FORGET APRÈS
                if turtle in hand:
                    hand.remove(turtle)
                    pile.append(turtle)
                ############################################################################################### EFFETS FORGET APRÈS
                discard += hand
                hand.clear()
                if self.enemy == master1:
                    printLine()
                    print("\033[1;34;40m \"Hmm, this is concerning. Perhaps you just weren't warmed up yet.\"")
                    printLine()
                elif self.enemy == master2:
                    printLine()
                    print("\033[1;34;40m \"What is this? Gather your equipment, and prove that you are worthy of my teachings!\"")
                    printLine()
                elif self.enemy == master2:
                    printLine()
                    print("\033[1;34;40m \"This final trial was intended to be difficult. I am disappointed, but not surprised. Follow me inside the monastery, and we shall discuss of your performance.\"")
                    printLine()
                else:
                    printLine()
                    print("\033[1;34;40m Now that my spirit feels lightened, I am ready to resume my journey.")
                    printLine()
                input("\n Press enter to continue.\n")
                
                break
            else:
                choice = choice.title()
                if (not choice.startswith("The")) and (("Yellow") not in choice) and (("Blue") not in choice) and (("Red") not in choice):
                    choice = "The " + choice
                if choice == "The " or len(hand) == 0:
                    good = False
                for x in hand:
                    if choice == x.name:
                        good = True
                        eff = x.effect
                        if self.enemy.name == "The Crow":
                            hand.remove(x)
                            discard.append(x)
                        if x.use == "- \033[1;31;40mUSED\033[1;37;40m":
                            printLine()
                            print(" This card's effect has already been used!")
                            break
                        if "Heal" in eff:
                            HP += x.heal
                            x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                        if x.name == "The Snake":
                            HP -= 1
                            x.val += 1
                        if "Forget" in eff:
                            forgetcount = x.forget
                            while forgetcount > 0:
                                if choice == "The " or len(hand) == 0:
                                    okay3 = False
                                printLine()
                                for x in hand:
                                    x.show()
                                if forgetcount == 1:
                                    print("\n You may forget \033[1;33;40m1\033[1;37;40m more card.\n")
                                else:
                                    print("\n You may forget \033[1;33;40m"+str(forgetcount)+"\033[1;37;40m more cards.\n")
                                printLine()
                                selectE = input(" Type the name of the card you wish to forget.\n")
                                selectE = selectE.title()
                                if selectE == "C":
                                    selectE = "The Canvas"
                                if (not selectE.startswith("The")) and (("Yellow") not in selectE) and (("Blue") not in selectE) and (("Red") not in selectE):
                                    selectE = "The " + selectE
                                for t in hand:
                                    if selectE == t.name:
                                        hand.remove(t)
                                        forgetcount -= 1
                                        okay3 = True
                                        break
                                    else:
                                        okay3 = False
                                        continue
                                if okay3 == False:
                                    printLine()
                                    print(" Error: Invalid card name selected. Please type the name of the card you wish to discard(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                            x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                        if "Discard" in eff:
                            discardcount = x.discard
                            while discardcount > 0:
                                if choice == "The " or len(hand) == 0:
                                    okay2 = False
                                printLine()
                                for x in hand:
                                    x.show()
                                if discardcount == 1:
                                    print("\n You may discard \033[1;33;40m1\033[1;37;40m more card.\n")
                                else:
                                    print("\n You may discard \033[1;33;40m"+str(discardcount)+"\033[1;37;40m more cards.\n")
                                printLine()
                                selectD = input(" Type the name of the card you wish to discard.\n")
                                selectD = selectD.title()
                                if selectD == "C":
                                    selectD = "The Canvas"
                                if (not selectD.startswith("The")) and (("Yellow") not in selectD) and (("Blue") not in selectD) and (("Red") not in selectD):
                                    selectD = "The " + selectD
                                for t in hand:
                                    if selectD == t.name:
                                        dis = hand.remove(t)
                                        discard.append(dis)
                                        discardcount -= 1
                                        okay2 = True
                                        break
                                    else:
                                        okay2 = False
                                        continue
                                if okay2 == False:
                                    printLine()
                                    print(" Error: Invalid card name selected. Please type the name of the card you wish to discard(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                            x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                        if "Draw" in eff:
                            if len(pile) >= x.draw:
                                urdraw = "h" * x.draw
                                for h in urdraw:
                                    draw = pile.pop()
                                    hand.append(draw)
                                x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                                break
                            else:
                                printLine()
                                print("\033[1;34;40m I have turned the final page of my sketchbook")
                                print(" Now is a good opportunity to add the new drawings I have learned")
                                print(" In the last few steps of my journey")
                                print(" But in the murky depths of my soul")
                                print(" Something which I have been struggling to conceal")
                                print(" Emerges from the darkness")
                                print(" And finds its way into my sketchbook")
                                printLine()
                                pile += discard
                                discard.clear()
                                ohno = Flaw.pop(0)
                                pile.append(ohno)
                                random.shuffle(pile)
                                input("\n Press enter to continue.\n")
                                if len(pile) >= x.draw:
                                    urdraw = "h" * x.draw
                                    for h in urdraw:
                                        draw = pile.pop()
                                        hand.append(draw)
                                    x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                                    break
                                elif len(pile) == 0:
                                    printLine()
                                    print(" There are no cards left in your draw pile!")
                                    printLine()
                                if len(pile)+len(hand)+len(discard) == 0:
                                    printLine()
                                    print(" \033[1;34;40mMy sketchbook is somehow empty")
                                    print(" Returned to nothing")
                                    print(" As consequence for my destructive whims")
                                    print(" Nothing can be done now")
                                    print(" I open my eyes")
                                    print(" And find myself sitting still")
                                    print(" With an empty canvas standing before me")
                                    printLine()
                                    input(" Game over. Press enter to terminate the program.\n")
                                    exit()
                        else:
                            printLine()
                            print(" This card does not have a usable active effect!")
                            break
                        
                    else:
                        good = False
                        continue
                if good == False:
                    printLine()
                    print(" Error: Invalid action selected. Please type \"d\" to draw a card, \"forget\" to abandon this combat, or type the name of the card you wish to use.")
                continue
        if self.location == "Monastery":
            EncounterM()

def EncounterM():
    global room
    global HP
    global pile
    global discard
    if room == 0:
        random.shuffle(fight1pool)
        x = fight1pool.pop()
        y = fight1pool.pop()
        if len(pile) > 0:
            for o in pile:
                if "Flaw" in o.effect:
                    craneE.val +=1
        if len(discard) > 0:    
            for o in discard:
                if "Flaw" in o.effect:
                    craneE.val +=1
        printLine()
        print("\033[1;34;40m As my first steps scatter the red leaves across the soil")
        print(" I find myself inspired by the statues surrounding the trail")
        print(" Surely they would not mind appearing in a painting or two")
        print(" Who shall I paint first?\033[1;37;40m")
        printLine()
        print("\n Paintings remaining before next event: \033[1;33;40m5\033[1;37;40m\n")
        input(dialogs["pause"])
        x.show()
        y.show()
        printLine()
        print("[1] "+ x.name)
        print("[2] " + y.name)
        encount1 = input("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            printLine()
            print(" Error: Invalid option selected. Selecting random encounter...")
            encount1 = random.randint(1,2)
            if encount1 == 1:
                fight1pool.append(y)
                fight = Encounter(x, "Monastery")
                fight.Fight()
            elif encount1 == 2:
                fight1pool.append(x)
                fight = Encounter(y, "Monastery")
                fight.Fight()
    elif room > 0 and room < 5:
        craneE.val = 0
        if len(pile) > 0:
            for o in pile:
                if "Flaw" in o.effect:
                    craneE.val +=1
        if len(discard) > 0:    
            for o in discard:
                if "Flaw" in o.effect:
                    craneE.val +=1
        random.shuffle(fight1pool)
        x = fight1pool.pop()
        y = fight1pool.pop()
        v = x.name
        w = y.name
        printLine()
        print("\033[1;34;40m I continue my path towards the monastery")
        print(" Breathing calmly the fresh air of the forest")
        print(" Perhaps I should enjoy this moment of peace")
        print(" And paint a few more statues along the way.\033[1;37;40m")
        printLine()
        print("\n Paintings remaining before next event: \033[1;33;40m"+str(5-room)+"\033[1;37;40m\n")
        input(dialogs["pause"])
        x.show()
        y.show()
        printLine()
        print("[1] "+ v)
        print("[2] " + w)
        encount1 = input("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            printLine()
            print(" Error: Invalid option selected. Selecting random encounter...")
            encount1 = random.randint(1,2)
            if encount1 == 1:
                fight1pool.append(y)
                fight = Encounter(x, "Monastery")
                fight.Fight()
            elif encount1 == 2:
                fight1pool.append(x)
                fight = Encounter(y, "Monastery")
                fight.Fight()
    elif room == 5:
        printLine()
        print("\033[1;34;40m I have reached the middle of my journey in the Autumn Monastery")
        print(" I have encountered some of its denizens, and I shall surely see a few more before arriving at my destination")
        print(" My mind is flowing with ideas for new sketches")
        print(" But my body is feeling tired and exhausted")
        print(" Perhaps some rest is in order")
        print(" I notice two stone benches standing aside the path, make myself comfortable, and begin breathing calmly")
        print(" Crimson leaves fall all around me, and small rays of light piercing through the foliage illuminate the scenery")
        print(" A monk dressed in bright red garnments exits the monastery, and begins walking down the path towards me")
        print(" She sits on the second bench, closes her eyes, and speaks")
        print(" \"You have done well, Disciple of the Master\"")
        print(" \"You have seen five of our guardians, and learned that not all things are meant to be kept forever\"")
        print(" \"You seek inspiration at the very bottom of your dreams, correct?\"")
        print(" \"The dangers standing in your path are not trivial\"")
        print(" \"But you need not worry about that for now. Breathe, and rest.\"")
        printLine()
        print(" Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
        print("[1] \033[1;32;40mBreathe\033[1;37;40m (Heal 5 HP)")
        print("[2] \033[1;31;40mDraw\033[1;37;40m (Challenge the Acolyte)")
        if len(pile) == 1:
            print("[3] \033[1;36;40mReflect\033[1;37;40m (Shuffle your discard pile back into your draw pile without adding a \033[1;31;40mFlaw\033[1;37;40m, and forget up to 3 cards in your deck. You currently have \033[1;33;40m" + str(len(pile))+" \033[1;37;40mcard remaining in your draw pile.)")
        else:
            print("[3] \033[1;36;40mReflect\033[1;37;40m (Shuffle your discard pile back into your draw pile without adding a \033[1;31;40mFlaw\033[1;37;40m, and forget up to 3 cards in your deck. You currently have \033[1;33;40m" + str(len(pile))+" \033[1;37;40mcards remaining in your draw pile.)")
        printLine()
        eventchoice = input(" Please enter the number corresponding to your choice to proceed:\n")
        if eventchoice == "1":
            HP += 5
            printLine()
            print("\033[1;34;40m \"Excellent. Feel the air traverse your lungs. Be refreshed, Disciple.\"")
            print(" \"Alas, not all things are meant to last forever, as you have learned\"")
            print(" \"Our Master is eager to put you to the test\"")
            print(" \"May you remember all we have taught you as you journey onwards\"")
            print(" I turn to look at the monk and say goodbye, but she has already disappeared.")
            printLine()
            print(" You have gained 5 health points. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
            room += 1
            input(dialogs["pause"])
            EncounterM()
        elif eventchoice == "2": # Combattre le Acolyte
            fight = Encounter(acolyteE, "Monastery")
            fight.Fight()
        elif eventchoice == "3":
            pile += discard
            discard.clear()
            forget = 3
            while forget > 0:
                print("\033[1;34;40m\n As I listen to the bright red leaves hitting the soil, I lose myself in my thoughts.\033[1;37;40m")
                for x in pile:
                    x.show()
                if forget == 1:
                    selectF = input("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more card. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                else:
                    selectF = input("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more cards. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                selectF = selectF.title()
                if selectF == "C":
                    selectF = "The Canvas"
                if (not selectF.startswith("The")) and (("Yellow") not in selectF) and (("Blue") not in selectF) and (("Red") not in selectF):
                    selectF = "The " + selectF
                if selectF == "The Exit":
                    break
                
                for x in pile:
                    if "Flaw" in x.effect and forget <= 1 and selectF == x.name:
                        printLine()
                        print(" Error: You do not have enough cards left to forget to select a \033[1;31;40mFlaw\033[1;37;40m!")
                        printLine()
                        break
                    if selectF == x.name:
                        pile.remove(x)
                        if "Flaw" in x.effect and forget > 1:
                            forget -= 2
                        else:
                            forget -= 1
                        okay = True
                        break
                    else:
                        okay = False
                        continue
                    if okay == False:
                        printLine()
                        print(" Error: Invalid card name selected. Please type the name of the card you wish to forget(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                        printLine()
                    
                    continue
            printLine()
            print("\033[1;34;40m \"Is simply resting so difficult for you?\"")
            print(" \"I see an Artist's mind never slumbers\"")
            print(" \"Very well then\"")
            print(" \"I am eager to see how this dedication will help you in the rest of your journey\"")
            print(" I turn to look at the monk and say goodbye, but she has already disappeared.")
            printLine()
            room += 1
            input(dialogs["pause"])
            EncounterM()
        else:
            printLine()
            print("\033[1;34;40m \"You don't know what to choose?\"")
            print("\033[1;34;40m \"I understand. In such a foreign land, so far away from home...\"")
            print("\033[1;34;40m \"Finding rest can be rather difficult\"")
            print("\033[1;34;40m \"Here, compare your breathing with a flower\"")
            print("\033[1;34;40m \"Opening and closing itself as the day and night chase each other\"")
            print("\033[1;34;40m \"Excellent.\"")
            print(" After practicing the monk's exercise for a few minutes, I turn my head to thank her, but she has already disappeared.")
            printLine()
            HP += 5
            print(" You have gained 5 health points. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
            room += 1
            input(dialogs["pause"])
            EncounterM()
    elif room == 6:
        craneE.val = 0
        if len(pile) > 0: 
            for o in pile:
                if "Flaw" in o.effect:
                    craneE.val +=1
        if len(discard) > 0:
            for o in discard:
                if "Flaw" in o.effect:
                    craneE.val +=1
        random.shuffle(fight1pool)
        x = fight1pool.pop()
        y = fight1pool.pop()
        v = x.name
        w = y.name
        printLine()
        print("\033[1;34;40m After this rather enriching encounter with my first human being in this strange land")
        print(" I leave the stone bench behind, grateful for this opportunity to stop for a moment")
        print(" It is time to press on")
        print(" And paint a few more statues along the way.\033[1;37;40m")
        printLine()
        print("\n Paintings remaining before meeting the Master: \033[1;33;40m"+str(11-room)+"\033[1;37;40m\n")
        input(dialogs["pause"])
        x.show()
        y.show()
        printLine()
        print("[1] "+ v)
        print("[2] " + w)
        encount1 = input("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            printLine()
            print(" Error: Invalid option selected. Selecting random encounter...")
            encount1 = random.randint(1,2)
            if encount1 == 1:
                fight1pool.append(y)
                fight = Encounter(x, "Monastery")
                fight.Fight()
            elif encount1 == 2:
                fight1pool.append(x)
                fight = Encounter(y, "Monastery")
                fight.Fight()
    elif room > 6 and room < 11:
        craneE.val = 0
        if len(pile) > 0:
            for o in pile:
                if "Flaw" in o.effect:
                    craneE.val +=1
        if len(discard) > 0:    
            for o in discard:
                if "Flaw" in o.effect:
                    craneE.val +=1
        random.shuffle(fight1pool)
        x = fight1pool.pop()
        y = fight1pool.pop()
        v = x.name
        w = y.name
        printLine()
        print("\033[1;34;40m With every step I take, the monastery grows closer")
        print(" Soon, I shall meet the Master, and put all I have learned to the test")
        print(" If I succeed")
        print(" I am certain that great insight will be granted upon me")
        print(" For now, I cannot resist attempting to paint a few more of these beautiful statues.")
        printLine()
        print("\n Paintings remaining before meeting the Master: \033[1;33;40m"+str(11-room)+"\033[1;37;40m\n")
        input(dialogs["pause"])
        x.show()
        y.show()
        printLine()
        print("[1] "+ v)
        print("[2] " + w)
        encount1 = input("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            printLine()
            print(" Error: Invalid option selected. Selecting random encounter...")
            encount1 = random.randint(1,2)
            if encount1 == 1:
                fight1pool.append(y)
                fight = Encounter(x, "Monastery")
                fight.Fight()
            elif encount1 == 2:
                fight1pool.append(x)
                fight = Encounter(y, "Monastery")
                fight.Fight()
    elif room == 11:
        boss = 1
        printLine()
        print("\033[1;34;40m At last")
        print(" I have travelled down the path of statues")
        print(" And I now find myself at the gates of the monastery")
        print(" But just as I prepare to open the doors and see what lies inside")
        print(" I feel a hand lay down on my right shoulder")
        print(" \"Not yet, Disciple. You have one more test to pass.\"")
        printLine()
        input(dialogs["pause"])
        printLine()
        print(" \033[1;34;40mI turn around and see a man draped in bright red clothing, decorated with the images of a variety of animals")
        print(" I recognize every single one of them as one of the statues I have encountered in this eventful beginning of my journey")
        print(" In fact, all of them but one")
        print(" Before I can get a closer look at it, the Master bows and blocks my view of the unfamiliar figure")
        print(" \"You have stayed in our humble grove for so little time\"")
        print(" \"And yet you have learned so much\"")
        print(" \"It is now time to put all the knowledge you have acquired to the test\"")
        print(" \"Please save your questions for later\"")
        print(" \"And face me, the Master of the Autumn Monastery, Sculptor of Statues.\"")
        printLine()
        input(" Press enter to open your sketchbook and FIGHT.\n")
        fight = Encounter(master1, "Monastery")
        fight.Fight()
    elif room == 12:
        fight = Encounter(master2, "Monastery")
        fight.Fight()
    elif room == 13:
        fight = Encounter(master3, "Monastery")
        fight.Fight()
    elif room == 14:
        ending()

def ending():
    boss = 0
    printLine()
    print("\n".join(dialogs["monastery"]["ending"]["text1"]))
    printLine()
    input(" Press enter to receive the results of your evaluation.\n")

    # You can do 0 > honor > 3 in python, but I don't recommand, 
    # since other languages will execute this from left to right
    # so 0 > honor will return, and then true > 3 will be executed, which isn't what we want
    if honor < 0 or honor > 3:
        raise GameError("You're not supposed to have more than 3 honor points")

    printLine()
    print("\n".join(dialogs["monastery"]["ending"][f"honor{honor}"]))
    printLine()
    if honor == 0:
        input(" Game over. Press enter to terminate the program.\n")
        exit()
    elif honor != 1:
        discard.append(master)

    input(dialogs["pause"])

    printLine()
    print("\n".join(dialogs["monastery"]["ending"]["text1"]))
    printLine()

    # this part should be in the world selection
    print("[1] \033[1;33;40m The Golden Hive")
    print("\033[1;37;40m[2] \033[1;35;40m The Theatre of Virtuosos")
    dest1 = input("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")

    raise NotImplementedError

class GameError(Exception):
    pass

if __name__ == "__main__":
    mainmenu()
