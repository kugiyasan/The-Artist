# https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python/31281467

import sys
from contextlib import contextmanager
from io import StringIO
import unittest
from TheArtist import *

# * GUIDE TO MAKE A TEST CASE
# 1. Start by copying test_base(), rename it but the new name MUST starts with "test_"
# 2. Replace the enemy in Fight() to the desired one
# 3. Uncomment player.draw_pile for a custom draw_pile, and uncomment random.seed(69420) to predetermined every random move
# 4. Run the script, ensure that the behavior is as intended while playing and remember the input sequence and give it as an argument to captured_std()
# 5. Uncomment captured_std() and indent the line under it
# 6. Re-run the script, copy and paste the big string and assign it to expected
# 7. Remove the print(repr(output)) line, run the script and you should have a passing test!

# TODO tests
# ////Normal cards: beginning canvas red blue yellow dawn crow dragon frog leopard mantis rabbit wolf
# Cards with special effects, listed below:
#* crane
#* monkey
#* snake
#* spider
#* stag
#* swan
#* tiger
#* turtle

# Normal enemies: frogE rabbitE snakeE spiderE stagE swanE tigerE turtleE
# Enemies with special effects, listed below:
# * craneE
# * crowE
# * dragonE
# * leopardE
# * mantisE
# * monkeyE
#   wolfE

# EncounterAcolyte() + Enemy + Card
# Bossfight() + Enemy + Card

# Every kind of death
# death no HP
# death no HP by spider Card after match


@contextmanager
def captured_std(input_string=""):
    new_out, new_err, new_in = StringIO(), StringIO(), StringIO(input_string)
    old_out, old_err, old_in = sys.stdout, sys.stderr, sys.stdin
    try:
        sys.stdout, sys.stderr, sys.stdin = new_out, new_err, new_in
        yield sys.stdout
    finally:
        sys.stdout, sys.stderr, sys.stdin = old_out, old_err, old_in


