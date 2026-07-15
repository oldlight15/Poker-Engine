import unittest

from card import Card
from game import Game
from player import Player


def cards(*values):
    """Create cards from compact strings such as AS, 10H, or 2D."""
    suits = {"S": "Spades", "H": "Hearts", "D": "Diamonds", "C": "Clubs"}
    ranks = {"A": 1, "J": 11, "Q": 12, "K": 13}
    result = set()
    for value in values:
        rank_text, suit_text = value[:-1], value[-1]
        rank = ranks.get(
            rank_text,
            int(rank_text) if rank_text.isdigit() else None,
        )
        result.add(Card(rank, suits[suit_text]))
    return result


class HandRankingTests(unittest.TestCase):
    def setUp(self):
        Game.players = []

    def game_with(self, board, *hands):
        players = [Player(f"P{index}", "player") for index in range(len(hands))]
        Game.players = players
        return Game(
            {player: cards(*hand) for player, hand in zip(players, hands)},
            board=cards(*board),
        ), players

    def test_pair_kicker_decides_winner(self):
        game, players = self.game_with(
            ("9S", "9H", "4D", "3C", "2S"),
            ("AS", "KH"),
            ("QS", "JH"),
        )
        self.assertEqual(game.determine_winner(), [players[0]])

    def test_board_can_create_true_tie(self):
        game, players = self.game_with(
            ("AS", "KH", "QD", "JC", "10S"),
            ("2S", "3H"),
            ("9S", "9H"),
        )
        self.assertEqual(game.determine_winner(), players)

    def test_two_pair_uses_kicker(self):
        game, players = self.game_with(
            ("KS", "KH", "4D", "4C", "2S"),
            ("AS", "3H"),
            ("QS", "JH"),
        )
        self.assertEqual(game.determine_winner(), [players[0]])

    def test_full_house_compares_trip_rank_first(self):
        game, players = self.game_with(
            ("KS", "KH", "2D", "2C", "3S"),
            ("KD", "AH"),
            ("2H", "QS"),
        )
        self.assertEqual(game.determine_winner(), [players[0]])

    def test_six_high_straight_beats_wheel(self):
        game, players = self.game_with(
            ("2S", "3H", "4D", "5C", "KS"),
            ("AS", "QH"),
            ("6S", "JH"),
        )
        self.assertEqual(game.determine_winner(), [players[1]])

    def test_flush_compares_all_kickers(self):
        higher_flush = cards("AS", "KS", "9S", "7S", "4S")
        lower_flush = cards("AS", "KS", "9S", "7S", "3S")
        self.assertGreater(
            Game._rank_five(higher_flush), Game._rank_five(lower_flush)
        )

    def test_straight_flush_outranks_four_of_a_kind(self):
        straight_flush = cards("9S", "10S", "JS", "QS", "KS")
        four_kind = cards("AH", "AS", "AD", "AC", "2D")
        self.assertGreater(
            Game._rank_five(straight_flush),
            Game._rank_five(four_kind),
        )

    def test_all_hand_categories_are_ordered_correctly(self):
        hands = [
            cards("AS", "KD", "9H", "6C", "3S"),
            cards("AS", "AD", "9H", "6C", "3S"),
            cards("AS", "AD", "9H", "9C", "3S"),
            cards("AS", "AD", "AH", "6C", "3S"),
            cards("5S", "6D", "7H", "8C", "9S"),
            cards("AS", "JS", "9S", "6S", "3S"),
            cards("AS", "AD", "AH", "6C", "6S"),
            cards("AS", "AD", "AH", "AC", "3S"),
            cards("9S", "10S", "JS", "QS", "KS"),
        ]

        ranks = [Game._rank_five(hand) for hand in hands]
        self.assertEqual(ranks, sorted(ranks))

    def test_four_of_a_kind_uses_kicker(self):
        aces_with_king = cards("AS", "AD", "AH", "AC", "KS")
        aces_with_queen = cards("AS", "AD", "AH", "AC", "QS")
        self.assertGreater(
            Game._rank_five(aces_with_king),
            Game._rank_five(aces_with_queen),
        )

    def test_one_pair_compares_each_kicker(self):
        king_kicker = cards("AS", "AD", "KH", "QC", "10S")
        jack_kicker = cards("AS", "AD", "KH", "QC", "JS")
        self.assertGreater(
            Game._rank_five(jack_kicker),
            Game._rank_five(king_kicker),
        )


if __name__ == "__main__":
    unittest.main()
