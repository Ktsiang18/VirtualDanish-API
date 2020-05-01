#!/usr/bin/python
from models import Games, Users, Cards
from app import db
import random


class Card(object):
    """Cards designated by suit (S/H/C/D) and
     digit (1-13 with J/Q/K being 11/12/13)"""

    def __init__(self, suit, digit):
        self.suit = suit
        self.value = digit
        self.name = self.assignName(suit, digit)

    def assignName(self, suit, digit):
        royals = {
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
        }
        return suit + (royals[digit] if digit in royals else str(digit))

class Deck(object):
    def __init__(self):
        self.cards = self.fillDeck()
        self.size = len(self.cards)
        self.shuffle()

    def fillDeck(self):
        cards = []
        suits = ['S', 'H'] #'D', 'C']
        for s in suits:
            for d in range(2, 15):
                cards.append(Card(s, d))
        return cards

    def shuffle(self):
        for i in range(self.size):
            randInt = random.randint(0, self.size-1)
            self.cards[i], self.cards[randInt] = self.cards[randInt], self.cards[i]

    def dealCard(self):
        if self.size <= 0:
            raise Exception('Deck is Empty, cannot deal cards')
            return

        self.size -= 1
        return self.cards.pop()

class Pile(object):
    """Pile in center of board where cards are put down and picked up"""

    def __init__(self):
        self.pileCards = []

    def readTop(self):
        if self.pileCards:
            return self.pileCards[-1]

    def verifyCardsArePlayable(self, cards):
        values = set()

        for c in  cards:
            if not self.verifyCardIsPlayable(c):
                return False
            values.add(c.value)

        if len(values) > 1:
            print('Error: You may only play cards of the same value')
            return False

        return True

    def verifyCardIsPlayable(self, card):
        """Card is playable if
            the player has the card in their hand
            there is no top card
            it is a 10 or a 2
            it is <= than the top card annd top card is a 7
            it is >= the top card and the top card is not a 7
        """
        if not card:
            return False
        elif len(self.pileCards) == 0 or card.value in [2, 10]:
            return True
        elif self.readTop().value == 7 and card.value <= 7:
            return True
        elif self.readTop().value != 7 and card.value >= self.readTop().value:
            return True
        else:
            print('The card, ', card.name ,', is not playable.')
            return False
