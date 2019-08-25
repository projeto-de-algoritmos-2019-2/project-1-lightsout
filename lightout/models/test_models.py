import unittest

class TestCell(unittest.TestCase):

    def test_cell_neighbors_is_empty_on_creation(self):
        from models import Cell
        cells = Cell()

        self.assertListEqual(cells.neighbors, [])
    
class TestGame(unittest.TestCase):

    def tests_if_the_game_builder_returns_all_cells_off(self):
        from models import Game
        game = Game(size=3, cells_on=False)

        for cell in game.cells:
            self.assertFalse(cell.is_on)
    
    def tests_if_the_game_builder_returns_all_cells_on(self):
        from models import Game
        game = Game(size=3, cells_on=True)

        for cell in game.cells:
            self.assertTrue(cell.is_on)
    
    def test_generate_id_method(self):
        from models import Game, Cell
        game = Game(size=3)

        cells_state = [True, False, True, 
                      False, True, False,
                      True, False, True]
        
        for cell, cell_state in zip(game.cells, cells_state):
            cell.is_on = cell_state

        game.generate_id()
        
        expected_id = 2**0 * cells_state[0] + 2**1 * cells_state[1] + \
                      2**2 * cells_state[2] + 2**3 * cells_state[3] + \
                      2**4 * cells_state[4] + 2**5 * cells_state[5] + \
                      2**6 * cells_state[6] + 2**7 * cells_state[7] + \
                      2**8 * cells_state[8]
        
        self.assertEqual(expected_id, game.id)
    
    def test_toggle_game_cell(self):
        from models import Game
        from copy import deepcopy

        game = Game(size=3, cells_on=True)

        possible_game_cells = [
            [False, False, True,
             False, True,  True,
             True,  True,  True],

            [False, False, False,
             True, False, True,
             True, True, True],

            [True, False, False,
             True, True, False,
             True, True, True],

            [False, True, True,
             False, False, True,
             False, True, True],

            [True, False, True,
             False, False, False,
             True, False, True],

            [True, True, False,
             True, False, False,
             True, True, False],
            
            [True, True, True,
             False, True, True,
             False, False, True],
            
            [True, True, True,
             True, False, True,
             False, False, False],
            
            [True, True, True,
             True, True, False,
             True, False, False],
        ]

        for i in range(9):
            cpy_game = deepcopy(game)
            cpy_game.toggle(i)

            game_cells_state = [cell.is_on for cell in cpy_game.cells]

            self.assertListEqual(game_cells_state, possible_game_cells[i])
    

    def test_if_return_all_possible_moves(self):
        from models import Game
        game = Game(size=3, cells_on=True)

        possible_game_cells = [
            [False, False, True,
             False, True,  True,
             True,  True,  True],

            [False, False, False,
             True, False, True,
             True, True, True],

            [True, False, False,
             True, True, False,
             True, True, True],

            [False, True, True,
             False, False, True,
             False, True, True],

            [True, False, True,
             False, False, False,
             True, False, True],

            [True, True, False,
             True, False, False,
             True, True, False],
            
            [True, True, True,
             False, True, True,
             False, False, True],
            
            [True, True, True,
             True, False, True,
             False, False, False],
            
            [True, True, True,
             True, True, False,
             True, False, False],
        ]

        for next_game, possible_cells_state in \
            zip(game.possible_moves(), possible_game_cells):
            
            game_cells_state = [cell.is_on for cell in next_game.cells]

            self.assertListEqual(game_cells_state, possible_cells_state)
    
    def test_create_list_of_cells(self):
        """
        This test verifies that all cells are connected with their neighbors.
        """

        from models import Game
        from collections import Counter
        game = Game(size=3, cells_on=True)
        cells = game.cells

        expect_neighbors = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4, 6],
            4: [1, 5, 7, 3],
            5: [2, 4, 8],
            6: [3, 7],
            7: [6, 4, 8],
            8: [7, 5]
        }

        for cell in cells:
            expect_neighbor = expect_neighbors[cell.value]
            
            cell_neighbors_set = Counter(cell.neighbors)
            expect_neighbor_set = Counter(expect_neighbor)

            self.assertEquals(cell_neighbors_set, expect_neighbor_set)
    
unittest.main()