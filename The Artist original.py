# -*- coding: utf-8 -*-
import random # Praise RNGesus

# TO DO LIST
# 
# 
#
#
# 
#
# 
# 
# 
# 
godmode = False

room = 0
HP = 20
honor = 0
boss = 0
class Card:
    def __init__(self, name, val, effect, heal, draw, discard, forget, use):
        self.name = name # Nom de la carte
        self.val = val # Valeur numérique de la carte
        self.effect = effect # Effet de la carte
        self.heal = heal
        self.draw = draw
        self.use = use
        self.discard = discard
        self.forget = forget
    def show(self):
        if self.val > 0: #Valeurs positives en vert
            print (" {} (\033[1;32;40m{}\033[1;37;40m) - {} {}".format(self.name, self.val, self.effect, self.use))
        elif self.val == 0: #Valeurs de 0 en jaune
            print (" {} (\033[1;33;40m{}\033[1;37;40m) - {} {}".format(self.name, self.val, self.effect, self.use))
        else: #Valeurs négatives en rouge
            print (" {} (\033[1;31;40m{}\033[1;37;40m) - {} {}".format(self.name, self.val, self.effect, self.use))


hand = []
discard = []

handlength = 0

shamed = Card("The Shamed", -2, "Flaw. No effect.", 0, 0,0,0, "")
dusk = Card("The Dusk", -1, "Flaw. At the end of this combat, forget a random card in your hand and lose 1 HP.",0,0,0,0,"")

desperate = Card("The Desperate", 0, "Flaw. No effect.", 0, 0,0,0, "")
deceased = Card("The Deceased", -99, "Flaw. At the end of this combat, die.", 0, 0,0,0, "")

superFlaw = [desperate]
Flaw = [shamed, dusk]
random.shuffle(Flaw)
random.shuffle(superFlaw)
for x in superFlaw:
    Flaw.append(x)
for x in range (50):
    Flaw.append(deceased)
# Heal, draw, discard, forget
red = Card("Red", 2, "No effect.", 0, 0,0,0, "")
blue = Card("Blue", 0, "Heal 2 HP.", 2, 0,0,0, "\033[1;32;40m*\033[1;37;40m")
yellow = Card("Yellow", 1, "Draw 1 card.", 0, 1,0,0, "\033[1;32;40m*\033[1;37;40m")
beginning = Card("The Beginning", 1, "No effect.", 0, 0,0,0, "")
dawn = Card("The Dawn", 2, "Heal 2 HP. Draw 2 cards.", 2, 2,0,0, "\033[1;32;40m*\033[1;37;40m")
canvas = Card("The Canvas" , 0, "No effect.",0 ,0,0,0, "")

tiger = Card("The Tiger", 0, "This card's value begins at 0, and increases by 1 for every 2 cards in your hand.",0 ,0,0,0, "")
stag = Card("The Stag", -5, "This card's value increases by 1 for every card in your hand.", 0,0,0,0, "")
dragon = Card ("The Dragon", 4, "No effect.",0,0,0,0,"")
snake = Card("The Snake", 0, "Reusable. Lose 1 HP. For this combat, this card's value increases by 1.",0,0,0,0,"\033[1;32;40m*\033[1;37;40m")
rabbit = Card ("The Rabbit", 0, "Discard 2 cards. Draw 2 cards.",0,2,2,0,"\033[1;32;40m*\033[1;37;40m")
leopard = Card("The Leopard", 1, "Draw 1 card.",0,1,0,0,"\033[1;32;40m*\033[1;37;40m")
swan = Card("The Swan", 0, "This card value's is 0. If this is the only card in your hand, the value of this card becomes 4.", 0,0,0,0,"")
crane = Card("The Crane", -2, "This card's value increases by 2 for every card with a negative value in your hand.",0,0,0,0,"")
turtle = Card ("The Turtle", 1, "At the end of this combat, put this card back in your draw pile.",0,0,0,0,"")
mantis = Card ("The Mantis",2,"Heal 1 HP.",1,0,0,0,"\033[1;32;40m*\033[1;37;40m")
wolf = Card("The Wolf", 3, "Forget 1 card.",0,0,0,1,"\033[1;32;40m*\033[1;37;40m")
monkey = Card("The Monkey", 2,"If the enemy you are facing has a might value equal to or greater than 10, gain 1 bonus inspiration when this card is drawn.",0,0,0,0,"")
spider = Card("The Spider", 3, "At the end of this combat, lose 2 HP.", 0,0,0,0,"")
crow = Card("The Crow", 2, "Discard 1 card.",0,0,1,0,"\033[1;32;40m*\033[1;37;40m")
frog = Card("The Frog", 0, "Forget 1 card.", 0,0,0,1,"\033[1;32;40m*\033[1;37;40m")

acolyte = Card("The Acolyte", 2, "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.",0,0,0,0,"")
master = Card("The Acolyte", 2, "While this card is in your hand, increase the value of all cards containing the name of an animal by 1.",0,0,0,0,"")
# Deck du joueur initial, sera modifié par après
pile = [red, yellow, blue, dawn, canvas, canvas, canvas, canvas, canvas, canvas, canvas, beginning, beginning]


random.shuffle(pile) # shuffle initial

animalpool = [tiger, stag, dragon, snake, rabbit, leopard, swan, crane, turtle, mantis, wolf, monkey, spider, crow, frog]

monkeycom = False #effet de l'ennemi monkey
moncom = False #effet de la carte monkey

class Enemy:
    def __init__(self, name, val, draw, effect, reward, desc):
        self.name = name
        self.val = val
        self.effect = effect
        self.draw = draw
        self.reward = reward
        self.desc = desc
    def show(self):
        print ("=================================================\n \033[1;36;40m{}\033[1;37;40m\n Might: \033[1;31;40m{}\033[1;37;40m\n Inspiration: \033[1;32;40m{}\033[1;37;40m\n Effects: \033[1;33;40m{}\033[1;37;40m\n \n \033[1;34;40mREWARD:\033[1;37;40m".format(self.name, self.val, self.draw, self.effect))
        self.reward.show()
    def introduce(self):
        print ("{}".format(self.desc))
