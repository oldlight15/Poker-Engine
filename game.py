# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:55:57 2026

@author: gavin
"""
import player 
import card
import random
import card as c
from collections import Counter     
import math as m
import numpy as np
import statistics
import montecarlo

class Game:
    
    
    playercount = 0
    is_betting = False
    players = []
    
    bblind = 2
    dealer = 0
    sblind = 1
    
    def __init__(self, player_hands, pot = 1000, board = None, deck = None):
        
        
        # Fix based on new public variable
        self.deck = deck         # List that contains the cards
        self.position = 0       # Tracks the top card of the deck
        #self.pot = pot Fix to split pot among players
        self.board = set() if board is None else set(board)
            
            
        if deck == None:
            self.deck = []
            for x in range(13):
                self.deck.append(c.Card(x + 1, "Diamonds"))    
                self.deck.append(c.Card(x + 1, "Hearts"))    
                self.deck.append(c.Card(x + 1, "Spades"))    
                self.deck.append(c.Card(x + 1, "Clubs"))   
            random.shuffle(self.deck)
            
        cards_in_play = set()
        if board is not None:
            cards_in_play = cards_in_play.union(board)
        if player_hands is not {}:
            for hand in player_hands.values():
                cards_in_play = cards_in_play.union(hand)
        if cards_in_play is not None:
            for x in self.deck:
                if x in cards_in_play:
                    self.deck.remove(x)
        self.player_hands = player_hands
                
                
    def reset_hands(self, p): # Resets all hands except p
        for x in Game.players:
            pass
        
    def show_hands(self):
        print("Board:")
        print(self.board)
        for x in self.player_hands:
            if x.in_play:
                for y in self.player_hands[x]:
                    print(y)
    
    def flop(self):
        for x in range(3):
            self.board.add(self.deal())
        for x in self.board:
            print(x)
            
            
            
    @classmethod        
    def set_playercount(cls, playercount):
        cls.playercount = playercount      
        
        
    def starter(self):
        if self.board is None:
            if self.bblind == Game.playercount - 1:
                return 0
            else:
                return self.bblind
        else:
            if self.sblind == Game.playercount - 1:
                return 0
            else:
                return self.bblind
            
    @classmethod        
    def add_players(cls, playercount, pot = 1000):
        
        for x in range(playercount):
            if x == 1:
                cls.players.append(player.Player(f"P{x}", "player", pot))
            else:
                cls.players.append(player.Player(f"P{x}", "lag", pot))
  
           # This method needs to fixed to accomodate random AIs 
            
            
    @classmethod       
    def shiftblinds(cls): # moves blinds and dealer position at end of each game
       if cls.dealer == cls.playercount:
           cls.dealer = 0
           cls.sblind += 1
           cls.bblind += 1
       elif cls.sblind == cls.playercount:
          cls.dealer += 1
          cls.sblind = 0
          cls.bblind += 1
       elif cls.bblind == cls.playercount:
           cls.dealer += 1
           cls.sblind += 1
           cls.bblind = 0
       else:
           cls.dealer += 1
           cls.sblind += 1
           cls.bblind += 1
           
    def deal(self):
          self.position += 1
          return self.deck[self.position - 1]
      
    def shuffle(self):
          random.shuffle(self.deck)
          self.dealer = 0
          self.sblind = 1
          self.bblind = 2
          
          
          
    def dealhands(self, player_hands = {}): # Deals two cards to each player
         for player_ in self.players:
             if player_ not in self.player_hands:
                 self.player_hands[player_] = {
                self.deal(),
                self.deal()
            }

                 
                 
    def handvalue(self, player):
        
        
        hand = self.player_hands[player] | self.board
        points = 0
        
        
        
        if self.check_royalflush(hand):
                return 35
        if self.check_straight(hand):
            points += 12 
        if self.check_flush(hand):
            points += 13
        if self.check_four_of_kind(hand):
            points += 20
        points +=  4 * self.check_pair(hand)
        points +=  4 * self.check_three_of_kind(hand)
        return points
        
    def tie_break(self, players, board): # Retunrs the highest rank in play for each player
        
        return [
        max(
            14 if card_.rank == 1 else card_.rank
            for card_ in (self.player_hands[player_] | board)
        )
        for player_ in players
    ]
    
    def check_royalflush(self, hand): # Checks for royal flush
        royal_ranks = {1, 10, 11, 12, 13}

        for suit in ("Diamonds", "Clubs", "Hearts", "Spades"):
            suited_ranks = {
            card_.rank
            for card_ in hand
            if card_.suit == suit
        }

        if royal_ranks.issubset(suited_ranks):
            return True

        return False

    def check_straight(self, hand):
        ranks = []

        for x in hand:
            ranks.append(x.rank)

        ranks = sorted(set(ranks))  # remove duplicates + sort

        if len(ranks) < 5:
            return False
        if 1 in ranks:
            ranks.append(14)
        for i in range(len(ranks) - 4):
            if (
            ranks[i] + 1 == ranks[i + 1] and
            ranks[i] + 2 == ranks[i + 2] and
            ranks[i] + 3 == ranks[i + 3] and
            ranks[i] + 4 == ranks[i + 4]
            ):
                return True

        return False
    
    
    def monte(self, player): # Runs a monte carlo simulation to determine probability to +-.01 with a confidence of 99.99%
    #switch from game to self
        wins = []
        ties = []
        
        for x in range(40000):
                game = Game(player_hands = {player : self.player_hands[player]},  board = self.board)             
                game.dealhands()
                for cards in range(5 - len(game.board)):
                    game.board.add(game.deal())
                hand_values = []
                for x in game.players:
                    hand_values.append(game.handvalue(x))
                if hand_values[game.players.index(player)] == max(hand_values):
                    if hand_values.count(max(hand_values)) == 1:
                        wins.append(1)
                    else:
                        high_values = game.tie_break(game.players, game.board)

                        player_index = game.players.index(player)
                        player_high = high_values[player_index]
                        best_high = max(high_values)

                        if player_high == best_high:
                                if high_values.count(best_high) > 1:
                                        ties.append(1)
                        else:
                            wins.append(1)
                            
        p_hat_wins = sum(wins) / 40000
        p_hat_ties = sum(ties) / 40000
        return montecarlo.Montecarlo(p_hat_wins, p_hat_ties)
    
    
    def player_status(self, player):
        
        if Game.players.index(player) == Game.sblind:
            print("You are the small blind.")
        elif Game.players.index(player) == Game.bblind:
            print("You are the big blind.")
        elif Game.players.index(player) == Game.dealer:
            print("You are the dealer.")
            
        self.hand_and_board(player)

    def hand_and_board(self, player):
        print("Hand:")
        for x in self.player_hands[self.players[0]]:
            print(x)
        if self.board is not None:
            print("Board:")
            for x  in self.board:
                print(x)

    def determine_winner(self):
        active_players = [
        player_
        for player_ in self.players
        if player_.in_play
    ]

        if not active_players:
            return []

        hand_values = {
        player_: self.handvalue(player_)
        for player_ in active_players
    }

        best_value = max(hand_values.values())

        finalists = [
        player_
        for player_, value in hand_values.items()
        if value == best_value
    ]

    # One player has the best hand value.
        if len(finalists) == 1:
            return finalists

    # Break equal hand values using the updated high-card logic.
        high_values = self.tie_break(finalists, self.board)
        best_high = max(high_values)

        winners = [
        player_
        for player_, high_value in zip(finalists, high_values)
        if high_value == best_high
    ]

        return winners           

         
    def end_of_round(self): # Runs at the end of play or when only one player is left
    
        winners = self.determine_winner()
        if len(winners)  == 1:
            print(f"{winners[0].name} wins")
        else:
            print("Tie between:", ", ".join(player.name for player in winners))                
                    
    def check_flush(self, hand):
   # Return True when at least five cards share the same suit. 
     suit_counts = Counter(card.suit for card in hand)
     return any(count >= 5 for count in suit_counts.values())


    def check_three_of_kind(self, hand):
     # Return the number of ranks containing exactly three cards. 
        rank_counts = Counter(card.rank for card in hand)
        return sum(count == 3 for count in rank_counts.values())


    def check_four_of_kind(self, hand):
   # Return True when four cards have the same rank.
        rank_counts = Counter(card.rank for card in hand)
        return any(count == 4 for count in rank_counts.values())


    def check_pair(self, hand):
        # Return the number of ranks containing exactly two cards. 
        rank_counts = Counter(card.rank for card in hand)
        return sum(count == 2 for count in rank_counts.values())