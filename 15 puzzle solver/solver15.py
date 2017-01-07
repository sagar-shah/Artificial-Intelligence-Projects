# solver15.py
#
# The 15 tile puzzle problem is: From any given initial configuration, our goal is to find the shortest possible sequence
# of moves that restores the canonical configuration (all tiles in ascending order)

# I have used to A* approach to solve the above mentioned problem. Since our heuristic function (explained below)
# is admissible and consistent, we avoid re-visiting the already visited states by keeping a track of them in a list.
# 1)Abstraction:
# a) State Space: The state space of the problem contains all the successor states that can be generated from the
# initial configuration, until the goal is reached
# b) Successor Function: From any given state, the successor function generates 4 new states, by swapping a tile from
# each direction (L,R,U,D). We avoid visiting repeated states by
# c) Cost Function/Edge Weight: For each move a cost of 1 is added
# d) Heuristic Function: I have used the (modified) Manhattan Distance to calculate the Heuristic Cost of a State.
# By modified,I mean that I have incorporated the "important change" ie. the tiles being able to iterate over the edges.
# In some cases, it can reduce the usual Manhattan Distance for a tile, and by taking care of that, I have maintained
# the admissibility and the consistency of the heuristic function. Kindly refer the heuristic_cost() for more clarification.
# e) Goal State: The goal state is the state with all tiles in the ascending order.
# I am storing the coordinates of the goal state in goal_board_final to check if the goal state has been reached or not.
#
# 2) Working:
# Its a simple A* Search Algorithm with admissible and consistent heuristics (as explained above)
# It initially converts the input file into a initial_list which is then converted to a dictionary called initial_state_global
# Each successor state is then stored in the same format as this dictionary
# These dictionaries contain the following keys:
# a) grid: Stores the grid values and their coordinates
# b) moves: Stores all the moves done to reach the current state from the initial state
# c) level: The level (or the g(s) = distance of the current state from the initial state)
# The initial_list is passed to the is_solution()-->permutation_inversion() function, which determines the solvability of the initial board
# If it is even, only then the board is solvable, else the program says "Sorry, no solution found"
# If solvable, the initial_state_global dict is then passed to the solve() function.
# It contains 'fringe'(a priority queue-to keep a track of generated successors) and
# 'closed' (a list-to keep a track of visited states)
# We ignore the already visited states and do not add them to the fringe.
# Since the heuristic is admissible and consistent, we will always get the optimal path to the goal.

# 3)
# a) Challenges: Balancing between the priority queue functionality and its looping cost (to find whether a state already exists in the fringe)
# Created a list_fringe_track list which is kind of a duplicate of the fringe, to minimize the looping cost.

# b) Design Decisions: Implemented the state as a dict rather than a list of lists, so as to reduce the iterations while swapping and generating successors.
# Each state also contains the level and the moves. Advantages of which are as follows:
# Moves: Stoes moves of each state, so as to avoid any back tracking for the final set of moves upon reaching the goal state.
# Level: To calculate the g(s) of the successor state

# Based on the board size ie. N, the code can also work for some configurations of a 24 tile puzzle (N=5)


# Other Heuristics:
# Except for Manhattan, I had tried the following:
# a) No of misplaced tiles: Works worst than the Manhattan Distance
# b) Manhattan + Linear Conflict: Linear conflict adds 2 to the Manhattan distance, incase there is any linear conflicts
# (a greater no is ahead of a smaller no) in the same row. But in some cases, adding this makes our heuristic as non-admissible,
# since we can flip the slides from the border.
# c) Pattern Heuristics:

import copy
import time
import sys
from Queue import PriorityQueue

