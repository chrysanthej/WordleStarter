# File: WordleGraphics.py

"""
This file implements the WordleGWindow class, which manages the
graphical display for the Wordle project.
"""

import atexit
import math
import time
import tkinter

# Constants

N_ROWS = 6			# Number of rows
N_COLS = 5			# Number of columns

CORRECT_COLOR = "#66BB66"       # Light green for correct letters
CORRECT_COLOR_CB = "#0000FF"    # Blue for correct letter for color blind mode
PRESENT_COLOR = "#CCBB66"       # Brownish yellow for misplaced letters
PRESENT_COLOR_CB = "#FFA500"    # Orange for misplaced letters color blind mode
MISSING_COLOR = "#999999"       # Gray for letters that don't appear
UNKNOWN_COLOR = "#FFFFFF"       # Undetermined letters are white
KEY_COLOR = "#DDDDDD"           # Keys are colored light gray

CANVAS_WIDTH = 500		# Width of the tkinter canvas (pixels)
CANVAS_HEIGHT = 750		# Height of the tkinter canvas (pixels)

SQUARE_SIZE = 60		# Size of each square (pixels)
SQUARE_SEP = 5                  # Separation between squares (pixels)
TOP_MARGIN = 100    		# Top margin (pixels)
BOTTOM_MARGIN = 30    		# Bottom margin (pixels)
MESSAGE_SEP = 20                # Space between board and message center

SQUARE_FONT = ("Helvetica Neue", -44, "bold")
MESSAGE_FONT = ("Helvetica Neue", -20, "bold")
KEY_FONT = ("Helvetica Neue", -18)
ENTER_FONT = ("Helvetica Neue", -14)

KEY_WIDTH = 40
KEY_HEIGHT = 60
KEY_CORNER = 9
KEY_XSEP = 5
KEY_YSEP = 7

KEY_LABELS = [
    [ "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P" ],
    [ "A", "S", "D", "F", "G", "H", "J", "K", "L" ],
    [ "ENTER", "Z", "X", "C", "V", "B", "N", "M", "DELETE" ]
]

CLICK_MAX_DISTANCE = 2
CLICK_MAX_DELAY = 0.5

# Derived constants

SQUARE_DELTA = SQUARE_SIZE + SQUARE_SEP
BOARD_WIDTH = N_COLS * SQUARE_SIZE + (N_COLS - 1) * SQUARE_SEP
BOARD_HEIGHT = N_ROWS * SQUARE_SIZE + (N_ROWS - 1) * SQUARE_SEP
MESSAGE_X = CANVAS_WIDTH / 2
MESSAGE_Y = TOP_MARGIN + BOARD_HEIGHT + MESSAGE_SEP

BUTTON_WIDTH = 125
BUTTON_HEIGHT = 60

