import math
from typing import List, Optional, Tuple

MAX_ROWS, MAX_COLUMNS = 6, 7

class C4Agent:
##########     MOVE     ###########
    def move(self, symbol, board, last_move):
        depth = 4 #alpha-beta and iterative deepening soon

        legal = legal_moves(board) #legal is an ordered array
        if not legal:
            return 0
         
        best_val = -math.inf #set best value to -infinity so that we can maximise it
        best_col = legal[0] #no ordering yet

        for column in legal:
            child = drop_piece(board, column, symbol)
            val = minimax(child, depth-1, maximizing=False, me=symbol)
            if val > best_val:
                best_val, best_col = val, column
        return best_col


##########     HELPER FUNCTIONS TO LET 
# MINIMAX SIMULATE POSSIBILITIES     ############

def legal_moves(board):
        #Return all columns that are valid i.e. aren't full and are within row bounds
    return [c for c in range(MAX_COLUMNS) if len(board[c]) < MAX_ROWS]
    #returns a list of integers that are not full e.g. if column 2 is full, it would be [0,1,3,4,5,6]

def drop_piece(board, col, s):
        #Returns the new board with the piece dropped in the colm
    new_board = board.copy()
    new_board[col] = new_board[col] + s
    return new_board

def to_grid(board):
    #initially creates a 6x7 grid full of None
    #Loops through each column string and for each character
        #g[r][c]

    #the board looks like this: board = ["XO", "", "", "", "", "", ""]
        #i.e. column 0 has X at the bottom and then O on top
    g = [[None for i in range(MAX_COLUMNS)] for i in range(MAX_ROWS)]
    for c in range(MAX_COLUMNS):
        for r, ch in enumerate(board[c]): #using enumerate for the string "XO" to break it into g[X][0] and g[O][0]
            g[r][c] = ch
    return g

    #g will look like this
    #Row 0: ['X', None, None, None, None, None, None]   <- bottom row
    #Row 1: ['O', None, None, None, None, None, None]
    #Row 2: [None, None, None, None, None, None, None]
    #Row 3: [None, None, None, None, None, None, None]
    #Row 4: [None, None, None, None, None, None, None]
    #Row 5: [None, None, None, None, None, None, None]   <- top row

def check_winner(board, s):
    #true if s has a 4-in-a-way anywhere

    g = to_grid(board)

    #what does it mean to have 4-in-a-row
    def four(r, c, dr, dc):
        for i in range(4):
            rr, cc = r+i*dr, c+i*dc
            if not (0 <= rr < MAX_ROWS and 0 <= cc < MAX_COLUMNS):
                return False
            if g[rr][cc] != s:
                return False
        return True

    for r in range(MAX_ROWS):
        for c in range(MAX_COLUMNS):
            if g[r][c] != s:
                continue
            if (four(r, c, 0, 1) or    # →
                four(r, c, 1, 0) or    # ↑
                four(r, c, 1, 1) or    # ↗
                four(r, c, 1, -1)):    # ↖
                return True
    return False

def is_full(board):
    return all(len(board[c]) >= MAX_ROWS for c in range(MAX_COLUMNS))

def is_terminal(board):
    if check_winner(board, 'X'):
        return True, 'X'
    if check_winner(board, 'O'):
        return True, 'O'
    if is_full(board):
        return True, None
    return False, None

##########     EVALUATION FOR VALUES     ############

def evaluate(board, me):
    opp = '0' if me == 'X' else 'X'
    g = to_grid(board)

    total = 0
    for window in generate_windows(g):
        total += eval_set_basic(window, me, opp)
    return total    

def generate_windows(g):
    windows = []

    # Horizontal
    for r in range(MAX_ROWS):
        for c in range(MAX_COLUMNS - 3):
            windows.append([g[r][c+i] for i in range(4)])

    # Vertical
    for c in range(MAX_COLUMNS):
        for r in range(MAX_ROWS - 3):
            windows.append([g[r+i][c] for i in range(4)])

    # Diagonal ↗
    for r in range(MAX_ROWS - 3):
        for c in range(MAX_COLUMNS - 3):
            windows.append([g[r+i][c+i] for i in range(4)])

    # Diagonal ↖
    for r in range(MAX_ROWS - 3):
        for c in range(3, MAX_COLUMNS):
            windows.append([g[r+i][c-i] for i in range(4)])

    return windows
def eval_set_basic(window, me, opp):
    my_count = sum(1 for x in window if x==me)
    opp_count = sum(1 for x in window if x==opp)

    my_score  = my_count  if opp_count == 0 else 0
    opp_score = opp_count if my_count  == 0 else 0
    return my_score - opp_score

def minimax(board, depth, maximizing, me):
    #if maximizing is true, then me is playing
    #return evaluation from the perspective of me

    opp = 'O' if me == 'X' else 'X'
    terminal, winner = is_terminal(board)

    terminal, winner = is_terminal(board)
    
    if terminal:
        if winner == me:
            return 10_000  # big positive for a win
        elif winner == opp:
            return -10_000 # big negative for a loss
        else:
            return 0 #draw
    
    if depth == 0:
        return evaluate(board, me)
    
    if maximizing:
        best = -math.inf
        for col in legal_moves(board):
            child = drop_piece(board, col, me)
            best = max(best, minimax(child, depth - 1, False, me))
        return best
    else:
        best = math.inf
        for col in legal_moves(board):
            child = drop_piece(board, col, opp)
            best = min(best, minimax(child, depth - 1, True, me))
        return best