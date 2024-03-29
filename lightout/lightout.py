import os
import pickle
from models import Cell, Game
from random import choice
from collections import defaultdict, deque

from random import randint

class LightOut:
    """
    This class is responsible for generating a random game according to the 
    desired board size.

    The first time a board size is presented, this class computes all 
    desired boards and returns a random game.

    The class variable POSSIBLE_GAMES is a dictionary that for each board 
    size returns a list of all possible games to complete.

    Each game can be identified by a number formed by the sum of the values 
    of each cell on your board.
    
    Each cell has an associated value that will be used as a base exponent 2 
    multiplied by the cell state (1 if enabled, 0 if disabled).
    
    The value associated with the cell is obtained by its position in the 
    frame. Starting with 0 in the upper left cell and increasing one by one 
    for each cell, going left to right in each row.
    
    # Example for a size 3 grid:

    Associated values        grid state             Resulted value = 266
        0, 1, 2               0, 1, 0           0*2**0  +  1*2**1  +  0*2**2
        3, 4, 5       -->     1, 0, 0      ->   1*2**3  +  0*2**4  +  0*2**5
        6, 7, 8               0, 0, 1           0*2**6  +  0*2**7  +  1*2**8
    

    So, for a size 3 grid, all numbers from 0 to 511 are possible board 
    states, but some of these states are impossible games to win the game.

    For the game to always start with a board that can be completed, games 
    must be counted based on moves started on a board already won.
    """
    
    POSSIBLE_GAMES = defaultdict(list)
            
    def random_game(size, difficulty=1):
        """
        This class returns a random game based on the desired board size.
        """

        difficulty = min(5, difficulty)
        size = min(4, size)

        if not LightOut.POSSIBLE_GAMES[size]:
            
            file_name = 'size{0}grid.pkl'.format(size)
            path = os.path.join('static', file_name)

            try:
                game_list = pickle.load(open(path, 'rb'))
                LightOut.POSSIBLE_GAMES[size] = game_list
            
            except FileNotFoundError:
                game_list = LightOut.compute_all_possible_games(size)
                LightOut.POSSIBLE_GAMES[size] = game_list
                pickle.dump( game_list, open( path, "wb" ) )
        
        # print('difficulty: {0}'.format(difficulty))
        
        games_diff = [game for game in LightOut.POSSIBLE_GAMES[size] 
                        if game.difficulty == difficulty]
        
        if games_diff:
            return choice(games_diff)
        
        return choice(LightOut.POSSIBLE_GAMES[size])
        
    
    def compute_all_possible_games(size):
        """
        This class calculates all possible game boards based on the moves 
        made in a complete game, so that every generated game can be won.
        """

        possible_games = []

        gameOff = Game(size=size, cells_on=False)
        gameOn = Game(size=size, cells_on=True)

        possible_games += LightOut.bfs(gameOff)
        possible_games += LightOut.bfs(gameOn)

        # print('Qnt Valid Games: {0}'.format(len(possible_games)))
        return possible_games
    
    def best_cells_to_click(orig_game):
        """
        returns a list of the sequence of cells that must be pressed to win 
        the game as quickly as possible
        """

        # print('orig_game.moves_required: {0}'.format(orig_game.moves_required))

        visited_games_id = set()
        visited_games_id.add(orig_game.id)

        orig_game.cells_id_pressed = []
        
        queue = deque()
        queue.append(orig_game)

        while queue:

            game = queue.popleft()

            if len(game.cells_id_pressed) > orig_game.moves_required:
                continue
            
            for next_game in game.possible_moves():
                if next_game.id in visited_games_id:
                    continue
                
                ng = next_game
                ng.cells_id_pressed.append(next_game.last_position_pressed)
                    
                if next_game.is_over():
                    # print(next_game)
                    return next_game.cells_id_pressed

                
                visited_games_id.add(next_game.id)
                queue.append(next_game)
        
        return None
        
    def bfs(game, shortest_way=False):
        """
        Return all possible games derived from the game submitted as a 
        parameter
        """

        # moves_required = defaultdict(int)

        valid_games = set()
        visited_games_id = set()

        game_id = game.id
        visited_games_id.add(game_id)
        
        valid_games.add(game)

        queue = deque()
        queue.append(game)

        while queue:
            game = queue.popleft()
            
            # print(len(queue), 'moves req: {0}'.format(game.moves_required))

            for next_game in game.possible_moves():

                if next_game.id in visited_games_id:
                    continue
                
                # if moves_required[next_game.moves_required] > 25:
                    # continue
                    
                # moves_required[next_game.moves_required] += 1
                
                valid_games.add(game)
                visited_games_id.add(next_game.id)

                queue.append(next_game)
    
        return valid_games