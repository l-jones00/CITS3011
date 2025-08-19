import math
from typing import List, Optional, Tuple

MAX_ROWS, MAX_COLUMNS, WIN_SCORE = 6, 7, 10000

class C4Agent:
    def move(self, symbol, board, last_move):
        """Iterative deepening wrapper around alpha–beta."""
        legal = legal_moves(board)
        if not legal:
            return 0

        # start with simple center-first ordering
        order = sorted(legal, key=lambda c: abs(c - 3))

        best_col = order[0]
        best_val = -float('inf')
        MAX_DEPTH = 6

        for depth in range(1, MAX_DEPTH + 1):
            iter_best_col = order[0]
            iter_best_val = -math.inf

            for col in order:
                child = drop_piece(board, col, symbol)           # you play here
                val = alphabeta(child, depth-1, -math.inf, math.inf, False, symbol, last_col=col, last_sym=symbol)
                if val > iter_best_val:
                    iter_best_val = val
                    iter_best_col = col

            # keep deepest completed result
            best_col, best_val = iter_best_col, iter_best_val

            # principal variation move ordering for next iteration
            order = [iter_best_col] + [c for c in order if c != iter_best_col]

            # optional early stop: found a forced win at this depth
            if iter_best_val >= WIN_SCORE - depth:
                break

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

def _has_piece(board, r, c, s):
    # fast read: column bounds, row within that column's string length, and char match
    return (0 <= c < MAX_COLUMNS and 0 <= r < MAX_ROWS and
            r < len(board[c]) and board[c][r] == s)

def _count_one_dir(board, r, c, dr, dc, s):
    cnt = 0
    rr, cc = r + dr, c + dc
    while _has_piece(board, rr, cc, s):
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def won_from_last(board, last_col, last_sym):
    """Return True iff the last move (in column last_col by last_sym) creates a 4-in-a-row."""
    if last_col < 0:  # first move case
        return False
    r = len(board[last_col]) - 1
    c = last_col
    for dr, dc in ((1,0), (0,1), (1,1), (1,-1)):
        total = 1 + _count_one_dir(board, r, c, dr, dc, last_sym) + _count_one_dir(board, r, c, -dr, -dc, last_sym)
        if total >= 4:
            return True
    return False

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

def alphabeta(board, depth, alpha, beta, maximizing, me, last_col=-1, last_sym=None):
    """Alpha–beta minimax, scoring from `me`'s perspective."""
    opp = 'O' if me == 'X' else 'X'

     # Fast terminal: check the last move only
    if last_col != -1 and last_sym is not None:
        if won_from_last(board, last_col, last_sym):
            # That last move just made is a win for last_sym
            return (WIN_SCORE + depth) if last_sym == me else (-WIN_SCORE - depth)
    
    # Draw check: if no legal moves remain
    moves = [c for c in range(MAX_COLUMNS) if len(board[c]) < MAX_ROWS]
    if not moves:
        return 0
    
    if depth == 0:
        return evaluate(board, me)

    # Move ordering 
    moves.sort(key=lambda c: abs(c - 3))

    #recursive minimax
    if maximizing:
        value = -float('inf')
        for col in moves:
            child = board.copy()
            child[col] = child[col] + me        # you place
            score = alphabeta(child, depth-1, alpha, beta, False, me, last_col=col, last_sym=me)
            if score > value:
                value = score
            if value > alpha:
                alpha = value
            if alpha >= beta:  # β-cut
                break
        return value
    else:
        value = float('inf')
        for col in moves:
            child = board.copy()
            child[col] = child[col] + opp       # opponent places
            score = alphabeta(child, depth-1, alpha, beta, True, me, last_col=col, last_sym=opp)
            if score < value:
                value = score
            if value < beta:
                beta = value
            if alpha >= beta:  # α-cut
                break
        return value