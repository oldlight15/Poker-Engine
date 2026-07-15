# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:55:57 2026

@author: gavin
"""
import random
import card as c
from collections import Counter
from itertools import combinations
import montecarlo
import player

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
        """Return a fully comparable rank for a player's best five-card hand.

        The first value identifies the hand category (8 is a straight flush and
        0 is a high-card hand).  The remaining values are category-specific
        tie breakers in descending importance.  Python compares tuples
        lexicographically, which gives us correct poker tie breaking.
        """
        cards = self.player_hands[player] | self.board
        if len(cards) < 5:
            raise ValueError("At least five cards are required to rank a hand")
        return max(self._rank_five(combo) for combo in combinations(cards, 5))

    @staticmethod
    def _rank_five(cards):
        """Rank exactly five cards as (category, tie_breaker, ...)."""
        ranks = [14 if card_.rank == 1 else card_.rank for card_ in cards]
        counts = Counter(ranks)
        groups = sorted(
            ((count, rank) for rank, count in counts.items()), reverse=True
        )
        is_flush = len({card_.suit for card_ in cards}) == 1

        unique_ranks = set(ranks)
        if 14 in unique_ranks:
            unique_ranks.add(1)  # An ace may be low in A-2-3-4-5.
        straight_high = 0
        ordered = sorted(unique_ranks)
        for index in range(len(ordered) - 4):
            window = ordered[index:index + 5]
            if window[-1] - window[0] == 4:
                straight_high = window[-1]

        if is_flush and straight_high:
            return (8, straight_high)
        if groups[0][0] == 4:
            four_rank = groups[0][1]
            kicker = max(rank for rank in ranks if rank != four_rank)
            return (7, four_rank, kicker)
        if groups[0][0] == 3 and groups[1][0] == 2:
            return (6, groups[0][1], groups[1][1])
        if is_flush:
            return (5, *sorted(ranks, reverse=True))
        if straight_high:
            return (4, straight_high)
        if groups[0][0] == 3:
            trip_rank = groups[0][1]
            kickers = sorted(
                (rank for rank in ranks if rank != trip_rank), reverse=True
            )
            return (3, trip_rank, *kickers)
        pair_ranks = sorted(
            (rank for rank, count in counts.items() if count == 2), reverse=True
        )
        if len(pair_ranks) == 2:
            kicker = max(rank for rank in ranks if rank not in pair_ranks)
            return (2, pair_ranks[0], pair_ranks[1], kicker)
        if len(pair_ranks) == 1:
            pair_rank = pair_ranks[0]
            kickers = sorted(
                (rank for rank in ranks if rank != pair_rank), reverse=True
            )
            return (1, pair_rank, *kickers)
        return (0, *sorted(ranks, reverse=True))
        
    def tie_break(self, players, board):
        """Return complete hand ranks for compatibility with older callers."""
        return [self.handvalue(player_) for player_ in players]
    
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
                player_value = hand_values[game.players.index(player)]
                best_value = max(hand_values)
                if player_value == best_value:
                    if hand_values.count(best_value) == 1:
                        wins.append(1)
                    else:
                        ties.append(1)
                            
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

        return finalists

         
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
