from board import Board
import time
from math import floor
import threading
from copy import deepcopy

R_C = 30
W_H = 10
playing = False

def cycle_neighbours(i):
    if i >= R_C:
        return 0
    elif i < 0:
        return R_C -1
    else:
        return i

def get_neighbours(i, j):
    global board
    neighbours = [[i+1, j], [i-1, j], [i, j+1], [i, j-1], [i+1, j+1], [i-1, j+1], [i+1, j-1], [i-1, j+1]]
    cn= []
    #cycle 
    for coordinates in neighbours:
        cc = list(map(cycle_neighbours, coordinates)) # map on list
        cn.append(cc)
    values = []
    for coordinates in cn:
        values.append(board.field[coordinates[0]][coordinates[1]]) 
    return values

def game_thread(playing):
    global board
    while True:
        print("New Frame")
        new_field = deepcopy(board.field)
        for i in range(R_C):
            for j in range(R_C):

                if not playing():
                    print("Stop Thread")
                    return

                n = get_neighbours(i, j)
                alive = n.count(1)
                cell = board.field[i][j]
                if cell == 1: # cell is alive
                    if alive < 2 or alive > 3:
                        new_field[i][j] = 0
                        break
                elif cell == 0: # cell is dead
                    if alive == 3:
                        new_field[i][j] = 1
                        break

        board.field = new_field
        time.sleep(1)

def all_dead():
    global board
    for i in range(R_C):
        for j in range(R_C): 
            if board.field[i][j] == 1:
                return False
    return True

def play_game(event=None):
    global playing, t

    if playing == False:
        print("Starting Game")
        playing = True
        t = threading.Thread(target=game_thread, args =(lambda : playing, ))
        t.daemon = True
        t.start()
        while playing:   
            board.draw()
            board.platform.update()
            if all_dead():
                playing = False
                board.draw()
                board.platform.update()
                return
            print("Draw new Frame")
            time.sleep(0.01)
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
        time.sleep(0.01)
        board.platform.update()

board = Board("Game Of Life", W_H, R_C)
board.draw()
board.platform.bind("<Button-1>", set_start)
board.platform.bind("<Return>", play_game)
board.platform.focus_set()
board.start()
