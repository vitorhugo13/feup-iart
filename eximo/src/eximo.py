from copy import copy

class State:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def print(self):
        print('    A   B   C   D   E   F   G   H')
        print('   --------------------------------')
        for i in range(len(self.board)):
            print(str(i) + ' | ' + ' | '.join(str(cell) for cell in self.board[i]) + ' |')
            print('  | -   -   -   -   -   -   -   -')

def add(t1: tuple, t2: tuple) -> tuple:
    return (t1[0] + t2[0], t1[1] + t2[1])
def mult(t: tuple, f: int) -> tuple:
    return (t[0] * f, t[1] * f)

class Eximo:
    start_state = State([ [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0], 
                    [0, 1, 1, 0, 0, 1, 1, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 2, 2, 0, 0, 2, 2, 0], 
                    [0, 2, 2, 2, 2, 2, 2, 0], 
                    [0, 2, 2, 2, 2, 2, 2, 0]], 1)

    def __init__(self, player1: str, player2: str):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        while True:
            self.select_cell()
        
    def game_over(self, state: State) -> bool:
        if state.board.count(1) == 0:
            print("player 2 won")
            return True
        elif state.board.count(2) == 0:
            print("player 1 won")
            return True
        return False

    def select_cell(self) -> tuple:
        row = 0
        col = 0
        while row < 1 or row > 8:
            row = int(input('Row (1-8): '))
        while col < 1 or col > 8:
            col = ord(input('Col (A-H): ').lower()) - 96
        return (row, col)

    def get_piece(self, state: State, pos: tuple) -> int:
        return state.board[pos[0]][pos[1]]

    def place_piece(self, state: State, pos: tuple, piece: int) -> None:
        state.board[pos[0]][pos[1]] = piece

    def is_empty(self, state: State, pos: tuple) -> bool:
        return self.get_piece(state, pos) == 0
    
    # True if the piece on the position belongs to the player that is making the move
    def is_players(self, state: State, pos: tuple) -> bool:
        return self.get_piece(state, pos) == state.player
    
    def is_opponents(self, state: State, pos: tuple) -> bool:
        return not self.is_empty(state, pos) and not self.is_players(state, pos)

    # returns the movement direction multiplier 
    def get_direction(self, state: State) -> int:
        if state.player == 2:
            return -1
        return 1
    
    def valid_position(self, pos: tuple) -> bool:
        return pos[0] >= 0 and pos[0] <= 7 and pos[1] >= 0 and pos[1] <= 7


    # ORDINARY MOVE OPERATORS
    def move(self, state: State, pos: tuple, vec: tuple) -> State:
        if not self.is_players(state, pos):
            return state
        
        dir = self.get_direction(state)
        n_pos = add(pos, mult(vec, dir))

        if not self.valid_position(n_pos):
            return state
        if not self.is_empty(state, n_pos):
            return state
        
        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.place_piece(n_state, n_pos, state.player)
        
        return n_state

    def move_north(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, 0))
    def move_north_east(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, -1))
    def move_north_west(self, state: State, pos: tuple) -> State:
        return self.move(state, pos, (1, 1))

    # JUMP MOVE OPERATORS
    def jump(self, state: State, pos: tuple, vec: tuple) -> State:
        if not self.is_players(state, pos):
            return state

        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_players(state, t_pos):
            return state
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return state

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.place_piece(n_state, n_pos, state.player)
        
        return n_state

    def jump_north(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, 0))
    def jump_north_east(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, -1))
    def jump_north_west(self, state: State, pos: tuple) -> State:
        return self.jump(state, pos, (1, 1))

    # CAPTURE OPERATORS
    def capture(self, state: State, pos: tuple, vec: tuple) -> State:
        if not self.is_players(state, pos):
            return state

        dir = self.get_direction(state)

        t_pos = add(pos, mult(vec, dir))
        if not self.valid_position(t_pos) or not self.is_opponents(state, t_pos):
            return state
        
        n_pos = add(pos, mult(vec, dir * 2))
        if not self.valid_position(n_pos) or not self.is_empty(state, n_pos):
            return state

        n_state = copy(state)
        self.place_piece(n_state, pos, 0)
        self.place_piece(n_state, t_pos, 0)
        self.place_piece(n_state, n_pos, state.player)
        
        return n_state

    def capture_north(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (1, 0))
    def capture_east(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (0, -1))
    def capture_north_east(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (1, -1))
    def capture_west(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (0, 1))
    def capture_north_west(self, state: State, pos: tuple) -> State:
        return self.capture(state, pos, (1, 1))


game = Eximo('P', 'P')
game.capture_north(game.start_state, (1, 3)).print()

