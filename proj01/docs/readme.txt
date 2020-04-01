EXIMO

Instructions

Run program
1. Python3 or higher needed to run the program
2. It is necessary to install the colorama module (https://pypi.org/project/colorama/) to be able to view colors in the terminal.
3. To run the program just enter the command "python3 main.py" in the correct directory (/src)


Game
1. First menu allows you to select the game mode (1-4) or exit the game (0)
2. 
   2.1. if the selected game mode is 'Player vs Player' the game will start immediately
   2.2. otherwise, if the selected mode involves a player being the computer, a second menu is displayed that allows you to select the desired heuristic, followed by an input that allows you to enter the computer level(note that this level corresponds to the depth of search)


How to make a move
1. The red pieces represent player1, while the blue pieces correspond to player 2
2. In the next step it is necessary to choose the piece that will make the move
   2.1. choose row(1-8)
   2.2. choose column(A-H)
   2.3. whenever the piece is not valid or an error occurs in the input, the program asks for the piece to be selected again.(IMPORTANT: if it is possible, it is mandatory to make captures, the game will check and if the selected piece is not one that can capture it asks to be introduced again)
3. select capture direction(if any more catch / jump is possible, the prompt to enter direction will appear again)



Bernardo Santos (up201706534)
João Matos      (up201705471)
Vítor Gonçalves (up201703917)
