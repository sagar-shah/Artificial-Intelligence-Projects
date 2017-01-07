# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, August 2016
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import time

start_time = time.clock()

# This is N, the size of the board.
N = 11
print "N=", N

# Count # of pieces in given row
def count_on_row(board, row):
    return sum(board[row])


# Count # of pieces in given column
def count_on_col(board, col):
    return sum([row[col] for row in board])

# Count # of pieces in a diagonal
def count_on_diagonal(board, row , col):
    c = col
    r = row
    count = 0
    while row > 0 and col > 0 and row<=N and col<=N:
        row -= 1
        col -= 1
        if board[row][col] == 1:
            count += 1
#    print count
    row = r
    col = c
    while row > 0 and col >= 0 and row<=N and col<N-1:
        row -= 1
        col += 1
#        print row,col
        if board[row][col] == 1:
            count += 1

    row = r
    col = c
    while row >= 0 and col > 0 and row<N-1 and col<=N:
        row += 1
        col -= 1
        if board[row][col] == 1:
            count += 1

    row = r
    col = c
    while row >=0 and col >=0 and row<N-1 and col<N-1:
        row += 1
        col += 1
        if board[row][col] == 1:
            count += 1

    if board[r][c] == 1:
        count +=1

    return count
# Count total # of pieces on board
def count_pieces(board):
    return sum([sum(row) for row in board])


# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([" ".join(["Q" if col else "_" for col in row]) for row in board])


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1, ] + board[row][col + 1:]] + board[row + 1:]


# Get list of successors of given board state
# def successors(board):
#    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# Get list of successors of given board state
def successors(board):
    return [add_piece(board, r, c) for r in range(0, N) for c in range(0, N)]


# Get list of successors of given board state
def successors2(board):
    if count_pieces(board) >= N:
        return []

    return_list = []
    for c in range(0, N):
        for r in range(0, N):
#            x = board[r][c]
            if board[r][c] == 0:
                return_list.append(add_piece(board, r, c))
    return return_list


#    return [  add_piece(board, r, c) if board[r][c] == 0 else pass for r in range(0, N) for c in range(0,N) ]

# Get list of successors of given board state - rooks
def successors3(board):
    if count_pieces(board) >= N:
        return []
    # if any( [ count_on_row(board, r) > 1 for r in range(0, N) ] ):
    #     return []
    # if any( [ count_on_col(board, r) > 1 for r in range(0, N) ] ):
    #     return []

    return_list = []
    for c in range(0, N):
        for r in range(0, N):
            if board[r][c] == 0 and count_on_row(board, r) == 0 and count_on_col(board, c) == 0:
                return_list.append(add_piece(board, r, c))
#                return return_list
    return return_list

# Get list of successors of given board state - queens
def nqueens_successors3(board):
    if count_pieces(board) >= N:
        return []
    # if any( [ count_on_row(board, r) > 1 for r in range(0, N) ] ):
    #     return []
    # if any( [ count_on_col(board, r) > 1 for r in range(0, N) ] ):
    #     return []

    return_list = []
    for c in range(0, N):
        for r in range(0, N):
            if board[r][c] == 0 and count_on_row(board, r) == 0 and count_on_col(board, c) == 0 and count_on_diagonal(board,r,c) == 0:
                return_list.append(add_piece(board, r, c))
 #               return return_list
    return return_list

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
           all([count_on_row(board, r) <= 1 for r in range(0, N)]) and \
           all([count_on_col(board, c) <= 1 for c in range(0, N)])

# check if board is a goal state
def nqueens_is_goal(board):
#    print "count= ",count_on_diagonal(board,3,2)
    return count_pieces(board) == N and \
           all([count_on_row(board, r) <= 1 for r in range(0, N)]) and \
           all([count_on_col(board, c) <= 1 for c in range(0, N)]) and is_diagonal_valid(board)
#            all([ count_on_diagonal(board,r,c) <=1 if board[r][c] == 1 for r in range(0, N) for c in range(0, N)])

#This checks if the diagonals that contain the queens are valid.
def is_diagonal_valid(board): 
    for c in range(0,N):
        for r in range(0,N):
            if board[r][c] == 1:
                if count_on_diagonal(board,r,c) > 1:
                    return False
    return True

# Solve n-rooks! DFS - successors
# def solve(initial_board):
#     fringe = [initial_board]
#     while len(fringe) > 0:
#         for s in successors( fringe.pop() ):
#             if is_goal(s):
#                 return(s)
#             fringe.append(s)
#     return False

# Solve n-rooks! BFS - successors
# def solve(initial_board):
#     fringe = [initial_board]
#     while len(fringe) > 0:
#         for s in successors( fringe.pop(0) ):
#             if is_goal(s):
#                 return(s)
#             fringe.append(s)
#     return False

# Solve n-rooks! DFS - successors2
# def solve(initial_board):
#     fringe = [initial_board]
#     while len(fringe) > 0:
#         for s in successors2( fringe.pop() ):
#             if is_goal(s):
#                 return(s)
#             fringe.append(s)
#     return False

# Solve n-rooks! BFS - successors2
# def solve(initial_board):
#     fringe = [initial_board]
#     while len(fringe) > 0:
#         for s in successors2( fringe.pop(0) ):
#             if is_goal(s):
#                 return(s)
#             fringe.append(s)
#     return False

# Solve n-rooks! BFS - successors3
# def solve(initial_board):
#     fringe = [initial_board]
#     while len(fringe) > 0:
#         for s in successors3( fringe.pop(0) ):
#             if is_goal(s):
#                 return(s)
#             fringe.append(s)
#     return False

# Solve n-rooks! DFS - successors3
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# Solve n-queens! DFS - successors3
def nqueens_solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in nqueens_successors3( fringe.pop() ):
            if nqueens_is_goal(s):
                return(s)
            fringe.append(s)
    return False

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0] * N] * N

print "Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n"
print "NROOKS"
solution = solve(initial_board)
# b=[[0,1,0,0],[0,0,0,1],[1,0,0,0],[0,0,1,0]]
# print Q_is_goal(b)
# print count_on_diagonal(b,2,3)
# print Qsuccessors3(b)
print printable_board(solution) if solution else "Sorry, no solution found. :("
print "NQUEENS"
solution = nqueens_solve(initial_board)
print printable_board(solution) if solution else "Sorry, no solution found. :("

print time.clock() - start_time, "seconds", "N= ",N
