# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
from copy import deepcopy

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#

def get_wells(board):
    prev_r = 20
    for r in range(0, len(board), 1):
        if board[r][0] == "x":
            prev_r = r
            break
    wells = 0
    for c in range(1,len(board[0])):
        for r in range( 0,len(board), 1):
            if board[r][c] == "x":
                wells += abs(r-prev_r)
                prev_r = r
                break
        if r == len(board)-1:
            wells += abs(20 - prev_r)
            prev_r = 20

    return wells

def get_holes(board):
    holes = 0
    flag = False
    for c in range(0,len(board[0])):
        for r in range( 0,len(board), 1):
            if board[r][c] == "x":
                flag = True
                continue
            if flag == True:
                holes+=1
        flag = False
    #print "holes=",holes
    #raw_input()
    return holes

def get_aggheight(board):
    height = [19]
    for c in range(0,len(board[0])):
        for r in range( 0,len(board), 1):
            if board[r][c] == "x":
                height.append(r)
                break
    return min(height)

def get_status(board):
    s=[]
    s.append(get_aggheight(board[0]))
    s.append(board[1])
    s.append(get_holes(board[0]))
    s.append(get_wells(board[0]))

    return s
def evaluate(board,piece,r,c,next_piece,depth):
    score = 0.0

    current = get_status(board)
    tempboard = TetrisGame.place_piece(board, piece, r, c)
    tempboard = TetrisGame.remove_complete_lines(tempboard)
    future = get_status(tempboard)

    #print  future[3]
    score += 0.3*future[0]
    score += 0.8*(future[1]-current[1])
    score -=0.5*(future[2]-current[2])
    score -= 0.1*(future[3]-current[3])

    if depth ==1:
        return score
    else:
        rotations = [TetrisGame.rotate_piece(next_piece, i) for i in range(0, 360, 90)]
        for i in rotations:
            k = deepcopy(rotations)
            k.remove(i)
            if i in k:
                rotations.remove(i)
        # print rotations
        i = 0
        h = [0]
        for piece in rotations:
            for c in range(0, len(board[0])):
                r = 0
                while not TetrisGame.check_collision(tempboard, piece, r + 1, c):
                    r += 1
                if r == 0:
                    continue
                h.append(evaluate(tempboard, piece, r, c, piece, depth-1))

        score += max(h)
        return score
def find_best(board,piece,current_score,next_piece):
    min_state = 0
    column_heights = [min([r for r in range(len(board) - 1, 0, -1) if board[r][c] == "x"] + [100, ]) for c in
                      range(0, len(board[0]))]
    min_col = column_heights.index(max(column_heights))
    rotations = [TetrisGame.rotate_piece(piece[0], i) for i in range(0, 360, 90)]

    for i in rotations:
        k = deepcopy(rotations)
        k.remove(i)
        if i in k:
            rotations.remove(i)

    options = {i: [0, min_col] for i in range(0, len(rotations))}
    i = 0
    for piece in rotations:
        for c in range(0, len(board[0])):
            r = 0
            while not TetrisGame.check_collision((board, current_score), piece, r + 1, c):
                r += 1
            if r == 0:
                continue

            h = evaluate((board, current_score),piece,r,c,next_piece,2)
            if h > min_state:
                options[i] = [h, c]
                min_state = h
        i += 1
        offset = max(options, key=lambda k: options[k][0])
    return [offset,options[offset][1]]

def find_best_animated(board,piece,current_score,next_piece):
    min_state = 0
    column_heights = [min([r for r in range(len(board) - 1, 0, -1) if board[r][c] == "x"] + [100, ]) for c in
                      range(0, len(board[0]))]
    min_col = column_heights.index(max(column_heights))
    rotations = [TetrisGame.rotate_piece(piece[0], i) for i in range(0, 360, 90)]

    for i in rotations:
        k = deepcopy(rotations)
        k.remove(i)
        if i in k:
            rotations.remove(i)

    options = {i: [0, min_col] for i in range(0, len(rotations))}
    i = 0
    for piece in rotations:
        for c in range(0, len(board[0])):
            for r in range(min(column_heights),len(board)):
                # r = min(column_heights)
                if not TetrisGame.check_collision((board, current_score), piece, r, c):
            #     r += 1
            # if r == 0:
            #     continue

                    h = evaluate((board, current_score),piece,r,c,next_piece,2)
                    if h > min_state:
                        options[i] = [h, c]
                        min_state = h
        i += 1
        offset = max(options, key=lambda k: options[k][0])
    return [offset,options[offset][1]]

class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        input_string = ""

        board = tetris.get_board()
        piece = tetris.get_piece()
        score = tetris.get_score()

        option = find_best_animated(board,piece,score,tetris.get_next_piece())

        for k in range(0,option[0]):
            input_string += 'n'
        index = option[1]
        column = tetris.col
        while index != column:
            if (index < column):
                column-=1
                input_string+='b'
            elif (index > column):
                column += 1
                input_string += 'm'
        return input_string
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):

        while 1:
            # time.sleep(0.1)
            board = tetris.get_board()
            piece = tetris.get_piece()
            score = tetris.get_score()

            option = find_best(board, piece, score, tetris.get_next_piece())
            # print "find best called"
            


            for k in range(0, option[0]):
                tetris.rotate()
            index = option[1]
            column = tetris.col
            #while index != column:
            if (index < column):
                tetris.left()
            elif (index > tetris.col):
                tetris.right()
            else:
                tetris.down()
        # another super simple algorithm: just move piece to the least-full column
        
        # while 1:
        #     time.sleep(0.1)
        #     board = tetris.get_board()
        #     column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
        #     index = column_heights.index(max(column_heights))
        #     if(index < tetris.col):
        #         tetris.left()
        #     elif(index > tetris.col):
        #         tetris.right()
        #     else:
        #         tetris.down()
        




###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s

