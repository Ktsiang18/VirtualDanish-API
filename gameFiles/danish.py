#!/usr/bin/python
from playersAndBoard import *
import time

print('Welcome to Danish!')
time.sleep(.5)
print('Dealing cards...\n')
time.sleep(.5)

#initialize objects

Game = Board(2)

# let players swap cards
for player in Game.players:
    player.swapCards()

print('Starting Game... \n')
time.sleep(1)
# Swap player turns
while True:
    gameWon = Game.handleCurrentPlayersTurn()
    if gameWon:
        break
    Game.changePlayer()

Game.handleGameWon()

#fix:  down cards - need to keep down  hand and  hand separate.
