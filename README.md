================================================================================

Environment replication
-------------
A virtual environment manager is recommended to execute the code in the same environment. In this project, virtualenv has been used (conda or other could be used).

This project has been developed using python 3.10 but a lower version should work too.

```bash
    python3 -m venv venv
    source venv/bin/acitvate
    python3 -m pip install -r requirements.txt
```


================================================================================


================================================================================

Compile Notes
-------------

To generate a compatible executable with the game interface, execute:
```bash
    python -m PyInstaller main.py
```
The executable will be generated in dist/main/main

================================================================================

Runtime Notes
-------------

The command list is as follows:

        name        - print the name of the Game Engine.
        print       - print the board.
        exit/quit   - quit the game.
        black XXXX  - place the black stone on position XXXX in the board.
        white XXXX  - place the writing stone on the XXXX in the board, X is the A-S.
        next        - the engine will search for the move for the next step.
        move XXXX   - tell the engine that the opponent takes the move XXXX,
                        and the engine will search the move for the next step.
        new black   - start a new game and set the engine to Black player.
        new white   - start a new game and set it to White.
        depth d     - set the alpha-beta search depth, default is 6.
        help        - print this 
        genetic     - start the genetic competition.
        metrics     - get times and nodes for 10 moves for each player