class WordleGWindow:
    """This class creates the Wordle window."""

    def __init__(self):
        """Creates the Wordle window."""

        def create_grid():
            return [
                [
                    WordleSquare(canvas, i, j) for j in range(N_COLS)
                ] for i in range(N_ROWS)
            ]

        def create_keyboard():
            keys = { }
            nk = len(KEY_LABELS[0])
            h = KEY_HEIGHT
            y0 = CANVAS_HEIGHT - BOTTOM_MARGIN - 3 * KEY_HEIGHT - 2 * KEY_YSEP
            for row in range(len(KEY_LABELS)):
                y = y0 + row * (KEY_HEIGHT + KEY_YSEP)
                x = (CANVAS_WIDTH - nk * KEY_WIDTH - (nk - 1) * KEY_XSEP) / 2
                if row == 1:
                    x += (KEY_WIDTH + KEY_XSEP) / 2
                for col in range(len(KEY_LABELS[row])):
                    label = KEY_LABELS[row][col]
                    w = KEY_WIDTH
                    if len(label) > 1:
                        w += (KEY_WIDTH + KEY_XSEP) / 2
                    keys[label] = WordleKey(self._canvas, x, y, w, h, label)
                    x += w + KEY_XSEP
            return keys
        
        def create_colorblind_button():
            return WordleButton(self._canvas)

        def create_message():
            return WordleMessage(self._canvas,
                                 CANVAS_WIDTH / 2,
                                 MESSAGE_Y)


        def key_action(tke):
            print(tke)

            if isinstance(tke, str):
                ch = tke.upper()
            
            elif hasattr(tke, 'keysym'):
                ch = tke.keysym.upper()

            else:
                ch = tke.char.upper()

            if ch == "DELETE" or ch == "\x08" or ch == "BACKSPACE":
                self.show_message("")
                print("backspace")
                if self._row < N_ROWS and self._col > 0:
                    self._col -= 1
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(" ")
            elif ch == "\r" or ch == "\n"  or ch == "RETURN" or ch == "ENTER":
                self.show_message("")
                s = ""
                for col in range(N_COLS):
                    s += self._grid[self._row][col].get_letter()
                for fn in self._enter_listeners:
                    fn(s)
            elif ch.isalpha():
                self.show_message("")
                print("is aplha pressed")
                if self._row < N_ROWS and self._col < N_COLS:
                    sq = self._grid[self._row][self._col]
                    sq.set_letter(ch)
                    self._col += 1

        def press_action(tke):
            self._down_x = tke.x
            self._down_y = tke.y
            self._down_time = time.time()

        def release_action(tke):
            if abs(self._down_x - tke.x) <= CLICK_MAX_DISTANCE:
                if abs(self._down_y - tke.y) <= CLICK_MAX_DISTANCE:
                    t = time.time()
                    if t - self._down_time < CLICK_MAX_DELAY:
                        key = find_key(tke.x, tke.y)
                        if key:
                            key_action(key._label)

        def find_key(x, y):
            for key in self._keys.values():
                kx, ky, kw, kh = key._bounds
                if x >= kx and x <= kx + kw and y >= ky and y <= ky + kh:
                    return key
            return None
        
        def button_clicked(event):
            print("button was clicked")

        def delete_window():
            """Closes the window and exits from the event loop."""
            root.destroy()

        def start_event_loop():
            """Starts the tkinter event loop when the program exits."""
            root.mainloop()

        root = tkinter.Tk()
        root.title("Wordle")
        root.protocol("WM_DELETE_WINDOW", delete_window)
        self._root = root
        canvas = tkinter.Canvas(root,
                                bg="White",
                                width=CANVAS_WIDTH,
                                height=CANVAS_HEIGHT,
                                highlightthickness=0)
        canvas.pack()
        self._canvas = canvas
        self._grid = create_grid()
        self._message = create_message()
        self._keys = create_keyboard()
        self._button = WordleButton(self._canvas, self.toggle_colorblind, self)
        self._enter_listeners = [ ]
        root.bind("<Key>", key_action)
        root.bind("<ButtonPress-1>", press_action)
        root.bind("<ButtonRelease-1>", release_action)
        self._row = 0
        self._col = 0
        self._is_colorblind = False # Initializes the colorblind state
        atexit.register(start_event_loop)

    def get_square_letter(self, row, col):
        return self._grid[row][col].get_letter()

    def set_square_letter(self, row, col, ch):
        self._grid[row][col].set_letter(ch)

    def get_square_color(self, row, col):
        return self._grid[row][col].get_color()

    def set_square_color(self, row, col, color):
        self._grid[row][col].set_color(color)

    def get_key_color(self, ch):
        return self._keys[ch].get_color()

    def set_key_color(self, ch, color):
        self._keys[ch].set_color(color)

    def get_current_row(self):
        return self._row

    def set_current_row(self, row):
        self._row = row
        self._col = 0
        for col in range(N_COLS):
            self.set_square_letter(row, col, " ")
            self.set_square_color(row, col, UNKNOWN_COLOR)

    def add_enter_listener(self, fn):
        self._enter_listeners.append(fn)

    def show_message(self, msg, color="Black"):
        self._message.set_text(msg, color)
    
    def toggle_colorblind(self):
        self._is_colorblind = not self._is_colorblind
        print(self._is_colorblind)
        self.update_colors()

    def update_colors(self):
        for row in range(N_ROWS):
            for col in range(N_COLS):
                current_color = self.get_square_color(row, col)
                updated_color = self.get_updated_color(current_color)
                self.set_square_color(row, col, updated_color)

    def get_updated_color(self, color):
        if self._is_colorblind:
            # Return color for colorblind mode
            if color == CORRECT_COLOR:
                return CORRECT_COLOR_CB
            elif color == PRESENT_COLOR:
                return PRESENT_COLOR_CB
            else:
                return color  # Keep other colors unchanged in colorblind mode
        else:
            # Return color for regular mode
            if color == CORRECT_COLOR_CB:
                return CORRECT_COLOR
            elif color == PRESENT_COLOR_CB:
                return PRESENT_COLOR
            return color

