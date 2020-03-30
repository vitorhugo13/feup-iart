from state import *

#numero de peças do jogador - número de peças do adversário
def subtraction(state: State) -> int:
    return state.score[state.player % 2 + 1] - state.score[state.player]

# numero de peças do jogador multiplicado por um fator no placement
def placement_factor(state: State) -> int:
    if state.action == 4:
        return state.score[state.player] 
    else:
        return state.score[state.player % 2 +1] * 2

# prioritizar o move invés do jump
def prioritize_jump(state: State) -> float:
    if state.action == 1:
        return state.score[state.player % 2 +1]* 1.5
    elif state.action == 2:
        return state.score[state.player % 2 +1] * 0.5
    else:
        return state.score[state.player % 2 +1]

#number of available moves
def available_moves(state: State):
    moves = state.get_children()
    return len(moves)

# prioritize side columns
def side(state: State) -> int:
    score = 0    
    for row in state.board:
        for col, piece in enumerate(row):
            if not piece == state.player % 2 + 1:
                continue
            
            if col == 0 or col == 7:
                score += 4
            elif col == 1 or col == 6:
                score += 3
            elif col == 2 or col == 5:
                score += 3
            elif col == 3 or col == 4:
                score += 1

    return score

# side heuristic variation
def side2(state: State) -> int:
    score = 0    
    for row in state.board:
        for col, piece in enumerate(row):
            if not piece == state.player % 2 + 1:
                continue
            
            if col == 0 or col == 7:
                score += 7
            elif col == 1 or col == 6:
                score += 5
            elif col == 2 or col == 5:
                score += 2
            elif col == 3 or col == 4:
                score += 1

    return score


# prioritize center rows
def center(state: State) -> int:
    score = 0    
    for row, list in enumerate(state.board):
        for col, piece in enumerate(list):
            
            if not piece == state.player % 2 + 1:
                continue
            
            if col == 0 or col == 7:
                score += 1
            elif col == 1 or col == 6:
                score += 3
            elif col == 2 or col == 5:
                score += 6
            elif col == 3 or col == 4:
                score += 9

            # player 1
            if state.player == 2:
                score += 7 - row
            # player 2
            else:
                score += row        
    return score

# prioritize advancing on the board
def forward(state: State) -> int:
    score = 0    
    for row in state.board:
        for col, piece in enumerate(row):
            
            if not piece == state.player % 2 + 1:
                continue

            # player 1
            if state.player == 2:
                score += 7 - row
            # player 2
            else:
                score += row                
    return score
            
#exploiting symmetry at the board               
