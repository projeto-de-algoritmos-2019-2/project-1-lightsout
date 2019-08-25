from copy import deepcopy

class Cell:
    """
    This class represents one of the cells of the board game. Each cell has 
    a state (on or off), has an associated value (calculated according to 
    its position), and a list of nearby neighbors.
    """
    def __init__(self, value=None, is_on=False):
        self.is_on = is_on
        self.neighbors = []
        self.value = value

class Game:
    """
    All instances of the Game class start as a game already won (all cells 
    enabled or disabled).
    
    To create a new game, it is necessary to calculate the movements from 
    the already expired game and update the necessary movements and the 
    difficulty of the generated game.
    """

    # Game difficulty
    PIECE_OF_CAKE = 0
    EASY_PEASY = 1
    NORMY = 2
    PAINFUL = 3
    HAIRLY = 4
    GOD_MODE = 5
        
    def __init__(self, size=3, cells_on=False):
        self.size = size
        self.cells = Game.create_list_of_cells(size, cells_on=cells_on)

        self.id = self.generate_id()

        self.moves_required = 0
        self.difficulty = Game.PIECE_OF_CAKE
    
    def generate_id(self):
        """
        Each game can be identified by a number calculated based on the 
        state of the board's cells. This method calculates and returns this 
        number
        """
        
        return sum([(2 ** cell.value) * cell.is_on for cell in self.cells])

    def possible_moves(self):
        """
        This method returns one by one of the possible moves from the 
        current game.
        """
        for i in range(self.size * self.size):
            game_copy = deepcopy(self)

            game_copy.toggle(position=i)

            game_copy.moves_required += 1
            game_copy.update_game_difficulty()
            game_copy.id = game_copy.generate_id()
            
            yield game_copy
        
    def update_game_difficulty(self):
        """
        This method updates the difficulty of the current game based on the 
        amount of moves required to win the game.
        """
        if self.moves_required == 0:
            self.difficulty = Game.PIECE_OF_CAKE
        
        elif self.moves_required < 3:
            self.difficulty = Game.EASY_PEASY

        elif self.moves_required < 8:
            self.difficulty = Game.NORMY
        
        elif self.moves_required < 13:
            self.difficulty = Game.PAINFUL
        
        elif self.moves_required < 21:
            self.difficulty = Game.HAIRLY
        
        elif self.moves_required < 55:
            self.difficulty = Game.GOD_MODE
    
    def toggle(self, position):
        """
        This method toggles the state of the cell at the set position and 
        all its neighbors.
        """

        self.cells[position].is_on = not self.cells[position].is_on
        neighbors = self.cells[position].neighbors
        cells = self.cells

        for i,_ in enumerate(neighbors):
            j = neighbors[i]
            cells[j].is_on = not cells[j].is_on
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __repr__(self):
        
        c = self.cells
        return f'{c[0].is_on, c[1].is_on, c[2].is_on}\n' + \
               f'{c[3].is_on, c[4].is_on, c[5].is_on}\n' + \
               f'{c[6].is_on, c[7].is_on, c[8].is_on}\n'
        
    def create_list_of_cells(size, cells_on=False):
        """
        This method create a list of cells with their respective values and 
        their respective neighbors.
        """
        
        cells = [Cell(is_on=cells_on) for _ in range(size*size)]

        for i in range(size*size):

            cells[i].value = i

            # right neighbor who is not on the right border
            if (i+1) % size:
                cells[i].neighbors.append(i+1)
                cells[i+1].neighbors.append(i)
            
            # down neighbor who is not on the bottom border
            if (i+size) < size*size:
                cells[i].neighbors.append(i+size)
                cells[i+size].neighbors.append(i)
        
        return cells