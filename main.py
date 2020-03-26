from board import Board
import time
from math import floor
import threading
from copy import deepcopy
from queue import Queue

R_C = 20
W_H = 20
playing = False
field_q = Queue()

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
    global board, field_q
    
    field = deepcopy(board.field)
    if not field_q.empty():
        field_q = Queue()

    while playing:
        #print("New Frame")
        new_field = deepcopy(field)
        for i in range(R_C):
            for j in range(R_C):

                n = get_neighbours(i, j)
                alive = n.count(1)
                cell = field[i][j]
                if cell == 1: # cell is alive
                    if alive < 2 or alive > 3:
                        new_field[i][j] = 0
                        break
                elif cell == 0: # cell is dead
                    if alive == 3:
                        new_field[i][j] = 1
                        break
        field = new_field
        field_q.put(new_field)
        time.sleep(0.5)
        

def all_dead():
    global board
    for i in range(R_C):
        for j in range(R_C): 
            if board.field[i][j] == 1:
                return False
    return True

def play_game(event=None):
    global playing, t, field_q

    if playing == False:
        print("Starting Game")
        playing = True
        t = threading.Thread(target=game_thread, args =(lambda : playing, ))
        t.daemon = True
        t.start()
        while playing:
            if not field_q.empty():
                board.field = field_q.get()
                board.draw()
                board.platform.update()
                #print("Draw new Frame")
            if all_dead():
                playing = False
                board.draw()
                board.platform.update()
                print("All cells dead")
                return
            time.sleep(0.01)
    else:
        print("Stoping game")
        playing = False

def set_start(event):
    global board, playing, field_q
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
