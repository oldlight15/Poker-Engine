"""
Created on Mon Jun 15 14:49:48 2026

@author: gavin
"""

import game
import montecarlo
import player


    
def run_betting_round (game):
    # Fixes needed:
    # If player folds remove from active list
    
    active_players = []
    for x in game.players[game.starter():] + game.players[:game.starter()]:
        if x.in_play == True:
            active_players.append(x)
    for x in active_players:
          if game.players.index(x) == 0:
              game.player_status(x)
              print("Raise or Call?")
              player_choice = input()
              if player_choice.upper() == "RAISE":
                  print("By how much?")
                  player_choice = input()
                  run_betting_round_rasies (game, active_players, active_players.index(x))
                  break
        #It might be helpful to add in an error/go back line here to accomadate a mistype
          elif x.base_ai(x, 0) == "call":
              print(f"{x.name} calls")
          elif x.base_ai(game.monte(x), 0) == "bet":
             run_betting_round_rasies (game, active_players, active_players.index(x))
             break
         
                    
def run_betting_round_rasies (game, active_players, index): # Triggers if any player raises
    montecarlos = {}
    return
    
playercount = 0
while playercount == 0:
    print("How many players (Max: 10)")
    try:
        playercount = int(input())
        if playercount < 4 or playercount > 10:
            print("Please enter a number between 4 and 10")
            playercount = 0  # reset so the loop continues
    except ValueError:
        print("Please enter a number")   
        

game.Game.add_players(playercount, pot = 1000)

game = game.Game({})
gstate = True # Tracks whether or not the player wishes to continue playing the game

while gstate:  
    
    
    game.dealhands()
    run_betting_round (game)    
    game.flop()
    run_betting_round (game)
    game.board.add(game.deal())
    run_betting_round (game)
    game.board.add(game.deal())  
    run_betting_round (game)   
    
    game.end_of_round()
         
    print("Continue(Y/N): ") # Plays another round 
    x = input().upper()
    if x == "Y":
       pass
    elif x == "N":
       gstate = False     
    else:
        print("Please enter 'Y' or 'N'")
