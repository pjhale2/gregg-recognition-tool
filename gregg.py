import math
import tkinter as tk
from tkinter import *

WIDTH = 32 * 12  # width of the window
HEIGHT = 32 * 6  # height of the window
LINE_WIDTH = 5  # width of the pen
LINE_RESOLUTION = 5  # minimum length of line segment; larger means more accurate angles but rougher lines
ANGLE_THRESHOLD = 60  # minimum angle to begin a new phoneme

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
        self.current_phoneme = []
        self.current_phoneme

    # interpret the phonemes
    # TODO: use neural nets to distinguish phonemes
    def interpret(self):
        print(self.phoneme_list)

    # TODO: speak phonemes aloud
    def speak(self):
        pass

    # start a new phoneme when the mouse is pressed
    def mouse_down(self, event):
        self.current_phoneme = [(event.x, event.y)]

        # draw a dot in case the button is immediately lifted
        self.x_prev = event.x
        self.y_prev = event.y
        self.prev_dir = None
        self.canvas.create_line(event.x, event.y, event.x, event.y,
                                width=LINE_WIDTH, fill='black',
                                capstyle=ROUND, smooth=TRUE, splinesteps=36)

    # draw and record the coordinates of mouse movements
    # TODO: check for new phonemes while moving (i.e. circles, semi-circles, etc.)
    def mouse_move(self, event):
        if abs(event.x - self.x_prev) > LINE_RESOLUTION or abs(event.y - self.y_prev) > LINE_RESOLUTION:
            # create new phoneme on a sharp bend
            dir = math.atan2((self.x_prev - event.x), (self.y_prev - event.y))
            dir = 180 / math.pi * -dir
            if self.prev_dir:
                diff = dir - self.prev_dir
                if diff > 180: diff -= 360 
                if diff < -180: diff += 360
                if abs(diff) >= ANGLE_THRESHOLD:
                    # we've encountered a sharp bend; create a new phoneme
                    self.draw_phonemes()
            self.prev_dir = dir

            # draw the movement to the canvas and record it in the current phoneme
            self.current_phoneme.append((event.x, event.y))
            self.canvas.create_line(self.x_prev, self.y_prev, event.x, event.y,
                                    width=LINE_WIDTH, fill='black',
                                    capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.x_prev = event.x
            self.y_prev = event.y

    # draw the current phonemes in alternating colors
    def draw_phonemes(self, event=None):
        # add the current phoneme
        self.phoneme_list.append(self.current_phoneme)
        self.current_phoneme = self.current_phoneme[-1:]

        # draw phonemes while cycling through colors
        colors = ['navy', 'blue', 'light blue']
        color_index = 0
        for phoneme in self.phoneme_list:
            color_index = (color_index + 1) % len(colors)
            for index in range(len(phoneme)):
                x_prev = phoneme[index - 1][0] if index > 0 else phoneme[index][0]
                y_prev = phoneme[index - 1][1] if index > 0 else phoneme[index][1]
                self.canvas.create_line(x_prev, y_prev, phoneme[index][0], phoneme[index][1],
                        width=LINE_WIDTH, fill=colors[color_index],
                        capstyle=ROUND, smooth=TRUE, splinesteps=36)

# start Gregg recognition tool
if __name__ == '__main__':
    Gregg()
