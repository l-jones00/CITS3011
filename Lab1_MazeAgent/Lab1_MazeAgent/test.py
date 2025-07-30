import unittest
from maze_agent import MazeAgent
from maze_generator import generate_maze

GRID_SIZE = 11
MAX_MOVES = 100000

KNOWN_MAZES = [
'''#...####...
##.#...#.#.
#..#.#.#.#.
##.#.#.#.#.
#..#.#.#.#.
##.#.#.#.#.
...#.#.#.#.
.#...#...#.
.#########.
.##########
...........''',
'''...........
.#########.
.#########.
.##......#.
.##.####.#.
.##.#..#.#.
.##.#..#.#.
.##.#..#.#.
.##.#....#.
.##.######.
.##........''',
'''.#...#.....
...#.......
...#..#....
...#.......
...#.......
...........
...........
......#....
......#....
...........
.#....#....''',
'''.#.##......
.#####.##.#
.#####.##.#
.#..##.###.
.........#.
.#........#
.....#.#...
####.##.#..
##.....##..
#..#.#.#...
...##...#..'''
]

UNKNOWN_MAZES = [
    generate_maze(width=11, height=11, verbose=False),
    generate_maze(width=11, height=11, verbose=False)
]

MAZES = KNOWN_MAZES + UNKNOWN_MAZES

class TestMazeAgent(unittest.TestCase):

    def stringToMaze(self, maze_str):
        lines = maze_str.split()
        return [[lines[y][x] == "." for x in range(GRID_SIZE)] for y in range(GRID_SIZE-1, -1, -1)]

    def runMaze(self, agent, maze):
        x = GRID_SIZE - 1
        y = GRID_SIZE - 1
        count = 0
        agent.reset()
        while count < MAX_MOVES and ((x, y) != (0, 0)):
            count += 1
            move = agent.get_next_move(x, y)
            if (move == "U") and (y < GRID_SIZE-1) and maze[y+1][x]: y += 1
            elif (move == "D") and (y > 0) and maze[y-1][x]: y -= 1
            elif (move == "R") and (x < GRID_SIZE-1) and maze[y][x+1]: x += 1
            elif (move == "L") and (x > 0) and maze[y][x-1]: x -= 1
        return (x, y) == (0, 0)

    def test1(self):
        maze_str = MAZES[0]
        maze = self.stringToMaze(maze_str)
        self.assertTrue(self.runMaze(MazeAgent(), maze),
                        msg=f"did not reach end of maze within {MAX_MOVES} moves\n"+maze_str)
        print("DID NOT PASS TEST 1")

    def test2(self):
        maze_str = MAZES[1]
        maze = self.stringToMaze(maze_str)
        self.assertTrue(self.runMaze(MazeAgent(), maze),
                        msg=f"did not reach end of maze within {MAX_MOVES} moves\n"+maze_str)
        print("DID NOT PASS TEST 2")

    def test3(self):
        maze_str = MAZES[2]
        maze = self.stringToMaze(maze_str)
        self.assertTrue(self.runMaze(MazeAgent(), maze),
                        msg=f"did not reach end of maze within {MAX_MOVES} moves\n"+maze_str)
        print("DID NOT PASS TEST 3")

    def test4(self):
        maze_str = MAZES[3]
        maze = self.stringToMaze(maze_str)
        self.assertTrue(self.runMaze(MazeAgent(), maze),
                        msg=f"did not reach end of maze within {MAX_MOVES} moves\n"+maze_str)
        print("DID NOT PASS TEST 4")

    def test5(self):
        maze_str = MAZES[4]
        maze = self.stringToMaze(maze_str)
        self.assertTrue(self.runMaze(MazeAgent(), maze),
                        msg=f"did not reach end of maze within {MAX_MOVES} moves\n"+maze_str)
        print("DID NOT PASS TEST 5")

    def test6(self):
        maze_str = MAZES[5]
        maze = self.stringToMaze(maze_str)
        self.assertTrue(self.runMaze(MazeAgent(), maze),
                        msg=f"did not reach end of maze within {MAX_MOVES} moves\n"+maze_str)
        print("DID NOT PASS TEST 6")


if __name__ == "__main__":
    unittest.main()

