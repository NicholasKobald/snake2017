import sys

sys.path.extend(['.', '..'])

import main
import objects
import tests.fixtures as fixtures
import unittest

from food_fetcher import find_snakes_that_just_ate
from shared import create_snake_dict

class TestBasicSafety(unittest.TestCase):
    def test_prefer_head_collision_over_wall(self):
        game_data, only_valid_move = fixtures.get_data_with_one_valid_move()
        board_data = game_data['board']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = objects.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            game_data['you']['id'],
        )

        # assume that the one other snake ate
        game_data['ate_last_turn'] = [
            snake_id for snake_id in board_data['snakes'] if snake_id != game_data['you']['id']
        ]

        move = main.pick_move(game_data, board, snake_dict)
        self.assertEqual(move, only_valid_move, "Failed to choose only valid move.")


    def test_avoids_dead_end(self):
        game_data, _, _, best_move = fixtures.get_data_with_one_way_out()
        board_data = game_data['board']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = objects.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            game_data['you']['id'],
        )

        # should result in an empty list
        game_data['ate_last_turn'] = find_snakes_that_just_ate(board_data, [], board)

        move = main.pick_move(game_data, board, snake_dict)
        self.assertEqual(move, best_move, "Failed to choose best move.")

    def test_prefers_move_away_from_snake(self):
        game_data, _, _, best_move = fixtures.get_data_with_two_ways_out()
        board_data = game_data['board']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = objects.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            game_data['you']['id'],
        )

        # should result in an empty list
        game_data['ate_last_turn'] = find_snakes_that_just_ate(board_data, [], board)

        move = main.pick_move(game_data, board, snake_dict)
        self.assertEqual(move, best_move, "Failed to choose best move.")

class TestAdvancedSafety(unittest.TestCase):
    def test_prefer_larger_component(self):
        game_data, best_move = fixtures.get_data_with_one_big_component()
        board_data = game_data['board']

        snake_dict = create_snake_dict(board_data['snakes'])
        board = objects.Board(
            board_data['height'],
            board_data['width'],
            snake_dict,
            board_data['food'],
            game_data['you']['id'],
        )

        # should result in an empty list
        game_data['ate_last_turn'] = find_snakes_that_just_ate(board_data, [], board)

        move = main.pick_move(game_data, board, snake_dict)
        self.assertEqual(move, best_move, "Failed to choose move towards big component.")
