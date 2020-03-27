from board import Board
import time
from math import floor
import random
from copy import deepcopy
from queue import Queue

R_C = 20
W_H = 20
playing = False

def cycle_neighbours(i):
    if i >= R_C:
        return 0
    elif i < 0:
        return R_C-1
    else:
        return i

def get_neighbours(i, j):
    global board
    neighbours = [[i+1, j], [i-1, j], [i, j+1], [i, j-1], [i+1, j+1], [i-1, j+1], [i+1, j-1], [i-1, j-1]]
    cn = []
    #cycle 
    for coordinates in neighbours:
        coordinates = list(map(cycle_neighbours, coordinates)) # map on list
        cn.append(coordinates)

    values = []
    for coord in cn:
        values.append(board.field[coord[0]][coord[1]]) 
    return values

def next_frame():
    global board

    new_field = deepcopy(board.field)
    for i in range(R_C):
        for j in range(R_C):

            cell = board.field[i][j]
            n = get_neighbours(i, j)
            alive = n.count(1)

            #Rules
            if cell == 1: # cell is alive
                if alive < 2 or alive > 3:
                    new_field[i][j] = 0
                else:
                    new_field[i][j] = 1
            elif cell == 0: # cell is dead
                if alive == 3:
                    new_field[i][j] = 1
                else:
                    new_field[i][j] = 0

    board.field = new_field

def random_seed():
    global R_C, board

    p = 0.25 #[0, 1] 0 = no cells alive, 1 = all cells alive 

    for i in range(R_C):
        for j in range(R_C):
            if random.random() <= p:
                board.field[i][j] = 1

    board.draw()
    board.platform.update()
    time.sleep(0.1)

def all_dead():
    global board
    for i in range(R_C):
        for j in range(R_C): 
            if board.field[i][j] == 1:
                return False
    return True

def play_game(event=None):
    global playing
    if playing == False:
        if all_dead():
            print("Random Seed")
            random_seed()
        print("Starting Game")
        playing = True
        while playing:
            next_frame()
            board.draw()
            board.platform.update()
            time.sleep(0.1)
            if all_dead():
                playing = False
                board.draw()
                board.platform.update()
                print("All cells dead")
                return
    else:
        print("Stoping game")
        playing = False

def set_start(event):
    global board, playing
    if not playing:
        x = floor(event.x/W_H)
        y = floor(event.y/W_H)
        if board.field[x][y] == 0:
            board.field[x][y] = 1
        else:
            board.field[x][y] = 0
        board.draw()
        board.platform.update()

board = Board("Game Of Life", W_H, R_C)
board.draw()
board.platform.bind("<Button-1>", set_start)
board.platform.bind("<Return>", play_game)
board.platform.focus_set()

board.start()