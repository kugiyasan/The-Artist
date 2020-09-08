# https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python/31281467

import sys
from contextlib import contextmanager
from io import StringIO
import unittest
from TheArtist import *

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestFightMechanics(unittest.TestCase):
    def test_swan(self):
        player = Player()
        fight = Fight(player, swanE)
        sys.stdin = StringIO("\n\n")

        with captured_output() as (out, err):
            fight.fight()
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()
        text = '\x1b[1;37;40m=================================================\n\x1b[1;34;40m I stand before the statue of a magnificent white bird\n Whose silhouette would no doubt be a great addition to my sketchbook\n I can hear its beautiful signing voice\n "My power is unmatched and my beauty without equal"\n "You appear to be a rather talented Artist"\n "Therefore I shall allow you to paint my magnificence without hardships"\n "Hurry before I change my mind."\n\x1b[1;37;40m=================================================\n Press enter to continue.\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Swan\x1b[1;37;40m\n Might: \x1b[1;31;40m0\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m0\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Swan (\x1b[1;33;40m0\x1b[1;37;40m) - This card value\'s is 0. If this is the only card in your hand, the value of this card becomes 4. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n You have no cards in your hand!\n\x1b[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\x1b[1;37;40m\n\n \x1b[1;33;40mThe Swan\x1b[1;37;40m has been added to your discard pile.\n\n Press enter to continue.'
        self.assertEqual(output, text)

    def test_stag(self):
        player = Player()
        fight = Fight(player, stagE)
        sys.stdin = StringIO("d\n" * 15)

        with captured_output() as (out, err):
            fight.fight()
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()
        start = '\x1b[1;37;40m=================================================\n\x1b[1;34;40m I stand before the statue of a noble, venerable stag\n Whose stature would no doubt be a great addition to my sketchbook\n I can hear its deep, respectful voice\n "Disciple of the Master, you walk among our garden"\n "Be respectful of all those who have come before you"\n "As each of your steps flatten the soil of our great Monastery."\n\x1b[1;37;40m=================================================\n Press enter to continue.\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n You have no cards in your hand!\n\x1b[1;37;40m=================================================\n\n Your current might is \x1b[1;31;40m0\x1b[1;37;40m/\x1b[1;31;40m2\x1b[1;37;40m.\n Your current health is \x1b[1;33;40m20\x1b[1;37;40m/\x1b[1;33;40m24\x1b[1;37;40m.\n You currently have \x1b[1;33;40m13 \x1b[1;37;40mcards remaining in your draw pile, and \x1b[1;33;40m0 \x1b[1;37;40mcard remaining in your discard pile.\n You have \x1b[1;32;40m3\x1b[1;37;40m/\x1b[1;32;40m3\x1b[1;37;40m Inspiration remaining.\n\n Please type what you wish to do next:\n\x1b[1;37;40m=================================================\n\x1b[1;36;40m The Stag\x1b[1;37;40m\n Might: \x1b[1;31;40m2\x1b[1;37;40m\n Inspiration: \x1b[1;32;40m3\x1b[1;37;40m\n Effects: \x1b[1;33;40mNo effects.\x1b[1;37;40m\n \n \x1b[1;34;40mREWARD:\x1b[1;37;40m\n The Stag (\x1b[1;31;40m-5\x1b[1;37;40m) - This card\'s value increases by 1 for every card in your hand. \n\x1b[1;37;40m=================================================\n\x1b[1;32;40m YOUR HAND:\x1b[1;37;40m\n '
        end = "\n\x1b[1;34;40m\n I have proven myself worthy, and may now add a sketch of this creature to my collection.\x1b[1;37;40m\n\n \x1b[1;33;40mThe Stag\x1b[1;37;40m has been added to your discard pile.\n\n Press enter to continue."
        
        # can't assert the middle, because it's randomly generated
        self.assertTrue(output.startswith(start))
        self.assertTrue(output.endswith(end))


if __name__ == '__main__':
    unittest.main()