class WordleSquare:

    def __init__(self, canvas, row, col):
        x0 = (CANVAS_WIDTH - BOARD_WIDTH) / 2 + col * SQUARE_DELTA
        y0 = TOP_MARGIN + row * SQUARE_DELTA
        x1 = x0 + SQUARE_SIZE
        y1 = y0 + SQUARE_SIZE
        self._canvas = canvas
        self._ch = " "
        self._color = UNKNOWN_COLOR;
        self._frame = canvas.create_rectangle(x0, y0, x1, y1)
        self._text = canvas.create_text(x0 + SQUARE_SIZE / 2,
                                        y0 + SQUARE_SIZE / 2,
                                        text=self._ch,
                                        font=SQUARE_FONT)

    def get_letter(self):
        return self._ch

    def set_letter(self, ch):
        self._ch = ch
        self._canvas.itemconfigure(self._text, text=ch)

    def get_color(self):
        return self._color

    def set_color(self, color):
        color = color.upper()
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleKey:

    def __init__(self, canvas, x, y, width, height, label):
        self._canvas = canvas
        self._label = label
        self._bounds = [ x, y, width, height ]
        self._color = UNKNOWN_COLOR
        font = KEY_FONT
        if label == "ENTER":
            font = ENTER_FONT
        if label == "DELETE":
            label = "\u232B"
        points = [ x + KEY_CORNER, y,
                   x + KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width - KEY_CORNER, y,
                   x + width, y,
                   x + width, y + KEY_CORNER,
                   x + width, y + KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height - KEY_CORNER,
                   x + width, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + width - KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x + KEY_CORNER, y + height,
                   x, y + height,
                   x, y + height - KEY_CORNER,
                   x, y + height - KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y + KEY_CORNER,
                   x, y]
        self._frame = canvas.create_polygon(points,
                                            fill=KEY_COLOR,
                                            outline=KEY_COLOR,
                                            smooth=True)
        self._text = canvas.create_text(x + width / 2,
                                        y + height / 2,
                                        text=label,
                                        font=font)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        fg = "White"
        if color == UNKNOWN_COLOR:
            fg = "Black"
        self._canvas.itemconfig(self._frame, fill=color)
        self._canvas.itemconfig(self._text, fill=fg)


class WordleMessage:

    def __init__(self, canvas, x, y):
        self._canvas = canvas
        self._text = ""
        self._msg = canvas.create_text(x, y,
                                       text="",
                                       font=MESSAGE_FONT,
                                       anchor=tkinter.CENTER)

    def get_text(self):
        return self._text

    def set_text(self, text, color="Black"):
        self._text = text
        self._canvas.itemconfigure(self._msg, text=text, fill=color)

class WordleButton:

    def __init__(self, canvas, toggle_method, window):
        x0 = CANVAS_WIDTH - BUTTON_WIDTH - 15
        y0 = 15
        x1 = x0 + BUTTON_WIDTH
        y1 = y0 + BUTTON_HEIGHT
        self._canvas = canvas
        self._wordle_window = window
        self._text = ""
        self._toggle_method = toggle_method
        self._button = canvas.create_rectangle(x0, y0, x1, y1, tags="toggle_button")
        self._text = canvas.create_text(x0 + BUTTON_WIDTH / 2,
                                        y0 + BUTTON_HEIGHT / 2,
                                        text="Colorblind Mode",
                                        tags="toggle_button")
        self._canvas.itemconfig(self._button, fill=KEY_COLOR)
        self._canvas.tag_bind("toggle_button", "<Button-1>", self.toggle_button_clicked)
        print("button initialized")

    def toggle_button_clicked(self, event):
        print("inner toggle_button_clicked method called")
        self._toggle_method()
        self._wordle_window.update_colors()