initial_list = []
initial_state_global = {}
goal_board = {}
goal_board_final = {}
# This is N, the size of the board.
N = 4
if N == 5:
    # Goal boards for 24 board puzzle
    goal_board={1:(0,0), 2:(0,1), 3:(0,2), 4:(0,3), 5:(0,4), 6:(1,0), 7:(1,1), 8:(1,2), 9:(1,3), 10:(1,4), 11:(2,0), 12:(2,1), 13:(2,2), 14:(2,3), 15:(2,4), 16:(3,0), 17:(3,1), 18:(3,2), 19:(3,3), 20:(3,4), 21:(4,0), 22:(4,1), 23:(4,2), 24:(4,3), 0:(4,4)}
    goal_board_final={(0,0):1, (0,1):2, (0,2):3, (0,3):4, (0,4):5, (1,0):6, (1,1):7, (1,2):8, (1,3):9, (1,4):10, (2,0):11, (2,1):12, (2,2):13, (2,3):14, (2,4):15, (3,0):16, (3,1):17, (3,2):18, (3,3):19, (3,4):20, (4,0):21, (4,1):22, (4,2):23, (4,3):24, (4,4):0}
else:
    # Goal boards for 15 board puzzle
    goal_board = {0: (3, 3), 1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
                  9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3), 13: (3, 0), 14: (3, 1), 15: (3, 2)}
    goal_board_final = {(3, 3): 0, (0, 0): 1, (0, 1): 2, (0, 2): 3, (0, 3): 4, (1, 0): 5, (1, 1): 6, (1, 2): 7, (1, 3): 8,
                        (2, 0): 9, (2, 1): 10, (2, 2): 11, (2, 3): 12, (3, 0): 13, (3, 1): 14, (3, 2): 15}


# Checks if the current state is a goal state or not
def is_goal(board):
    return True if board['grid'] == goal_board_final else False


# Initializes the board from the input file and stores in the initial_state_global dict
def initialize(ini_list):
    global initial_state_global
    initial_state_global['moves'] = ''
    initial_state_global['level'] = 0
    grid = {}
    for x in range(0, N):
        for y in range(0, N):
            grid[x, y] = ini_list[(N * x) + y]
    initial_state_global['grid'] = grid


# Returns the "permutation inversion + zero row" value for an input list
def permutation_inversion(ini_list):
    p_inversion = 0
    zero_row = 1
    for x in range(0, len(ini_list)):
        if ini_list[x] == 0:
            zero_row += divmod(x, N)[0]
        else:
            for y in range(x + 1, len(ini_list)):
                if ini_list[x] > ini_list[y] > 0:
                    p_inversion += 1
    print "Permutation Inversion:", p_inversion + zero_row
    return p_inversion + zero_row


# Uses permutation inversion == even (ie. the precomputed permutation inversion of our goal state) logic to check if solution present
def is_solution(ini_list):
    return True if divmod(permutation_inversion(ini_list), 2)[1] == 0 else False


# Calculates and returns the heuristic cost h(s) for a state
def heuristic_cost(board):
    # global goal_board
    h_cost = 0
    for key, val in board['grid'].iteritems():
        # Skips calculating the permutation inversion of the empty tile
        if val != 0:
            xn = key[0]
            yn = key[1]
            xg = goal_board[val][0]
            yg = goal_board[val][1]
            d1 = abs(xn - xg)
            d2 = abs(yn - yg)
            if d1 == N - 1:
                d1 = 1
            if d2 == N - 1:
                d2 = 1
            h_cost += (d1 + d2)
    return h_cost


# Calculates and returns the evaluation cost f(s)= g(s) + h(s) for a state
def evaluation_cost(board):
    # current_cost = board['level'] * 0.5
    current_cost = board['level']
    return current_cost + heuristic_cost(board)


# Swaps the tile in Right direction and also updates the corresponding move and the level of the state
def swap_right(board1, x, y):
    if y == 0:
        board1['grid'][x, y] = board1['grid'][x, N - 1]
        board1['grid'][x, N - 1] = 0
    else:
        board1['grid'][x, y] = board1['grid'][x, y - 1]
        board1['grid'][x, y - 1] = 0
    board1['moves'] += 'R '
    board1['level'] += 1
    return board1


# Swaps the tile in Left direction and also updates the corresponding move and the level of the state
def swap_left(board2, x, y):
    if y == N - 1:
        board2['grid'][x, y] = board2['grid'][x, 0]
        board2['grid'][x, 0] = 0
    else:
        board2['grid'][x, y] = board2['grid'][x, y + 1]
        board2['grid'][x, y + 1] = 0
    board2['moves'] += 'L '
    board2['level'] += 1
    return board2


