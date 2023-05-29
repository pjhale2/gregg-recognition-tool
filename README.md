# Gregg Recognition Tool

This repository contains the beginnings of a tool designed to read Gregg Notehand. At the moment, it can somewhat reliably read a small subset of Notehand symbols.

### What is Gregg Notehand?

Gregg Notehand derives from Gregg shorthand, one of the more popular shorthand methods. Rather than writing words out letter by letter, Gregg users instead write symbols that represent phonemes. Furthermore, many words have short forms that can be written in just a symbol or two. In general, this means that Gregg users can write more text using less strokes, resulting in writing speeds at or above that of typical human speech. Below is a sample of Gregg shorthand.

![](/home/peter/snap/marktext/9/.config/marktext/images/2023-05-28-17-56-03-sample.png)

Gregg Notehand is a simpler form of Gregg shorthand published in 1960 and aimed at students. Notehand has fewer short forms, resulting in a slower writing speed. However, this makes it easier to learn and still results in an improved writing speed when studying and taking notes.

### How does it work?

The Gregg Recognition Tool will first prompt you to write a shorthand word. Note the grid lines on the canvas. Although you are free to train a model that recognizes your own writing size, the pretrained model best recognizes phonemes when they fit to the grid (that is, "a" takes up about one square, "r" takes up about two, and "l" takes up about three).

![](/home/peter/snap/marktext/9/.config/marktext/images/2023-05-28-18-05-59-blank.png)

From here, you can write a shorthand word on the canvas. Notice that, as you write, phonemes are automatically differentiated from each other. If you make a mistake, press "Clear" (or the "c" key) and try again. Once satisfied, you can press either "Read" to attempt to identify the phonemes, or "Speak" to identify and speak the word aloud.

![](/home/peter/snap/marktext/9/.config/marktext/images/2023-05-28-18-08-55-late.png)

If you wish to improve upon the provided model, you'll likely want to create more training data. To do this, draw a word and press "Label" (or the "l" key) to be prompted to label the first phoneme. Type your label and press "Enter" (or the enter key) to proceed to the next symbol until all phonemes have been labeled. This process saves each phoneme as a labeled training image.

![](/home/peter/snap/marktext/9/.config/marktext/images/2023-05-28-18-12-55-label.png)

Once you've collected enough data, you may run "train.py" to train a new neural network. Make sure to tune the parameters as you see fit.

### How do I run it?

Start by cloning the repository into a folder of your choice. In addition to Python 3, Tkinter and PyTorch must be installed. Optionally, you may install pyttsx3 for speaking ability. Depending on your OS, you may need to install additional packages to get this to work. Specific information can be found in the pyttsx3 README on GitHub.

### It seems incomplete...

Yes! At the moment, only a few symbols ("a", "d", "e", "f", "h", "l", "m", "n", "o", "r", "s", "t", and "v") are supported. In addition, certain grammar features (like the -ing ending) and all short forms are not supported. This stems from the fact that I've only read up through Unit 6 of the Gregg Notehand book.
