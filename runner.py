"""
Created on Mon Jun 15 14:49:48 2026

@author: gavin
"""

import game
import montecarlo
import player


    
def get_raise_amount(player_):
    """Prompt until the player enters a legal raise amount."""
    while True:
        try:
            amount = int(input())
        except ValueError:
            print("Please enter a whole number")
            continue

        if amount <= 0:
            print("Raise amount must be greater than zero")
        elif amount > player_.cash:
            print(f"You only have {player_.cash} remaining")
        else:
            return amount


def run_betting_round(game):
    # Fixes needed:
    # If player folds remove from active list
    # Fix over betting
    
    action_order = (
        game.players[game.starter():]
        + game.players[:game.starter()]
    )
    active_players = [
        player_ for player_ in action_order if player_.in_play
    ]

    for player_ in active_players:
        if not game.state_of_play():
            return
        if not player_.in_play:
            continue

        if player_.bot == "player":
            game.player_status(player_)
            print("Raise or Call?")
            player_choice = input().strip().upper()

            if player_choice == "RAISE":
                print("By how much?")
                raise_amount = get_raise_amount(player_)
                player_.bet(raise_amount)
                game.pot += raise_amount
                run_betting_round_raises(
                    game,
                    game.active_players(),
                    game.active_players().index(player_),
                    raise_amount,
                )
                return
              
        #It might be helpful to add in an error/go back line here to accomadate a mistype
       
        else:
            ai_choice = player_.base_ai(None, 0)
            
            if ai_choice == "call":
                print(f"{player_.name} calls")
            elif not player_.in_play:
                print(f"{player_.name} folds")
         
                    
def run_betting_round_raises(game, active_players, index, bet):
    """Give every other active player a chance to respond to a raise."""
    action_order = active_players[index + 1:] + active_players[:index]

    for player_ in action_order:
        if not game.state_of_play():
            return
        if not player_.in_play:
            continue

        if player_.bot == "player":
            print("Call or Fold?")
            player_choice = input().strip().upper()
            if player_choice == "CALL":
                if bet > player_.cash:
                    print("Not enough cash to call; you fold")
                    player_.fold()
                else:
                    player_.bet(bet)
                    game.pot += bet
            else:
                player_.fold()
        else:
            # AI raise logic is intentionally deferred. For now, bots only
            # call or fold when facing a raise.
            ai_choice = player_.base_ai(None, bet)
            if ai_choice == "call":
                if bet > player_.cash:
                    player_.fold()
                    print(f"{player_.name} folds")
                else:
                    player_.bet(bet)
                    game.pot += bet
                    print(f"{player_.name} calls")
            else:
                player_.fold()
                print(f"{player_.name} folds")



    
def main():
    playercount = 0
    while playercount == 0:
        print("How many players (Max: 10)")
        try:
            playercount = int(input())
            if playercount < 4 or playercount > 10:
                print("Please enter a number between 4 and 10")
                playercount = 0
        except ValueError:
            print("Please enter a number")

    game.Game.add_players(playercount, pot=1000)
    poker_game = game.Game({})
    game_running = True

    while game_running:
        poker_game.dealhands()
        run_betting_round(poker_game)

        if poker_game.state_of_play():
            poker_game.flop()
            run_betting_round(poker_game)

        if poker_game.state_of_play():
            poker_game.board.add(poker_game.deal())
            run_betting_round(poker_game)

        if poker_game.state_of_play():
            poker_game.board.add(poker_game.deal())
            run_betting_round(poker_game)

        poker_game.end_of_round()

        print("Continue(Y/N): ")
        choice = input().strip().upper()
        if choice == "N":
            game_running = False
        elif choice != "Y":
            print("Please enter 'Y' or 'N'")


if __name__ == "__main__":
    main()