# Swaps the tile in Down direction and also updates the corresponding move and the level of the state
def swap_down(board3, x, y):
    if x == 0:
        board3['grid'][x, y] = board3['grid'][N - 1, y]
        board3['grid'][N - 1, y] = 0
    else:
        board3['grid'][x, y] = board3['grid'][x - 1, y]
        board3['grid'][x - 1, y] = 0
    board3['moves'] += 'D '
    board3['level'] += 1
    return board3


# Swaps the tile in Up direction and also updates the corresponding move and the level of the state
def swap_up(board4, x, y):
    if x == N - 1:
        board4['grid'][x, y] = board4['grid'][0, y]
        board4['grid'][0, y] = 0
    else:
        board4['grid'][x, y] = board4['grid'][x + 1, y]
        board4['grid'][x + 1, y] = 0
    board4['moves'] += 'U '
    board4['level'] += 1
    return board4


# Creates and returns a LIST of 4 successors from a state by swapping the values of 0 with its neighbours
def successors(board):
    # return swap_pieces(board)
    index = board['grid'].keys()[board['grid'].values().index(0)]
    x = index[0]
    y = index[1]
    return [swap_right(copy.deepcopy(board), x, y), swap_left(copy.deepcopy(board), x, y),
            swap_down(copy.deepcopy(board), x, y), swap_up(copy.deepcopy(board), x, y)]


# Solves the 15-puzzle problem. Returns false if no solution present or found
def solve(initial_state):
    if not is_solution(initial_list):
        return False
    elif is_goal(initial_state):
        return initial_state
    # List for visited states
    closed = []
    # List to keep a track of states in the fringe. Used to optimize the search time of fringe
    list_fringe_track = []
    fringe = PriorityQueue()
    fringe.put((0, initial_state))
    while fringe.qsize() > 0:
        next_state = fringe.get()[1]
        closed.append(next_state['grid'])
        if next_state['grid'] in list_fringe_track:
            list_fringe_track.remove(next_state['grid'])

        if is_goal(next_state):
            return next_state

        for s in successors(next_state):
            # Discards the successor state, if its already in Closed
            if not s['grid'] in closed:
                # if not closed.__contains__(s['grid']):
                eval_func = evaluation_cost(s)
                s_infringe_flag = False
                length = fringe.qsize() - 1

                if s['grid'] in list_fringe_track:
                    # Checks & removes if the successors state is already present in the Fringe with a higher heuristic cost
                    while length > -1:
                        if fringe.queue[length][1]['grid'] == s['grid']:
                            s_infringe_flag = True
                            if fringe.queue[length][0] > eval_func:
                                fringe.get(length)
                                s_infringe_flag = False
                                list_fringe_track.remove(s['grid'])
                            break
                        length -= 1

                # If successor state not present in Fringe, adds to Fringe
                if not s_infringe_flag:
                    list_fringe_track.append(s['grid'])
                    fringe.put((eval_func, s))
    return False


# Converts the input file into a list of lists and stores in the global initial_list
def main(fname):
    global initial_list
    # "Reads text from a file, prints token and frequency."
    try:
        file = open(fname, mode='r')
        initial_list = [int(line) for line in file.read().split()]
        print "Initial List:"
        print initial_list
        initialize(initial_list)
        file.close()
    except IOError:
        print("Cannot read from file:", fname)
        return


start_time = time.time()
#file_name = "E:\Rahul\IUB Education\Fall 2016\AI (David Crandell)\Assignments\Assignment-1\Problem-2\p2_input13.txt"
file_name = sys.argv[1]
main(file_name)
print "Initial State Global:"
print initial_state_global
solution = solve(initial_state_global)
end_time = time.time()
print "Total Time:", end_time - start_time
if solution:
	print "Solution State:"
	print solution
	print "Total Moves:", solution['level']
	print "Moves:"
print solution['moves'] if solution else "Sorry, no solution found. :("
