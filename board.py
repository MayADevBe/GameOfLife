import tkinter as tk

class Board:
    '''Creates GUI Board'''

    def __init__(self, title, width, r_c):
        self.window = tk.Tk()
        self.window.title(title)
        self.width = width
        self.r_c = r_c
        self.field = []
        self.platform = tk.Canvas(self.window, width = r_c*width, height = r_c*width)
        self.platform.pack()

    def draw(self):
        if self.field == []:
            self.create_field()

        #draw field 
        for i in range(self.r_c):
            for j in range(self.r_c):
                if self.field[i][j] == 0:
                    self.platform.create_rectangle(i*self.width, j*self.width, (i+1)*self.width, (j+1)*self.width, fill="white")
                else:
                    self.platform.create_rectangle(i*self.width, j*self.width, (i+1)*self.width, (j+1)*self.width, fill="black")       

    def create_field(self):
        for i in range(self.r_c):
            self.field.append([])
            for j in range(self.r_c):
                self.field[i].append(0)

    def start(self):
        self.window.mainloop()