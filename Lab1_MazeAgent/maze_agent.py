
class MazeAgent():
    def reset(self):
        self.visited = set()
        self.walls = set()
        self.prev_pos = (10,10)
        self.moves = [] # so path can be reversed if need be
        self.directions = { # dictionary - use items() to return
            #[("U", (0, 1)), ("D", (0, -1)), ("L", (-1, 0)), ("R", (1, 0))]
           "D": (0, -1),
           "L": (-1, 0),
           "U": (0, 1),
           "R": (1, 0)
        }
        
    def get_next_move(self, x, y):
        current_pos = (x,y)

        if current_pos == self.prev_pos and self.moves: #ie if not the first position, and move failed last time
            last_move = self.moves.pop()
            dx, dy = self.directions[last_move]
            self.walls.add((x+dx, y+dy))
            #print("Adding (", x+dx, ",", y+dy, ") to walls")

        #add current position to visited list
        if current_pos not in self.visited:
            self.visited.add(current_pos)
        
        #now try and move 
        for move, (dx, dy) in self.directions.items():
            if (dx+x, dy+y) not in self.walls and (dx+x, dy+y) not in self.visited:
                self.moves.append(move)
                self.prev_pos = current_pos
                #print("Going to try and go", move, "\nEnd turn")
                return move
        
        #if none of these work
        if self.moves:
            last_move = self.moves.pop()
            opposite = {"U": "D", "D": "U", "L": "R", "R": "L"}
            move = opposite[last_move]
            self.prev_pos = current_pos
            #print("Backtracking by going", move, "\nEnd turn")
            return move


#agent checks its current position and compares to past_position
#if it's the same, then you know the last_move was into a wall. add that to the wall set using dictionary + current position 
#try and move down, left, then up and right. For each move, check that the new_pos is not in walls or visited, then return move
        #what if it's a circle? 
#if none of those moves work, backtrack one by reversing last_move


