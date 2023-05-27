import os
import math
import PIL.Image
import PIL.ImageDraw
import time
import tkinter as tk
from tkinter import *
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from train import SoftmaxModel

WIDTH = 32 * 12  # width of the window
HEIGHT = 32 * 6  # height of the window

LINE_WIDTH = 5  # width of the pen
LINE_RESOLUTION = 5  # minimum length of line segment; larger means more accurate angles but rougher lines

ANGLE_THRESHOLD = 70  # minimum angle to begin a new phoneme
LOOP_THRESHOLD = 2  # moving the pen this close to a coordinate already in the phoneme counts as creating a loop
LOOP_LENGTH = 3  # minimum unwound length of a loop (in LINE_RESOLUTIONs)

DATA_PATH = './data/'  # default data directory
DATA_WIDTH = 128  # width of saved training data
DATA_HEIGHT = 128  # height of saved training data

DEVICE = "cpu"  # device on which to run the net

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
        self.train_button = Button(self.frame, text='train', command=self.label_word)
        self.train_button.pack(side='left')

        # set up canvas
        self.canvas = Canvas(self.window, bg='white', width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=tk.BOTTOM)
        self.clear()

        # bind left mouse button for drawing
        self.canvas.bind('<Button-1>', self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.add_current_phoneme)

        # bind 't' key to train button
        self.window.bind('t', self.label_word)

        # get the net
        self.net = torch.load('./net.pkl')
        self.net.eval()

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
        images = [transforms.ToTensor()(image).unsqueeze_(0) for image in self.get_images()]
        outputs = [self.net(image) for image in images]
        predictions = [torch.max(output, 1) for output in outputs]
        print(outputs)
        print(predictions)

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
        self.since_loop = 0
        self.loop_in_phoneme = False
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
                    self.add_current_phoneme()
            self.prev_dir = dir

            # check if we're in a loop (i.e. we see a pixel we've already written to the current phoneme)
            self.since_loop += 1
            if len(self.current_phoneme) > LOOP_LENGTH:
                for index in range(len(self.current_phoneme) - LOOP_LENGTH):
                    if (abs(event.x - self.current_phoneme[index][0]) <= LOOP_THRESHOLD 
                            and abs(event.y - self.current_phoneme[index][1]) <= LOOP_THRESHOLD
                            and self.since_loop > LOOP_LENGTH):
                        self.since_loop = 0
                        self.loop_in_phoneme = True
                        
                        # splice the current phoneme into two
                        if index > LOOP_THRESHOLD:
                            self.phoneme_list.append(self.current_phoneme[0:index + 1])
                        self.current_phoneme = self.current_phoneme[index:]
                        self.add_current_phoneme()
                        self.current_phoneme = []
                        return

            # draw the movement to the canvas and record it in the current phoneme
            self.current_phoneme.append((event.x, event.y))
            self.canvas.create_line(self.x_prev, self.y_prev, event.x, event.y,
                                    width=LINE_WIDTH, fill='black',
                                    capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.x_prev = event.x
            self.y_prev = event.y

    # add the current phoneme to the phoneme list
    def add_current_phoneme(self, event=None):
        if self.current_phoneme and (not self.loop_in_phoneme or len(self.current_phoneme) > LOOP_THRESHOLD):
            self.phoneme_list.append(self.current_phoneme)
            self.current_phoneme = self.current_phoneme[-1:]
        self.draw_phonemes()

    # draw the current phonemes in alternating colors
    def draw_phonemes(self):
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
                
    # create a popup window to enter training labels
    def open_label_enter(self, label_num):
        self.label_window = Toplevel(self.window)
        directions_label = Label(self.label_window, text=f'Label for phoneme {label_num}:')
        directions_label.pack(side='top')
        self.label_entry = Entry(self.label_window)
        self.label_entry.pack(side='top', fill='x')
        self.label_entry.focus_set()
        self.label_entry.bind('<Return>', lambda event, label_window=self.label_window: self.close_label_enter(label_window))
        enter_button = Button(self.label_window, text="Enter", command=lambda:self.close_label_enter(self.label_window))
        enter_button.pack(side='bottom')

    # close the label entry popup window
    def close_label_enter(self, window, event=None):
        self.label = self.label_entry.get()
        window.destroy()

    # subtract two tuples
    def sub_tuples(self, a, b):
        return (a[0] - b[0], a[1] - b[1])
    
    # get the phoneme images for the current word
    def get_images(self):
        images = []

        for index in range(len(self.phoneme_list)):
            # get the position of the phoneme
            phoneme_x = min(coords[0] for coords in self.phoneme_list[index])
            phoneme_y = min(coords[1] for coords in self.phoneme_list[index])
            phoneme_coords = (phoneme_x, phoneme_y)

            # construct an image of the phoneme
            phoneme_image = PIL.Image.new('RGB', (DATA_WIDTH, DATA_HEIGHT), color='white')
            phoneme_draw = PIL.ImageDraw.Draw(phoneme_image)
            first_coords = self.sub_tuples(self.phoneme_list[index][0], phoneme_coords)
            if len(self.phoneme_list[index]) == 1:
                phoneme_draw.ellipse([first_coords, (first_coords[0] + LINE_WIDTH, first_coords[1] + LINE_WIDTH)], fill='black', width=LINE_WIDTH)
            phoneme_draw.line([self.sub_tuples(coords, phoneme_coords) for coords in self.phoneme_list[index]], fill='black', width=LINE_WIDTH, joint='curve')
            images.append(phoneme_image)

        return images

    # prompt the user to enter label data for each phoneme in a word
    def label_word(self, event=None):
        images = self.get_images()
        for index in len(images):
            # prompt the user for a label
            self.open_label_enter(index + 1)
            self.window.wait_window(self.label_window)

            # make sure the directory for the label exists
            if not os.path.exists(DATA_PATH + self.label):
                os.makedirs(DATA_PATH + self.label)

            # store the image in the  in the directory
            filename = str(time.time()) + '.jpg'
            images[index].save(DATA_PATH + self.label + '/' + filename)
            print(f'saved {filename}')

        self.clear()

# start Gregg recognition tool
if __name__ == '__main__':
    Gregg()
