## Kaooa Game
It is a two player game (https://www.whatdowedoallday.com/kaooa/) that has its origin in India. 
The word `kaooa` means crow in Hindi. This game is also called vultrues vs crows.

This is implemented to demonstrate the use of the Turtle graphics library (https://docs.python.org/3/library/turtle.html) in Python. It's a very basic graphics library with tools to draw shapes & click listeners. But for advanced game development, you may checkout other libraries such as pygame.

### A description of the files
1. `turt.py`: This is the man vs computer implementation. The computer plays as the crows and the man can play as the vulture. The computer doesn't use any advanced strategy, rather makes random moves.
2. `turt_manual.py`: This is a man vs man game implementation. i.e. both the moves have to be made by the player taking turns. Note that after all the 7 crows are placed, the user must first select a crow by clicking on it and then clicking again in an empty nearby spot to move the crow there.
3. `turt_manual2.py`: This is a cleaned up version of `turt_manual.py` after running over pylint. This one also enforces a variation of the game that the vulture is forced to jump over a crow if such a move is available.
4. `kaooa.py`: The **final code**. All the previous files has been deleted, but can be found in the previous commits.

Overall, the implementation is to demonstrate the use of the `turtle` graphics library.