class TestFightMechanics(unittest.TestCase):
    # def test_base(self):
    #     # random.seed(69420)
    #     player = Player()
    #     # player.draw_pile = [beginning] * 10
    #     fight = Fight(player, swanE)

    #     # with captured_std("") as out:
    #     fight.fight()

    #     output = out.getvalue().strip()
    #     expected = ""

    #     print(repr(output))
    #     self.assertEqual(output, expected)

    def test_normal_cards(self):
        player = Player()
        player.draw_pile = [beginning, canvas, red, blue, yellow, dawn, crow, dragon, frog, leopard, mantis, rabbit, wolf]
        fight = Fight(player, Enemy("Normie", 18, 13, "No effect.", canvas, short_name=""))

        with captured_std("d\n" * 15) as out:
            fight.fight()

        output = out.getvalue().strip()
        expected = '\x1b[1;37;40m=================================================\n\x1b[1;34;40mA wild Normie appeared!\n\x1b[1;37;40m=================================================\n Press enter to continue.\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n You have no cards in your hand!\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m0\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m13 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m13\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m3\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m12 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m12\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m3\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m11 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m11\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m5\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m10 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m10\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m6\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m9 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m9\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m6\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m8 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m8\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m10\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m7 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m7\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m12\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m6 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m6\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m14\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m5 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m5\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n Yellow (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m15\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m4 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m4\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n Yellow (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n Blue (\x1b[1;33;40m0\x1b[1;37;40m) - Heal 2 HP. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m15\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m3 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m3\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n Yellow (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n Blue (\x1b[1;33;40m0\x1b[1;37;40m) - Heal 2 HP. \x1b[1;32;40m*\x1b[1;37;40m\n Red (\x1b[1;32;40m2\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m17\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m2 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m2\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n Yellow (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n Blue (\x1b[1;33;40m0\x1b[1;37;40m) - Heal 2 HP. \x1b[1;32;40m*\x1b[1;37;40m\n Red (\x1b[1;32;40m2\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m17\x1b[1;37;40m/\x1b[1;31;40m18\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m1 \x1b[1;37;40mcard remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m1\x1b[1;37;40m/\x1b[1;32;40m13\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m Normie\x1b[1;37;40m\n Might: \x1b[1;31;40m18\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m13\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effect.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Rabbit (\x1b[1;33;40m0\x1b[1;37;40m) - Discard 2 cards. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n The Mantis (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 1 HP. \x1b[1;32;40m*\x1b[1;37;40m\n The Leopard (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Frog (\x1b[1;33;40m0\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dragon (\x1b[1;32;40m4\x1b[1;37;40m) - No effect. \n The Crow (\x1b[1;32;40m2\x1b[1;37;40m) - Discard 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n Yellow (\x1b[1;32;40m1\x1b[1;37;40m) - Draw 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n Blue (\x1b[1;33;40m0\x1b[1;37;40m) - Heal 2 HP. \x1b[1;32;40m*\x1b[1;37;40m\n Red (\x1b[1;32;40m2\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n\x1b[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\x1b[1;37;40m\n\n \x1b[1;33;40mNormie\x1b[1;37;40m has been added to your discard pile.\n\n Press enter to continue.\nThe Mantis is healing you\n\n\nThe Dawn is healing you\n\n\nBlue is healing you'

        self.assertEqual(output, expected)
        self.assertEqual(player.HP, player.maxHP)

    def test_stag_predetermined(self):
        random.seed(69420)
        player = Player()
        fight = Fight(player, stagE)

        with captured_std("d\n" * 7) as out:
            fight.fight()

        output = out.getvalue().strip()
        expected = '\x1b[1;37;40m=================================================\n\x1b[1;34;40m I stand before the statue of a noble, venerable stag\n Whose stature would no doubt be a great addition to my sketchbook\n I can hear its deep, respectful voice\n "Disciple of the Master, you walk among our garden"\n "Be respectful of all those who have come before you"\n "As each of your steps flatten the soil of our great Monastery."\n\x1b[1;37;40m=================================================\n Press enter to continue.\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n You have no cards in your hand!\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m0\x1b[1;37;40m/\x1b[1;31;40m2\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m13 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m3\x1b[1;37;40m/\x1b[1;32;40m3\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m0\x1b[1;37;40m/\x1b[1;31;40m2\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m12 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m2\x1b[1;37;40m/\x1b[1;32;40m3\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m0\x1b[1;37;40m/\x1b[1;31;40m2\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m11 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m1\x1b[1;37;40m/\x1b[1;32;40m3\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m1\x1b[1;37;40m/\x1b[1;31;40m2\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m10 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n \x1b[1;31;40m⚠\x1b[1;37;40m You have spent all your Inspiration! You will lose \x1b[1;33;40m1\x1b[1;37;40m HP per additional card draw.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m1\x1b[1;37;40m/\x1b[1;31;40m2\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m19\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m9 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n \x1b[1;31;40m⚠\x1b[1;37;40m You have spent all your Inspiration! You will lose \x1b[1;33;40m1\x1b[1;37;40m HP per additional card draw.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n The Canvas (\x1b[1;33;40m0\x1b[1;37;40m) - No effect. \n The Dawn (\x1b[1;32;40m2\x1b[1;37;40m) - Heal 2 HP. Draw 2 cards. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\x1b[1;37;40m\n\n \x1b[1;33;40mThe Stag\x1b[1;37;40m has been added to your discard pile.\n\n Press enter to continue.\nThe Dawn is healing you'

        self.assertEqual(output, expected)

    def test_swan(self):
        player = Player()
        fight = Fight(player, swanE)

        with captured_std("\n\n") as out:
            fight.fight()

        output = out.getvalue().strip()
        expected = '\x1b[1;37;40m=================================================\n\x1b[1;34;40m I stand before the statue of a magnificent white bird\n Whose silhouette would no doubt be a great addition to my sketchbook\n I can hear its beautiful signing voice\n "My power is unmatched and my beauty without equal"\n "You appear to be a rather talented Artist"\n "Therefore I shall allow you to paint my magnificence without hardships"\n "Hurry before I change my mind."\n\x1b[1;37;40m=================================================\n Press enter to continue.\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Swan\x1b[1;37;40m\n Might: \x1b[1;31;40m0\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m0\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Swan (\x1b[1;33;40m0\x1b[1;37;40m) - This card value\'s is 0. If this is the only card in your hand, the value of this card becomes 4. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n You have no cards in your hand!\n\x1b[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\x1b[1;37;40m\n\n \x1b[1;33;40mThe Swan\x1b[1;37;40m has been added to your discard pile.\n\n Press enter to continue.'
        self.assertEqual(output, expected)

    def test_wolf(self):
        player = Player()
        player.draw_pile = [beginning] * 3
        player.HP = 1
        fight = Fight(player, wolfE)

        # die using all his cards

        with captured_std("d\n" * 6) as out:
            with self.assertRaises(SystemExit):
                fight.fight()

        output = out.getvalue().strip()
        expected = '\x1b[1;37;40m=================================================\n\x1b[1;34;40m I stand before the fearsome statue of a gray wolf\n Whose frightening presence would no doubt be a great addition to my sketchbook\n I can hear its intimidating, growling voice\n "Artist, prepare for one of the greatest challenges of the beginning of your journey"\n "Prove your skill and might"\n "If you prevail, I will be glad to join your sketchbook"\n "And perhaps devour some of its inhabitants along the way."\n\x1b[1;37;40m=================================================\n Press enter to continue.\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Wolf\x1b[1;37;40m\n Might: \x1b[1;31;40m4\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m4\x1b[1;37;40m\n Effects: \x1b[1;33;40mIf you lose this combat, forget a random card in your hand.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n You have no cards in your hand!\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m0\x1b[1;37;40m/\x1b[1;31;40m4\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m1\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m3 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m4\x1b[1;37;40m/\x1b[1;32;40m4\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Wolf\x1b[1;37;40m\n Might: \x1b[1;31;40m4\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m4\x1b[1;37;40m\n Effects: \x1b[1;33;40mIf you lose this combat, forget a random card in your hand.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m1\x1b[1;37;40m/\x1b[1;31;40m4\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m1\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m2 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m3\x1b[1;37;40m/\x1b[1;32;40m4\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Wolf\x1b[1;37;40m\n Might: \x1b[1;31;40m4\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m4\x1b[1;37;40m\n Effects: \x1b[1;33;40mIf you lose this combat, forget a random card in your hand.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m2\x1b[1;37;40m/\x1b[1;31;40m4\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m1\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m1 \x1b[1;37;40mcard remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m2\x1b[1;37;40m/\x1b[1;32;40m4\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Wolf\x1b[1;37;40m\n Might: \x1b[1;31;40m4\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m4\x1b[1;37;40m\n Effects: \x1b[1;33;40mIf you lose this combat, forget a random card in your hand.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Wolf (\x1b[1;32;40m3\x1b[1;37;40m) - Forget 1 card. \x1b[1;32;40m*\x1b[1;37;40m\n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n The Beginning (\x1b[1;32;40m1\x1b[1;37;40m) - No effect. \n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m3\x1b[1;37;40m/\x1b[1;31;40m4\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m1\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m1\x1b[1;37;40m/\x1b[1;32;40m4\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n \x1b[1;34;40mMy sketchbook is somehow empty\n Returned to nothing\n As consequence for my destructive whims\n Nothing can be done now\n I open my eyes\n And find myself sitting still\n With an empty canvas standing before me\n\x1b[1;37;40m=================================================\n Game over. Press enter to terminate the program.'

        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
