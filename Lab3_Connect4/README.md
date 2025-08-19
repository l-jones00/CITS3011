# Lab 3: Connect Four

Using Python, write an agent that can play the game Connect Four.

Start with the code given in `connect4.py`, and implement the `move` method. (You can add more methods to the `C4Agent` class if you need to.)

The `move` method is given these parameters:
* `symbol` A single-character string `"X"` or `"O"`, indicating which game pieces belong to you
* `board` A list of 7 strings. Each string represents a column of the game board, made up of the characters `"X"` and `"O"` which represent game pieces. (The first character of a string represents the bottom row. Note that the strings are initially empty and grow throughout the game to a maximum length of 6.)
* `last_move` Your opponent's last move, the index of the column they chose to place a game piece. (`last_move` will be `-1` if you are making the first move of the game)

The `move` method must return a single integer, the index of the column where you are choosing to place a game piece.

If you make an invalid move, you will automatically lose the game.

Invalid moves:
* A number outside of the range [0-6] (the game board has 7 columns)
* The index of a column that is already full (each column can hold up to 6 pieces)

The tester will run your code by calling the `move` method. It will call `move` whenever it is your agent's turn to make a move in the game.

How to run the tester, in a terminal:
```
python3 test.py
```

The first test will pitch your agent against a random opponent four times, and your agent needs to win all games to pass. At the end of the game you are given a string representation of the board. Your discs are labelled 'A', 'B', 'C',... and the opponents are 'a','b','c',... so you can infer the order they were played. 

The second test requires your agent to beat a simple 2-ply minimax agent.

**Hint:** Consider your options such as minimax, alpha-beta pruning, etc. Which of these do you expect to perform the best?