#might, inspiration
tigerE = Enemy("The Tiger", 4, 4, "No effects.", tiger, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a ferocious striped beast\n Whose savagery would no doubt be a great addition to my sketchbook\n I can hear its callous, uncaring voice\n \"Another Disciple of the Master?\"\n \"Perhaps your remains will be tastier than the last\"\n \"Your defeat is inevitable\"\n \"This grove shall be the last thing you see.\"")
swanE = Enemy("The Swan", 0, 0, "No effects.", swan, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a magnificent white bird\n Whose silhouette would no doubt be a great addition to my sketchbook\n I can hear its beautiful signing voice\n \"My power is unmatched and my beauty without equal\"\n \"You appear to be a rather talented Artist\"\n \"Therefore I shall allow you to paint my magnificence without hardships\"\n \"Hurry before I change my mind.\"")
dragonE = Enemy("The Dragon", 10, 5, "Each card in your hand adds 1 to your total might.", dragon, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a formidable red dragon\n Whose power would no doubt be a great addition to my sketchbook\n I can hear its booming, majestic voice\n \"I see you have chosen the path of the Monastery\"\n \"Know that I am the ruler of this grove\"\n \"And that only my Master, who resides inside the monastery, can surpass my prowess\"\n \"Can you, human? Show me what you are capable of.\"")
craneE = Enemy("The Crane", 0, 1, "This enemy's might is equal to the number of Flaw cards you have in your deck.", crane, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a silent, sleeping crane\n Whose placidity would no doubt be a great addition to my sketchbook\n Despite all my attempts to wake it, as I imagine that their beauty would increase tenfold once awoken\n The crane remains mute\n As I nervously unpack my painting tools\n I worry that the crane may be dreaming of me, and of what perils I may encounter on my journey.")
leopardE = Enemy("The Leopard", 2, 3, "You may not have more than 3 cards in your hand. Exceeding this limit will cause a random card to be discarded.", leopard, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a swift spotted feline\n Whose alacrity would no doubt be a great addition to my sketchbook\n I can hear its growling, threatening voice\n \"Dear Artist, how about a race?\"\n \"I will chase, and you shall run\"\n \"Can your legs keep up?\"\n \"If they do, I will allow you to paint me, and perhaps learn that speed over carefulness is sometimes your best bet.\"")
snakeE = Enemy("The Snake", 1, 1, "No effects.", snake, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a slithering, scaly snake\n Whose elusiveness would no doubt be a great addition to my sketchbook\n I can hear its hissing, rattling voice\n \"Ssso, human, you have chosen me as the sssubject of your next creation?\"\n \"I am flattered, but alssso sssurprised\"\n \"Please, take a ssseat, and don't forget a single detail of my glissstening ssscalesss.\"")
monkeyE = Enemy("The Monkey", "?", 1, "This enemy's might is equal to the value of a random card taken away from your deck. The card will be put back at the end of the combat.", monkey, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a joyful, smiling monkey\n Whose mischief would no doubt be a great addition to my sketchbook\n As I prepare my painting tools, I notice one of the pages bearing one of my previous creations has vanished\n I can hear its playful, high-pitched voice\n \"Teehee! It's mine now!\"\n \"Surely I am beautiful enough to replace it. Go on, paint me, Artist.\"\n \"Teehee!\"")
stagE = Enemy("The Stag", 2, 3, "No effects.", stag, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a noble, venerable stag\n Whose stature would no doubt be a great addition to my sketchbook\n I can hear its deep, respectful voice\n \"Disciple of the Master, you walk among our garden\"\n \"Be respectful of all those who have come before you\"\n \"As each of your steps flatten the soil of our great Monastery.\"")
mantisE = Enemy("The Mantis", 3, 3, "Each unused point of inspiration after this combat heals you for 1 HP.", mantis, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the calming statue of a praying mantis\n Whose serenity would no doubt be a great addition to my sketchbook\n I can hear its tranquil whispers\n \"Breathe deeply, Artist.\"\n \"Through anger lies failure, through focus lies success\"\n \"If you show me that you have learned well\"\n \"Then you may draw me in that sketchbook of yours and find serenity.\"")
wolfE = Enemy("The Wolf", 4, 4, "If you lose this combat, forget a random card in your hand.", wolf, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the fearsome statue of a gray wolf\n Whose frightening presence would no doubt be a great addition to my sketchbook\n I can hear its intimidating, growling voice\n \"Artist, prepare for one of the greatest challenges of the beginning of your journey\"\n \"Prove your skill and might\"\n \"If you prevail, I will be glad to join your sketchbook\"\n \"And perhaps devour some of its inhabitants along the way.\"")
rabbitE = Enemy("The Rabbit",0,0,"No effects.", rabbit, "\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a small, adorable rabbit\n Whose fluffiness would no doubt be a great addition to my sketchbook\n I can hear its soft chirping voice\n \"Greetings, good Artist\"\n \"My body is small and weak and cannot forbid you from drawing it\"\n \"As you paint the outline of my frail shape\"\n \"Please remember this moment of calm before the storm.\"")
turtleE = Enemy ("The Turtle",2,2,"No effects.",turtle,"\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a sturdy, venerable turtle\n Whose resilience would no doubt be a great addition to my sketchbook\n I can hear its old, raspy voice\n \"For countless years, I have seen many of your kind walk in this grove\"\n \"Some have fallen, some have thrived\"\n \"No matter how well you succeed\"\n \"I will remain here for many more years, and I shall remember them all\"")
spiderE = Enemy("The Spider",0,0,"No effects.",spider,"\033[1;37;40m=================================================\n\033[1;34;40m I stand before the tiny sculpture of a green spider\n Interested by this peculiar piece of artwork\n I decide to bring it along on my journey\n And paint the outline of this odd creature\n In the corner of the first page of my sketchbook.")
crowE = Enemy("The Crow", 2,3,"Whenever you use the active effect of a card, discard it.",crow,"\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a somber, coal-colored crow\n Whose gloominess would no doubt be a great addition to my sketchbook\n I can hear its cackling, monotonous voice\n \"No matter how far you get and what beautiful paintings you come up with\"\n \"Death will come to you, and reduce your body to ash\"\n \"But if you have worked hard\"\n \"Then perhaps your achievements may live on.\"")
frogE = Enemy("The Frog", 1,1,"No effects.",frog,"\033[1;37;40m=================================================\n\033[1;34;40m I stand before the statue of a minuscule, wise frog\n Whose prudence would no doubt be a great addition to my sketchbook\n I can hear its humble, polite voice\n \"You have come far from your home to learn from us\"\n \"If there is only one lesson to remember\"\n \"It is that not all your work is perfect, and that there is no shame in losing some of it.\"")
fight1pool = [tigerE, swanE, dragonE, craneE, leopardE, snakeE, monkeyE, stagE, mantisE, wolfE, rabbitE, turtleE,spiderE,crowE,frogE]

acolyteE = Enemy("The Acolyte", 8,5, "Every card in your hand which contains the name of an animal increases your total might by 1.", acolyte, "\033[1;37;40m=================================================\n\033[1;34;40m \"I can see that the notion of rest is alien to you\"\n \"For you, every situation is yet another painting waiting to be created, is it not?\"\n \"My apologies, dear Artist, but a sketch of me is not granted\"\n \"It is earned.\"\n I open my sketchbook at its first page, as the Acolyte takes on her battle stance.")
master1 = Enemy("The Master \033[1;37;40m(\033[1;32;40m███\033[1;37;40m)", 8, 5, "Every card in your hand which contains the name of an animal increases The Master's total might by 1.", master, "\033[1;37;40m=================================================\n\n \033[1;31;40mROUND 1\n\n \033[1;34;40m\"Each statue I have carved possesses a soul of its own.\"\n \"However, I am, and will always will be their Master\"\n \"To begin your final test, let us see if you have memorized their lessons.\"")
master2 = Enemy("The Master \033[1;37;40m(\033[1;32;40m██\033[1;31;40m█\033[1;37;40m)", 4, 1, "At the end of this combat, heal 1 HP for every point of might exceeding the required total.", master, "\033[1;37;40m=================================================\n\n \033[1;31;40mROUND 2\n\n \033[1;34;40m\"This next battle should be much easier, now that you have acquainted yourself with my fighting style.\"\n \"However, make sure to keep painting to the best of your ability!\"\n \"I like to grant a special reward to disciples who truly manage to exceed my expectations.\"")
master3 = Enemy("The Master \033[1;37;40m(\033[1;32;40m█\033[1;31;40m██\033[1;37;40m)", 10, 3, "At the start of this combat, gain 1 inspiration for every Flaw present in your deck.", master, "\033[1;37;40m=================================================\n\n \033[1;31;40mFINAL ROUND\n\n \033[1;34;40m\"It is time. Show me the true colors of your power!\"\n \"I wish to see every work of art you have crafted in my grove.\"\n \"Even the worst Flaws can be turned into something beautiful by the most proficient students!\"")
def Start(): # Menu principal
    print ("\033[1;37;40m=================================================")
    print (" Please ensure that all of the following words are easily readable. Adjust your color settings if they are not.")
    print (" \033[1;30;47mBlack\033[1;37;40m \033[1;31;40mRed \033[1;32;40mGreen \033[1;33;40mYellow \033[1;34;40mBlue \033[1;35;40mPurple \033[1;36;40mCyan \033[1;37;40mWhite")
    print ("\033[1;37;40m=================================================")
    print ("""\033[1;36;40m  ▄▀▀▀█▀▀▄  ▄▀▀▄ ▄▄   ▄▀▀█▄▄▄▄      ▄▀▀█▄   ▄▀▀▄▀▀▀▄  ▄▀▀▀█▀▀▄  ▄▀▀█▀▄   ▄▀▀▀▀▄  ▄▀▀▀█▀▀▄ 
 █    █  ▐ █  █   ▄▀ ▐  ▄▀   ▐     ▐ ▄▀ ▀▄ █   █   █ █    █  ▐ █   █  █ █ █   ▐ █    █  ▐ 
 ▐   █     ▐  █▄▄▄█    █▄▄▄▄▄        █▄▄▄█ ▐  █▀▀█▀  ▐   █     ▐   █  ▐    ▀▄   ▐   █     
    █         █   █    █    ▌       ▄▀   █  ▄▀    █     █          █    ▀▄   █     █      
  ▄▀         ▄▀  ▄▀   ▄▀▄▄▄▄       █   ▄▀  █     █    ▄▀        ▄▀▀▀▀▀▄  █▀▀▀    ▄▀       
 █          █   █     █    ▐       ▐   ▐   ▐     ▐   █         █       █ ▐      █         
 ▐          ▐   ▐     ▐                              ▐         ▐       ▐        ▐         

""")
    print ("\033[1;37;40m[1] New Game")
    print ("[2] Tutorial")
    print ("[3] Continue")
    print ("[4] Credits")
    print ("\033[1;37;40m=================================================")
    startchoice = input (" Please enter the number corresponding to your choice to proceed:\n")
    if startchoice == "1":
        New()
    elif startchoice == "2":
        Tutorial()
    elif startchoice == "3":
        Continue()
        #rose, lilac, daffodil...
    elif startchoice == "4":
        Credits()
    else:
        print ("\033[1;37;40m=================================================")
        print (" Error: Invalid option selected. Press enter to go back.")
        print ("\033[1;37;40m=================================================")
        input ()
        Start()
def New():
    print ("\033[1;37;40m=================================================")
    print ("\033[1;34;40m I am the Artist")
    print (" From my paintbrush")
    print (" Worlds are created")
    print (" From my palette")
    print (" Creatures are born")
    print (" But this morning")
    print (" I feel empty like the blank canvas standing before me")
    print ("\033[1;37;40m=================================================")
    input (" Press enter to continue.\n")
    print ("\033[1;37;40m=================================================")
    print ("\033[1;34;40m Whenever I feel empty I like to dream")
    print (" Deep in my dreams there is someone who can help")
    print (" The road will be long and tiring")
    print (" But the day is young and so am I")
    New2()
def New2():    
    print ("\033[1;34;40m Where shall I begin my journey?")
    print ("\033[1;37;40m=================================================")
    print ("[1] \033[1;31;40m The Autumn Monastery")
    print ("\033[1;37;40m[2] \033[1;34;40m The Prismatic Observatory")
    dest1 = input ("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
    if dest1 == "1":
        Monastery()
    elif dest1 == "2":
        Observatory()
    else:
        print ("\033[1;37;40m=================================================")
        print (" Error: Invalid option selected.")
        print ("\033[1;37;40m=================================================")
        New2()
def Monastery():
    print ("\033[1;37;40m=================================================")
    print ("\033[1;34;40m I close my eyes")
    print (" I find myself in the clearing of a forest")
    print (" Surrounded by the warm colors of fall")
    print (" A path before me stretches to a great monastery in the distance")
    print (" Many statues watch over the road with great patience")
    print (" I can feel without doubt")
    print (" That the inhabitants of this peculiar place are ready to test my skill and wit")
    print (" If I prevail")
    print (" Then perhaps they shall grant me insight on where to go next.")
    print ("\033[1;37;40m=================================================")
    input (" Press enter to continue.\n")
    EncounterM()
        
def Observatory():
    print ("\033[1;37;40m=================================================")
    print ("\033[1;34;40m I close my eyes")
    print (" I find myself at the base of a great tower")
    print (" Surrounded by the echoing humming of the cosmos")
    print (" At the very summit of the spire")
    print (" I can see without doubt")
    print (" A telescope which shall grant priceless insights")
    print (" On the astral secrets of the universe")
    print (" If I prevail")
    print (" Then perhaps I may use it and plan where to go next.")
    print ("\033[1;37;40m=================================================")
    input (" Press enter to continue.\n")
    Encounter()

def Hive():
    print ("\033[1;37;40m=================================================")
    print ("\033[1;34;40m I close my eyes")
    print (" I find myself in the middle of a bustling city")
    print (" Surrounded by the deafening buzzes of many insect-like humanoids")
    print (" Flies, moths, butterflies, bees and many others alike")
    print (" March, flutter and crawl towards a great palace built atop the walls of the metropolis")
    print (" I can hear without doubt")
    print (" The humming songs chanted by the ruler of the capital")
    print (" If I prevail")
    print (" Then perhaps I may ask the Queen for advice on where to go next")
    print ("\033[1;37;40m=================================================")
    input (" Press enter to continue.\n")
    Encounter()

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
        print ("\033[1;37;40m=================================================")
        input (" Press enter to continue.\n")
        insp = self.enemy.draw
        global HP
        global honor
        global room
        global monkeycom
        global moncom
        room += 1
        mastercom = False
        while True:
            dam = 0
            handlength = len(hand)
            ############################################################################################### EFFETS DÉPART
            tiger.val = int(handlength/2) # tiger effect
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
                print ("\033[1;37;40m=================================================")
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
                    print ("\n "+str(duskremove.name)+" has been removed from your deck. (The Dusk)")
                if self.enemy == master2 and dam > self.enemy.val:
                    HP += dam-self.enemy.val
                ############################################################################################### EFFETS VICTOIRE
                discard += hand
                hand.clear()
                if self.enemy == master1:
                    print ("\033[1;34;40m\n \"Excellent work, disciple! However, I am only getting started...\033[1;37;40m")
                    honor += 1
                elif self.enemy == master2:
                    print ("\033[1;34;40m\n \"How splendid! It seems you are ready for your true ultimate trial.\"\033[1;37;40m")
                    honor += 1
                elif self.enemy == master3:
                    print ("\033[1;34;40m\n \"Absolutely outstanding! Please follow me inside the monastery, and we shall discuss about your performance.\"\033[1;37;40m")
                    honor += 1
                else:
                    print ("\033[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\033[1;37;40m")
                    print ("\n \033[1;33;40m"+str(self.enemy.name)+ "\033[1;37;40m has been added to your discard pile.")
                input ("\n Press enter to continue.\n") 
                break
            else:
                if len(hand) == 0:
                    self.enemy.show()
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;32;40m YOUR HAND:\033[1;37;40m")
                    print(" You have no cards in your hand!")
                    print ("\033[1;37;40m=================================================")
                else:
                    self.enemy.show()
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;32;40m YOUR HAND:\033[1;37;40m")
                    for x in hand:
                        x.show()
                print ("\n Your current might is \033[1;31;40m"+str(dam)+"\033[1;37;40m/\033[1;31;40m"+str(self.enemy.val)+"\033[1;37;40m.")
                print (" Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
                pluralc = "s"
                plurald = "s"
                if len(pile) == 1:
                    pluralc = ""
                if len(discard) == 1:
                    plurald = ""
                print (" You currently have \033[1;33;40m" + str(len(pile))+" \033[1;37;40mcard"+pluralc+" remaining in your draw pile, and \033[1;33;40m"+ str(len(discard))+" \033[1;37;40mcard"+plurald+" remaining in your discard pile.")
                if insp > 0:
                    print (" You have \033[1;32;40m"+str(insp)+"\033[1;37;40m/\033[1;32;40m"+str(self.enemy.draw)+"\033[1;37;40m Inspiration remaining.")
                else:
                    print (" \033[1;31;40m⚠\033[1;37;40m You have spent all your Inspiration! You will lose \033[1;33;40m1\033[1;37;40m HP per additional card draw.")
            choice = input ("\n Please type what you wish to do next:\n")
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
                            print ("\033[1;37;40m=================================================")
                            print ("\033[1;34;40m My mind is pained with the struggle of creativity")
                            print (" I keep looking for something new to paint, but nothing comes to mind")
                            print (" Perhaps this dream was all for naught")
                            print (" Perhaps I was never meant to be an artist")
                            print (" It is now time to wake up")
                            print (" I open my eyes")
                            print (" And find myself sitting still")
                            print (" With an empty canvas standing before me")
                            print ("\033[1;37;40m=================================================")
                            input (" Game over. Press enter to terminate the program.\n")
                            exit()
                        continue
                else:
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;34;40m I have turned the final page of my sketchbook")
                    print (" Now is a good opportunity to add the new drawings I have learned")
                    print (" In the last few steps of my journey")
                    print (" But in the murky depths of my soul")
                    print (" Something which I have been struggling to conceal")
                    print (" Emerges from the darkness")
                    print (" And finds its way into my sketchbook")
                    print ("\033[1;37;40m=================================================")
                    pile += discard
                    discard.clear()
                    ohno = Flaw.pop(0)
                    pile.append(ohno)
                    random.shuffle(pile)
                    input ("\n Press enter to continue.\n")
                    if len(pile) > 0:        
                        draw = pile.pop()
                        hand.append(draw)
                        continue
                    elif len(pile) == 0:
                        print ("\033[1;37;40m=================================================")
                        print (" There are no cards left in your draw pile!")
                        print ("\033[1;37;40m=================================================")
                    if len(pile)+len(hand)+len(discard) == 0:
                        print ("\033[1;37;40m=================================================")
                        print (" \033[1;34;40mMy sketchbook is somehow empty")
                        print (" Returned to nothing")
                        print (" As consequence for my destructive whims")
                        print (" Nothing can be done now")
                        print (" I open my eyes")
                        print (" And find myself sitting still")
                        print (" With an empty canvas standing before me")
                        print ("\033[1;37;40m=================================================")
                        input (" Game over. Press enter to terminate the program.\n")
                        exit()
            elif choice == "forget" or choice == "f":
                HP -= (self.enemy.val-dam)
                self.enemy.show()
                print ("\033[1;37;40m=================================================")
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
                    print ("\n "+str(wolfremove.name)+" has been removed from your deck. (The Wolf)\n")
                if dusk in hand:
                    HP -= 1
                    random.shuffle(hand)
                    duskremove = hand.pop()
                    print ("\n "+str(duskremove.name)+" has been removed from your deck. (The Dusk)\n")
                ############################################################################################### EFFETS FORGET AVANT
                for x in hand:
                    x.show()
                    x.use = ""
                if HP <= 0:
                    print ("\033[1;37;40m=================================================")
                    print (" \033[1;34;40mThis creature is far too strong")
                    print (" My artistic prowess is incapable of impressing it")
                    print (" I feel like every single one of my thoughts")
                    print (" Is being absorbed into a bottomless void")
                    print (" I see it is time to wake up at last")
                    print (" I open my eyes")
                    print (" And find myself sitting still")
                    print (" With an empty canvas standing before me")
                    print ("\033[1;37;40m=================================================")
                    input (" Game over. Press enter to terminate the program.\n")
                    exit()
                print ("\033[1;34;40m\n Perhaps not all things are meant to be painted. Surely, some of my sketches must be flawed.\033[1;37;40m")
                if self.enemy.val-dam == 1:
                    print ("\n You have lost \033[1;33;40m"+str(self.enemy.val-dam)+ "\033[1;37;40m health point. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m.")
                else:
                    print ("\n You have lost \033[1;33;40m"+str(self.enemy.val-dam)+ "\033[1;37;40m health points. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m.")
                input ("\n Press enter to continue.\n")
                hand.sort(key=CardValueSort)
                forget = (self.enemy.val-dam)
                while forget > 0:
                    if choice == "The " or len(hand) == 0:
                        okay = False
                    print ("\033[1;34;40m\n Using my lost life essence, I shall burn away some of these worthless scribbles.\033[1;37;40m")
                    for x in hand:
                        x.show()
                    if forget == 1:
                        selectF = input ("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more card. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                    else:
                        selectF = input ("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more cards. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
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
                            print ("\033[1;37;40m=================================================")
                            print(" Error: You do not have enough cards left to forget to select a \033[1;31;40mFlaw\033[1;37;40m!")
                            print ("\033[1;37;40m=================================================")
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
                            print ("\033[1;37;40m=================================================")
                            print(" Error: Invalid card name selected. Please type the name of the card you wish to forget(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                            print ("\033[1;37;40m=================================================")
                        
                        continue
                ############################################################################################### EFFETS FORGET APRÈS
                if turtle in hand:
                    hand.remove(turtle)
                    pile.append(turtle)
                ############################################################################################### EFFETS FORGET APRÈS
                discard += hand
                hand.clear()
                if self.enemy == master1:
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;34;40m \"Hmm, this is concerning. Perhaps you just weren't warmed up yet.\"")
                    print ("\033[1;37;40m=================================================")
                elif self.enemy == master2:
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;34;40m \"What is this? Gather your equipment, and prove that you are worthy of my teachings!\"")
                    print ("\033[1;37;40m=================================================")
                elif self.enemy == master2:
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;34;40m \"This final trial was intended to be difficult. I am disappointed, but not surprised. Follow me inside the monastery, and we shall discuss of your performance.\"")
                    print ("\033[1;37;40m=================================================")
                else:
                    print ("\033[1;37;40m=================================================")
                    print ("\033[1;34;40m Now that my spirit feels lightened, I am ready to resume my journey.")
                    print ("\033[1;37;40m=================================================")
                input ("\n Press enter to continue.\n")
                
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
                            print ("\033[1;37;40m=================================================")
                            print (" This card's effect has already been used!")
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
                                print ("\033[1;37;40m=================================================")
                                for x in hand:
                                    x.show()
                                if forgetcount == 1:
                                    print ("\n You may forget \033[1;33;40m1\033[1;37;40m more card.\n")
                                else:
                                    print ("\n You may forget \033[1;33;40m"+str(forgetcount)+"\033[1;37;40m more cards.\n")
                                print ("\033[1;37;40m=================================================")
                                selectE = input (" Type the name of the card you wish to forget.\n")
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
                                    print ("\033[1;37;40m=================================================")
                                    print(" Error: Invalid card name selected. Please type the name of the card you wish to discard(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                            x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                        if "Discard" in eff:
                            discardcount = x.discard
                            while discardcount > 0:
                                if choice == "The " or len(hand) == 0:
                                    okay2 = False
                                print ("\033[1;37;40m=================================================")
                                for x in hand:
                                    x.show()
                                if discardcount == 1:
                                    print ("\n You may discard \033[1;33;40m1\033[1;37;40m more card.\n")
                                else:
                                    print ("\n You may discard \033[1;33;40m"+str(discardcount)+"\033[1;37;40m more cards.\n")
                                print ("\033[1;37;40m=================================================")
                                selectD = input (" Type the name of the card you wish to discard.\n")
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
                                    print ("\033[1;37;40m=================================================")
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
                                print ("\033[1;37;40m=================================================")
                                print ("\033[1;34;40m I have turned the final page of my sketchbook")
                                print (" Now is a good opportunity to add the new drawings I have learned")
                                print (" In the last few steps of my journey")
                                print (" But in the murky depths of my soul")
                                print (" Something which I have been struggling to conceal")
                                print (" Emerges from the darkness")
                                print (" And finds its way into my sketchbook")
                                print ("\033[1;37;40m=================================================")
                                pile += discard
                                discard.clear()
                                ohno = Flaw.pop(0)
                                pile.append(ohno)
                                random.shuffle(pile)
                                input ("\n Press enter to continue.\n")
                                if len(pile) >= x.draw:
                                    urdraw = "h" * x.draw
                                    for h in urdraw:
                                        draw = pile.pop()
                                        hand.append(draw)
                                    x.use = "- \033[1;31;40mUSED\033[1;37;40m"
                                    break
                                elif len(pile) == 0:
                                    print ("\033[1;37;40m=================================================")
                                    print (" There are no cards left in your draw pile!")
                                    print ("\033[1;37;40m=================================================")
                                if len(pile)+len(hand)+len(discard) == 0:
                                    print ("\033[1;37;40m=================================================")
                                    print (" \033[1;34;40mMy sketchbook is somehow empty")
                                    print (" Returned to nothing")
                                    print (" As consequence for my destructive whims")
                                    print (" Nothing can be done now")
                                    print (" I open my eyes")
                                    print (" And find myself sitting still")
                                    print (" With an empty canvas standing before me")
                                    print ("\033[1;37;40m=================================================")
                                    input (" Game over. Press enter to terminate the program.\n")
                                    exit()
                        else:
                            print ("\033[1;37;40m=================================================")
                            print (" This card does not have a usable active effect!")
                            break
                        
                    else:
                        good = False
                        continue
                if good == False:
                    print ("\033[1;37;40m=================================================")
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
        v = x.name
        w = y.name
        if len(pile) > 0:
            for o in pile:
                if "Flaw" in o.effect:
                    craneE.val +=1
        if len(discard) > 0:    
            for o in discard:
                if "Flaw" in o.effect:
                    craneE.val +=1
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m As my first steps scatter the red leaves across the soil")
        print (" I find myself inspired by the statues surrounding the trail")
        print (" Surely they would not mind appearing in a painting or two")
        print (" Who shall I paint first?\033[1;37;40m")
        print ("\033[1;37;40m=================================================")
        print ("\n Paintings remaining before next event: \033[1;33;40m5\033[1;37;40m\n")
        input (" Press enter to continue.\n")
        x.show()
        y.show()
        print ("\033[1;37;40m=================================================")
        print ("[1] "+ v)
        print ("[2] " + w)
        encount1 = input ("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            print ("\033[1;37;40m=================================================")
            print (" Error: Invalid option selected. Selecting random encounter...")
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
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m I continue my path towards the monastery")
        print (" Breathing calmly the fresh air of the forest")
        print (" Perhaps I should enjoy this moment of peace")
        print (" And paint a few more statues along the way.\033[1;37;40m")
        print ("\033[1;37;40m=================================================")
        print ("\n Paintings remaining before next event: \033[1;33;40m"+str(5-room)+"\033[1;37;40m\n")
        input (" Press enter to continue.\n")
        x.show()
        y.show()
        print ("\033[1;37;40m=================================================")
        print ("[1] "+ v)
        print ("[2] " + w)
        encount1 = input ("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            print ("\033[1;37;40m=================================================")
            print (" Error: Invalid option selected. Selecting random encounter...")
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
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m I have reached the middle of my journey in the Autumn Monastery")
        print (" I have encountered some of its denizens, and I shall surely see a few more before arriving at my destination")
        print (" My mind is flowing with ideas for new sketches")
        print (" But my body is feeling tired and exhausted")
        print (" Perhaps some rest is in order")
        print (" I notice two stone benches standing aside the path, make myself comfortable, and begin breathing calmly")
        print (" Crimson leaves fall all around me, and small rays of light piercing through the foliage illuminate the scenery")
        print (" A monk dressed in bright red garnments exits the monastery, and begins walking down the path towards me")
        print (" She sits on the second bench, closes her eyes, and speaks")
        print (" \"You have done well, Disciple of the Master\"")
        print (" \"You have seen five of our guardians, and learned that not all things are meant to be kept forever\"")
        print (" \"You seek inspiration at the very bottom of your dreams, correct?\"")
        print (" \"The dangers standing in your path are not trivial\"")
        print (" \"But you need not worry about that for now. Breathe, and rest.\"")
        print ("\033[1;37;40m=================================================")
        print (" Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
        print ("[1] \033[1;32;40mBreathe\033[1;37;40m (Heal 5 HP)")
        print ("[2] \033[1;31;40mDraw\033[1;37;40m (Challenge the Acolyte)")
        if len(pile) == 1:
            print ("[3] \033[1;36;40mReflect\033[1;37;40m (Shuffle your discard pile back into your draw pile without adding a \033[1;31;40mFlaw\033[1;37;40m, and forget up to 3 cards in your deck. You currently have \033[1;33;40m" + str(len(pile))+" \033[1;37;40mcard remaining in your draw pile.)")
        else:
            print ("[3] \033[1;36;40mReflect\033[1;37;40m (Shuffle your discard pile back into your draw pile without adding a \033[1;31;40mFlaw\033[1;37;40m, and forget up to 3 cards in your deck. You currently have \033[1;33;40m" + str(len(pile))+" \033[1;37;40mcards remaining in your draw pile.)")
        print ("\033[1;37;40m=================================================")
        eventchoice = input (" Please enter the number corresponding to your choice to proceed:\n")
        if eventchoice == "1":
            HP += 5
            print ("\033[1;37;40m=================================================")
            print ("\033[1;34;40m \"Excellent. Feel the air traverse your lungs. Be refreshed, Disciple.\"")
            print (" \"Alas, not all things are meant to last forever, as you have learned\"")
            print (" \"Our Master is eager to put you to the test\"")
            print (" \"May you remember all we have taught you as you journey onwards\"")
            print (" I turn to look at the monk and say goodbye, but she has already disappeared.")
            print ("\033[1;37;40m=================================================")
            print (" You have gained 5 health points. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
            room += 1
            input (" Press enter to continue.\n")
            EncounterM()
        elif eventchoice == "2": # Combattre le Acolyte
            fight = Encounter(acolyteE, "Monastery")
            fight.Fight()
        elif eventchoice == "3":
            pile += discard
            discard.clear()
            forget = 3
            while forget > 0:
                print ("\033[1;34;40m\n As I listen to the bright red leaves hitting the soil, I lose myself in my thoughts.\033[1;37;40m")
                for x in pile:
                    x.show()
                if forget == 1:
                    selectF = input ("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more card. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                else:
                    selectF = input ("\n Type the name of the card you wish to forget. You may forget \033[1;33;40m"+str(forget)+"\033[1;37;40m more cards. Forgetting a \033[1;31;40mFlaw\033[1;37;40m counts for 2 removed cards. Type \"exit\" to quit the forgetting phase.\n")
                selectF = selectF.title()
                if selectF == "C":
                    selectF = "The Canvas"
                if (not selectF.startswith("The")) and (("Yellow") not in selectF) and (("Blue") not in selectF) and (("Red") not in selectF):
                    selectF = "The " + selectF
                if selectF == "The Exit":
                    break
                
                for x in pile:
                    if "Flaw" in x.effect and forget <= 1 and selectF == x.name:
                        print ("\033[1;37;40m=================================================")
                        print(" Error: You do not have enough cards left to forget to select a \033[1;31;40mFlaw\033[1;37;40m!")
                        print ("\033[1;37;40m=================================================")
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
                        print ("\033[1;37;40m=================================================")
                        print(" Error: Invalid card name selected. Please type the name of the card you wish to forget(ex: \"The Canvas\" or \"canvas\"). The card must be in your current hand (shown below).")
                        print ("\033[1;37;40m=================================================")
                    
                    continue
            print ("\033[1;37;40m=================================================")
            print ("\033[1;34;40m \"Is simply resting so difficult for you?\"")
            print (" \"I see an Artist's mind never slumbers\"")
            print (" \"Very well then\"")
            print (" \"I am eager to see how this dedication will help you in the rest of your journey\"")
            print (" I turn to look at the monk and say goodbye, but she has already disappeared.")
            print ("\033[1;37;40m=================================================")
            room += 1
            input (" Press enter to continue.\n")
            EncounterM()
        else:
            print ("\033[1;37;40m=================================================")
            print ("\033[1;34;40m \"You don't know what to choose?\"")
            print ("\033[1;34;40m \"I understand. In such a foreign land, so far away from home...\"")
            print ("\033[1;34;40m \"Finding rest can be rather difficult\"")
            print ("\033[1;34;40m \"Here, compare your breathing with a flower\"")
            print ("\033[1;34;40m \"Opening and closing itself as the day and night chase each other\"")
            print ("\033[1;34;40m \"Excellent.\"")
            print (" After practicing the monk's exercise for a few minutes, I turn my head to thank her, but she has already disappeared.")
            print ("\033[1;37;40m=================================================")
            HP += 5
            print (" You have gained 5 health points. Your current health is \033[1;33;40m"+str(HP)+"\033[1;37;40m/\033[1;33;40m24\033[1;37;40m.")
            room += 1
            input (" Press enter to continue.\n")
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
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m After this rather enriching encounter with my first human being in this strange land")
        print (" I leave the stone bench behind, grateful for this opportunity to stop for a moment")
        print (" It is time to press on")
        print (" And paint a few more statues along the way.\033[1;37;40m")
        print ("\033[1;37;40m=================================================")
        print ("\n Paintings remaining before meeting the Master: \033[1;33;40m"+str(11-room)+"\033[1;37;40m\n")
        input (" Press enter to continue.\n")
        x.show()
        y.show()
        print ("\033[1;37;40m=================================================")
        print ("[1] "+ v)
        print ("[2] " + w)
        encount1 = input ("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            print ("\033[1;37;40m=================================================")
            print (" Error: Invalid option selected. Selecting random encounter...")
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
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m With every step I take, the monastery grows closer")
        print (" Soon, I shall meet the Master, and put all I have learned to the test")
        print (" If I succeed")
        print (" I am certain that great insight will be granted upon me")
        print (" For now, I cannot resist attempting to paint a few more of these beautiful statues.")
        print ("\033[1;37;40m=================================================")
        print ("\n Paintings remaining before meeting the Master: \033[1;33;40m"+str(11-room)+"\033[1;37;40m\n")
        input (" Press enter to continue.\n")
        x.show()
        y.show()
        print ("\033[1;37;40m=================================================")
        print ("[1] "+ v)
        print ("[2] " + w)
        encount1 = input ("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
        if encount1 == "1":
            fight1pool.append(y)
            fight = Encounter(x, "Monastery")
            fight.Fight()
        elif encount1 == "2":
            fight1pool.append(x)
            fight = Encounter(y, "Monastery")
            fight.Fight()
        else:
            print ("\033[1;37;40m=================================================")
            print (" Error: Invalid option selected. Selecting random encounter...")
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
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m At last")
        print (" I have travelled down the path of statues")
        print (" And I now find myself at the gates of the monastery")
        print (" But just as I prepare to open the doors and see what lies inside")
        print (" I feel a hand lay down on my right shoulder")
        print (" \"Not yet, Disciple. You have one more test to pass.\"")
        print ("\033[1;37;40m=================================================")
        input (" Press enter to continue.\n")
        print ("\033[1;37;40m=================================================")
        print (" \033[1;34;40mI turn around and see a man draped in bright red clothing, decorated with the images of a variety of animals")
        print (" I recognize every single one of them as one of the statues I have encountered in this eventful beginning of my journey")
        print (" In fact, all of them but one")
        print (" Before I can get a closer look at it, the Master bows and blocks my view of the unfamiliar figure")
        print (" \"You have stayed in our humble grove for so little time\"")
        print (" \"And yet you have learned so much\"")
        print (" \"It is now time to put all the knowledge you have acquired to the test\"")
        print (" \"Please save your questions for later\"")
        print (" \"And face me, the Master of the Autumn Monastery, Sculptor of Statues.\"")
        print ("\033[1;37;40m=================================================")
        input (" Press enter to open your sketchbook and FIGHT.\n")
        fight = Encounter(master1, "Monastery")
        fight.Fight()
    elif room == 12:
        fight = Encounter(master2, "Monastery")
        fight.Fight()
    elif room == 13:
        fight = Encounter(master3, "Monastery")
        fight.Fight()
    elif room == 14:
        boss = 0
        print ("\033[1;37;40m=================================================")
        print (" \033[1;34;40mThe Master turns the handle of his Monastery and invites me inside")
        print (" I take a moment to admire my surroundings, decorated by golden mosaics of the grove's inhabitants")
        print (" A small square red mat lies at the center of the room, surrounded by four bonsai trees")
        print (" I suddenly remind myself of the mysterious figure on the Master's robes")
        print (" But before I can get a closer look at it, the Master bows and blocks my view of the unfamiliar silhouette yet again")
        print (" \"Breathe deeply, for you are no longer my disciple.\"")
        print (" \"You are...\"")
        print ("\033[1;37;40m=================================================")
        input (" Press enter to receive the results of your evaluation.\n")
        if honor == 0:
            print ("\033[1;37;40m=================================================")
            print (" \033[1;34;40mThe Master pauses, then whispers, \"unworthy.\"")
            print (" \"Your skill is insufficient.\"")
            print (" \"It saddens me greatly to say it, but your journey ends here.\"")
            print (" \"Farewell, Artist. Perhaps your next attempt shall be more successful?")
            print (" Before I can express my disagreement, I feel the world around me fades into nothingness")
            print (" When my vision returns, I find myself sitting still")
            print (" With an empty canvas standing before me")
            print ("\033[1;37;40m=================================================")
            input (" Game over. Press enter to terminate the program.\n")
            exit()
        elif honor == 1:
            print ("\033[1;37;40m=================================================")
            print (" \033[1;34;40mThe Master pauses, then whispers, \"mediocre.\"")
            print (" \"As you have shown to be not completely talentless, I must allow you to pursue your travels.\"")
            print (" \"Know this: you must seek to improve your skills, for the creatures you will encounter beyond my domain are not as merciful as I am.\"")
            print (" \"For now, Artist, sit on the red mat, close your eyes, and dream vividly of your next destination.\"")
            print ("\033[1;37;40m=================================================")
            input (" Press enter to continue.\n")
        elif honor == 2:
            print ("\033[1;37;40m=================================================")
            print (" \033[1;34;40mThe Master pauses, then whispers, \"my acolyte.\"")
            print (" \"You have learned well, and your sketchbook is filled with skillful drawings.\"")
            print (" \"Look inside it; I have added one of mine as a way for you to remember my teachings.\"")
            print (" \"I regret to inform you that we must now part ways.\"")
            print (" \"I can gurarantee that all you have learned in my grove will be of great use to you.\"")
            print (" \"And now, Artist, sit on the red mat, close your eyes, and dream vividly of your next destination.\"")
            print ("\033[1;37;40m=================================================")
            input (" Press enter to continue.\n")
            discard.append(master)
        elif honor == 3:
            print ("\033[1;37;40m=================================================")
            print (" \033[1;34;40mThe Master pauses, then whispers, \"the new Master.\"")
            print (" \"You have outdone me in every way possible.\"")
            print (" \"I have added a creation of mine in your sketchbook, but I imagine it pales in comparison of what you have acquired so far.\"")
            print (" \"Listen. I must tell you something important.\"")
            print (" \"From all the statues you have seen in my grove, one is missing.\"")
            print (" \"That statue is the Lamb; a frail and weak creature, which felt completely out of place among the talented residents of my domain.\"")
            print (" \"I tried many times to make her better, but to no avail\"")
            print (" \"One morning, she left my grove, never to be seen again\"")
            print (" \"If you see her, wherever you will go...\"")
            print (" \"Tell her the Autumn Monastery is always ready to welcome her back\"")
            print (" \"And I could say the same thing for you, dear Master\"")
            print (" \"Now, I shall not retain you any longer. Please sit on the red mat, close your eyes, and dream vividly of your next destination.\"")
            print ("\033[1;37;40m=================================================")
            discard.append(master)
            input (" Press enter to continue.\n")
        print ("\033[1;37;40m=================================================")
        print ("\033[1;34;40m I close my eyes")
        print (" I find myself in the middle of a great staircase, floating in the void")
        print (" Hearing a faint buzzing sound from the summit, I turn my attention towards it")
        print (" A richly decorated gate coated in thick, sweet and golden honey urges me to approach it")
        print (" And perhaps taste some of its delightful nectar along the way")
        print (" A sudden orchestral crescendo coming from the bottom of the stairway snaps me out of my reverie")
        print (" An entrance made of soft purple cloth to what seems to be a circus invites me inside")
        print (" And shall perhaps allow me to take part in the show taking place behind it")
        print (" Where shall I pursue my travels?")
        print ("\033[1;37;40m=================================================")
        print ("[1] \033[1;33;40m The Golden Hive")
        print ("\033[1;37;40m[2] \033[1;35;40m The Theatre of Virtuosos")
        dest1 = input ("\033[1;37;40m Please enter the number corresponding to your choice to proceed:\n")
Start()
