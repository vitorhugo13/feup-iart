from eximo import Eximo
from state import *

game = Eximo('P', 'P')

start_state = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0], 
    [0, 2, 2, 0, 0, 2, 2, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 1, 1, 0, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Start())

test_state_1 = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 0, 2, 2, 2, 0], 
    [0, 0, 0, 0, 0, 2, 2, 0], 
    [0, 2, 0, 2, 0, 0, 0, 0], 
    [0, 1, 0, 0, 0, 0, 0, 0], 
    [0, 0, 1, 0, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Start())
    
    
test_state_2 = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 0, 2, 2, 2, 0], 
    [0, 2, 2, 1, 0, 2, 2, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 1, 0, 0, 0, 0, 0], 
    [0, 0, 1, 0, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Jump((5, 2)))

test_state_3 = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0], 
    [0, 0, 2, 0, 0, 0, 2, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 2, 0, 0, 1, 2, 0, 0], 
    [0, 1, 0, 2, 1, 0, 1, 0], 
    [0, 1, 1, 1, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Start())


test_state_4 = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0], 
    [0, 2, 2, 0, 0, 2, 2, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 2, 0, 0, 0, 0, 2, 0], 
    [0, 1, 1, 0, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Start())


test_state_5 = State([
    [0, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 0], 
    [0, 2, 0, 0, 0, 2, 2, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 2, 0, 0, 0, 0, 0], 
    [0, 1, 1, 0, 0, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0], 
    [0, 1, 1, 1, 1, 1, 1, 0]], 1, 16, 16, Capture((5,2)))

def test_move():
    print("North")
    state = game.move(start_state, (5, 1), (1, 0))
    if (state != None): state.print()

    print("Northwest")
    state = game.move(start_state, (6, 6), (1, -1))
    if (state != None): state.print()

    print("Northeast")
    state = game.move(start_state, (6, 5), (1, 1))
    if (state != None): state.print()

def test_jump_start():
    #north
    state = game.jump_start(test_state_1,(6,2),(1,0))
    if (state != None): state.print()
    #northeast
    state = game.jump_start(test_state_1,(6,5),(1,-1))
    if (state != None): state.print()
    #northwest
    state = game.jump_start(test_state_1,(6,6),(1,1))
    if (state != None): state.print()

def test_jump_combo():
    #JUMP_COMBO
    state = game.jump_combo(test_state_2,(1,0))
    if (state != None): state.print()


def test_capture_start():
     #north
    print('North')
    state = game.capture_start(test_state_3,(5,1),(1,0))
    if (state != None): state.print()
    #northeast
    print('NorthEast')
    state = game.capture_start(test_state_4,(5,5),(1,-1))
    if (state != None): state.print()
    #northwest
    print('NorthWest')
    state = game.capture_start(test_state_4,(5,2),(1,1))
    if (state != None): state.print()
    #east
    print('East')
    state = game.capture_start(test_state_3,(4,4),(0,-1))
    if (state != None): state.print()
    #west
    print('west')
    state = game.capture_start(test_state_3,(5,4),(0,1))
    if (state != None): state.print()

def test_capture_combo():
    #JUMP_COMBO
    state = game.capture_combo(test_state_5,(1,0))
    if (state != None): state.print()

# test_move()
# test_jump_start()
# test_jump_combo()
# test_capture_start()
# test_capture_combo()

# all okay. Need to test Place


