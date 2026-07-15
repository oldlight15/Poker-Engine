# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:27:08 2026

@author: gavin
"""
import card
import random

# Builds standard deck of 52 careds
class Deck :
    def __init__(self):
        self.order = []         # List that contains the cards
        self.position = 0       # Tracks the top card of the deck
        for x in range(12):
            self.order.append(card(x + 1, "Diamonds"))    
        for x in range(12):
            self.order.append(card(x + 1, "Hearts"))    
        for x in range(12):
            self.order.append(card(x + 1, "Spades"))    
        for x in range(12):
            self.order.append(card(x + 1, "Clubs")) 
    def deal(self):
        self.position += 1
        return self.order[self.position - 1]
    def shuffle(self):
        self.position = 0
        self.order.random.shuffle()
