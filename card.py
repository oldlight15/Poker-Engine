# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:49:48 2026

@author: gavin
"""

class Card:
# Cosntructs a card and contains a comparison operator for rank.
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
        
    def __str__(self):
        if self.rank == 1: 
            return f"Ace of {self.suit}" 
        elif self.rank == 11: 
            return f"Jack of {self.suit}" 
        elif self.rank == 12: 
            return f"Queen of {self.suit}" 
        elif self.rank == 13: 
            return f"King of {self.suit}" 
        else:
            return f"{self.rank} of {self.suit}"
        
        
    def __lt__(self, obj):
        if self.rank < obj.rank:
            return True
        return False