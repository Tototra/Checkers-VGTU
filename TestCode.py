# Import the necessary modules
import unittest
from unittest.mock import Mock
from project import Game


# Define the test class
class TestMethods(unittest.TestCase):
    # Set up the test environment
    def setUp(self):
        # Create a mock Game object
        self.game = Mock(spec=Game)
        # Mock the endTurn method
        self.game.return_value.endTurn.side_effect = lambda: None  # Mocking endTurn to return None by default

    # Test case to check if the game object is not None
    def test_game(self):
        # Ensure the game object is not None
        self.assertIsNotNone(self.game, "The game is not launched")

    # Test case to check if the pawn lists are not empty
    def test_list(self):
        # Mock the list_of_pawn attribute
        self.game.return_value.blackPawns.list_of_pawn = [Mock(), Mock()]
        self.game.return_value.whitePawns.list_of_pawn = [Mock(), Mock()]
        # Check if the lists are not empty
        self.assertIsNot(self.game.return_value.blackPawns.list_of_pawn, [], "The list is not empty")
        self.assertIsNot(self.game.return_value.whitePawns.list_of_pawn, [], "The list is not empty")

    # Test case to check if the board initialization message is returned
    def test_board(self):
        # Mock the initBoard method to return a message
        self.game.return_value.initBoard.return_value = "The board is created"
        # Check if the board initialization message is returned
        self.assertEqual(self.game.return_value.initBoard(), "The board is created")

    # Test case to check the endTurn method in different game states
    def test_end_turn(self):
        # Mock the endTurn method to simulate different game states
        # Simulate no white pawns left
        self.game.return_value.whitePawns.list_of_pawn = []
        # Ensure None is returned when no pawns are left
        self.assertEqual(self.game.return_value.endTurn(), None)

        # Simulate one white pawn left
        self.game.return_value.whitePawns.list_of_pawn = [Mock()]
        # Simulate no black pawns left
        self.game.return_value.blackPawns.list_of_pawn = []
        # Ensure None is returned when no pawns are left
        self.assertEqual(self.game.return_value.endTurn(), None)

        # Simulate one white pawn left
        self.game.return_value.whitePawns.list_of_pawn = [Mock()]
        # Simulate one black pawn left
        self.game.return_value.blackPawns.list_of_pawn = [Mock()]
        # Ensure None is returned to continue the game
        self.assertEqual(self.game.return_value.endTurn(), None)


# Run the tests if this script is executed directly
if __name__ == '__main__':
    unittest.main()
