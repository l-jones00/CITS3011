# Lab 1: Maze Agent

Using Python, write a basic agent that can navigate a maze. In `maze_agent.py`, there is an incomplete class `MazeAgent`, which you need to implement.

The agent initially does not know the layout of the maze. It must explore to find its way to the goal. The maze is a 11 by 11 grid of cells, where some cells are empty and some are solid walls. The agent cannot enter a cell that is a solid wall, and cannot go beyond the edge of the grid. If the agent tries to make an invalid move, it will remain at its current location.

The agent starts from the cell (10,10), which is the top-right corner of the grid.
The agent's goal is to reach the cell (0,0), which is the bottom-left corner of the grid.

The agent makes observations: It always knows its current position (x and y coordinates).

The agent can perform actions: At every decision point, it can choose to move Left, Right, Up, or Down.

The agent must attempt to move around the grid to reach the cell (0,0), building a model of the environment as it goes. If a move is unsuccessful (so it stays where it is), the agent can deduce that the cell it tried to move to is a solid wall. This information can allow it to efficiently navigate a maze.

You need to implement the `reset` and `get_next_move` methods in `MazeAgent`.

The method `reset(self)` is where you can set up any variables and data structures you need (e.g. `self.previous_location`). The tester will call `reset` whenever the agent is moved into a new maze.

The method `get_next_move(self, x, y)` is where the agent chooses which move to make. The tester will call `get_next_move`, giving the current x and y coordinates as parameters x and y, and expecting a move to be returned. The method must return either `"L"`, `"R"`, `"U"`, or `"D"` (meaning Left, Right, Up, or Down), indicating the direction the agent will attempt to move. (Returned value should be a string containing a single letter character.)

The tester will place the agent in a maze, then call the agent's `reset` method, and then repeatedly call `get_next_move` (up to 300 times). In each repetition, the tester gives the current x and y coordinates to the agent, receive the returned string from the agent, and then moves the agent in that direction (if possible), before moving on to the next repetition.

The agent is successful if it reaches the goal within 300 moves.

How to run the tester, in a terminal:
```
python3 test.py
```

Extra notes:
* For the tester to work, `maze_agent.py` and `test.py` must be in the same folder.
* If you have not seen `self` before, it is a part of object-oriented Python. It refers to the current object / the current instance of the class.

Example:
```
...........
...........
...........
....##X....
....##.....
....##.....
....##.....
....##.....
....##.....
...........
...........
```
If the agent is currently at the position indicated by the `X` symbol, its coordinates are (6,7). It tries to move left, to position (5,7), but it ends up back at (6,7). Because it did not move, the agent can infer there is a solid wall at position (5,7). The agent stores this information in a data structure, for later use.