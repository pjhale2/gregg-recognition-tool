import tkinter as tk
from tkinter import *

WIDTH = 32 * 12
HEIGHT = 32 * 6
LINE_WIDTH = 5

# UI and phoneme recorder for Gregg recognition tool
class Gregg(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Gregg Recognition Tool')

        # set up buttons
        self.frame = Frame(self.window)
        self.frame.pack(side=tk.TOP, fill='x')
        self.clear_button = Button(self.frame, text='clear', command=self.clear)
        self.clear_button.pack(side='left')
        self.interpret_button = Button(self.frame, text='interpret', command=self.interpret)
        self.interpret_button.pack(side='left')
        self.speak_button = Button(self.frame, text='speak', command=self.speak)
        self.speak_button.pack(side='left')

        # set up canvas
        self.canvas = Canvas(self.window, bg='white', width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=tk.BOTTOM)
        self.clear()

        # bind left mouse button for drawing
        self.canvas.bind('<Button-1>', self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.draw_phonemes)

        # run UI loop
        self.window.mainloop()

    # clear the canvas and the current word in memory
    def clear(self):
        self.canvas.delete('all')

        # draw grid lines
        grid_step = HEIGHT / 4
        grid_base = HEIGHT / 4 / 2
        for x in range(8):
            self.canvas.create_line(grid_base + x * grid_step, 0, grid_base + x * grid_step, HEIGHT, fill='light gray')
        for y in range(4):
            self.canvas.create_line(0, grid_base + y * grid_step, WIDTH, grid_base + y * grid_step, fill='light gray')

        # clear phonemes
        self.phoneme_list = []

    # interpret the phonemes
    # TODO: use neural nets to distinguish phonemes
    def interpret(self):
        print(self.phoneme_list)

    # TODO: speak phonemes aloud
    def speak(self):
        pass

    # start a new phoneme when the mouse is pressed
    def mouse_down(self, event):
        self.phoneme_list.append('new')
        self.phoneme_list.append((event.x, event.y))

        # draw a dot in case the button is immediately lifted
        self.x_prev = event.x
        self.y_prev = event.y
        self.canvas.create_line(event.x, event.y, event.x, event.y,
                                width=LINE_WIDTH, fill='black',
                                capstyle=ROUND, smooth=TRUE, splinesteps=36)

    # draw and record the coordinates of mouse movements
    # TODO: check for new phonemes while moving (i.e. circles, semi-circles, or angles)
    def mouse_move(self, event):
        self.phoneme_list.append((event.x, event.y))
        self.canvas.create_line(self.x_prev, self.y_prev, event.x, event.y,
                                width=LINE_WIDTH, fill='black',
                                capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.x_prev = event.x
        self.y_prev = event.y

    # draw the current phonemes in alternating colors
    # TODO: make the lines connected
    def draw_phonemes(self, event=None):
        colors = ['navy', 'blue', 'light blue']
        color_index = 0
        for item in self.phoneme_list:
            if item == 'new':
                color_index = (color_index + 1) % len(colors)
            else:
                self.canvas.create_line(item[0], item[1], item[0], item[1],
                        width=LINE_WIDTH, fill=colors[color_index],
                        capstyle=ROUND, smooth=TRUE, splinesteps=36)

# start Gregg recognition tool
if __name__ == '__main__':
    Gregg()
