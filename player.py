# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:06:23 2026

@author: gavin
"""
import random

class Player:
    
    
    def __init__(self, name, bot, cash = 1000):
        
        self.in_play = True # Tracks if the players have folded and in the final round it will evaluate to false if the player has a losing hand
        self.name = name
        self.bot = bot
        self.bets = 0
        
        
        if cash > 0:
            self.cash = int(cash)
        else:
            self.cash = 1000
            
    def fold(self):
        self.in_play = False
        
    def bet(self, gamble):
        self.cash -= gamble 
        
    def highcard(self, game):
        return max(game.player_hands[self])
    
    def max_ev(self, montecarlo):
        ev = (montecarlo.p_hat_wins * self.bets) - ( 1 - (montecarlo.p_hat_wins + montecarlo.p_hat_ties) * self.bets)
        
    def base_ai(self, montecarlo, bet):

        factor = random.random()
        
        if  factor < .1:
            self.in_play = False
        else:
            return "call"
            
    def lag_ai(montecarlo): # Bot will tend to be more cautious and only bets with high equity
        factor = random.uniform(-0.1, 0.1)
        if montecarlo.p_hat_wins < .15 + factor:
            return "fold"
        if montecarlo.p_hat_wins < .35 + factor:
            return "call"
        if montecarlo.p_hat_wins < .5 + factor:
            return 0
    def tpa_ai(montecarlo): # Bot will tend to be more cautious and only bets with high equity
          factor = random.uniform(-0.1, 0.1)
          if montecarlo.p_hat_wins < .45 + factor:
              return "fold"
          elif montecarlo.p_hat_wins < .65 + factor:
              return "call"
          elif montecarlo.p_hat_wins < .75 + factor:
              return 0
    def lpa_ai(montecarlo): # Bot will tend to be more cautious and only bets with high equity
            factor = random.uniform(-0.1, 0.1)
            if montecarlo.p_hat_wins < .2 + factor:
                return "fold"
            elif montecarlo.p_hat_wins < .55 + factor:
                return "call"
            elif montecarlo.p_hat_wins < .8 + factor:
                return 0
    def tag_ai(montecarlo): # Bot will tend to be more cautious and only bets with high equity
            factor = random.uniform(-0.1, 0.1)
            if montecarlo.p_hat_wins < .4 + factor:
                return "fold"
            if montecarlo.p_hat_wins < .55 + factor:
                return "call"
            if montecarlo.p_hat_wins < .6 + factor:
                return 0
            
            
    def __str__(self):
        return self.name