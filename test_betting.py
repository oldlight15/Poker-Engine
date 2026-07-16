import unittest
from unittest.mock import patch

from player import Player
from runner import run_betting_round, run_betting_round_raises


class FakeGame:
    def __init__(self, players, pot=0):
        self.players = players
        self.pot = pot

    def starter(self):
        return 0

    def active_players(self):
        return [player_ for player_ in self.players if player_.in_play]

    def state_of_play(self):
        return len(self.active_players()) > 1

    def player_status(self, player_):
        pass


class BettingTests(unittest.TestCase):
    def test_last_player_does_not_take_an_action(self):
        winner = Player("Winner", "tag", 100)
        folded = Player("Folded", "tag", 100)
        folded.fold()
        winner.base_ai = lambda *_: self.fail("last player should not act")

        run_betting_round(FakeGame([winner, folded]))

        self.assertEqual(winner.cash, 100)
        self.assertTrue(winner.in_play)

    def test_human_raise_and_ai_call_update_cash_and_pot(self):
        human = Player("Human", "player", 100)
        bot = Player("Bot", "tag", 100)
        bot.base_ai = lambda *_: "call"
        game = FakeGame([human, bot], pot=10)

        with patch("builtins.input", side_effect=["raise", "20"]):
            run_betting_round(game)

        self.assertEqual(human.cash, 80)
        self.assertEqual(bot.cash, 80)
        self.assertEqual(game.pot, 50)

    def test_raise_responses_wrap_around_without_repeating_raiser(self):
        first = Player("First", "tag", 100)
        raiser = Player("Raiser", "tag", 100)
        last = Player("Last", "tag", 100)
        action_order = []

        first.base_ai = lambda *_: action_order.append("First") or "call"
        last.base_ai = lambda *_: action_order.append("Last") or "call"
        raiser.base_ai = lambda *_: self.fail("raiser should not respond")
        game = FakeGame([first, raiser, last])

        run_betting_round_raises(game, game.players, 1, 10)

        self.assertEqual(action_order, ["Last", "First"])
        self.assertEqual(first.cash, 90)
        self.assertEqual(raiser.cash, 100)
        self.assertEqual(last.cash, 90)


if __name__ == "__main__":
    unittest.main()
