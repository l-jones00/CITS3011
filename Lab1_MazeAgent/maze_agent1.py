
class MazeAgent():
    def reset(self):
        self.visited = set()
        self.walls = set()
        self.prev_pos = (10,10)
        self.current_path = [] # so path can be reversed if need be
        self.directions = { # dictionary - use items() to return
            #[("U", (0, 1)), ("D", (0, -1)), ("L", (-1, 0)), ("R", (1, 0))]
           "D": (0, -1),
           "L": (-1, 0),
           "U": (0, 1),
           "R": (1, 0)
        }
        
    def get_next_move(self, x, y):
        current_pos = (x,y)
        
        #if last move didn't work, the current_pos == self.prev_pos
        #add to wall
        if self.prev_pos == current_pos and self.current_path:
            last_move = self.current_path.pop()
            dx, dy = self.directions[last_move]
            blocked = (x + dx, y + dy)
            self.walls.add(blocked)
        
        #mark current position as visited
        self.visited.add(current_pos) #add > start, append > end
        
        #check all possible unexplored directions > prioritises down, then left, then the others
        for move, (dx, dy) in self.directions.items():
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            if (0 <= nx < 11) and (0 <= ny < 11):
                if next_pos not in self.visited and next_pos not in self.walls:
                    self.current_path.append(move)
                    self.prev_pos = current_pos
                    return move
        
        #if none of the possible directions work, backtrack
        if self.current_path and self.current_path:
            last_move = self.current_path.pop()
            opposite = {"U": "D", "D": "U", "L": "R", "R": "L"}
            move = opposite[last_move]
            self.current_path.append(opposite[move])
            self.prev_pos = current_pos
            return move
            
                    
        
        
        pass # should return 'U' 'D', 'L', 'R'
