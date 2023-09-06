from xml.dom import minidom

import cairo
import math
import random
import re

LETTER_SPACING = 12
RANDOMNESS_SCALE = 0 # 1.6
LINE_WIDTH = 0.8
MIN_LINE_WIDTH = 0.4
MAX_LINE_WIDTH = 1
LETTER_HEIGHT = 14

LETTER_WIDTHS = {'a':10, 
                 'b':7, 
                 'c':11, 
                 'd':7, 
                 'e':9.5, 
                 'f':6, 
                 'g':7, 
                 'h':7, 
                 'i':3,
                 'j':2, 
                 'k':5.5, 
                 'l':3, 
                 'm':10, 
                 'n':7, 
                 'o':8, 
                 'p':10, 
                 'q':8, 
                 'r':10, 
                 's':7, 
                 't':6, 
                 'u':8, 
                 'v':8, 
                 'w':8, 
                 'x':10, 
                 'y':7, 
                 'z':9,
                 'A':10,
                 'B':10,
                 'C':11,
                 'D':10,
                 'E':9,
                 'F':9,
                 'G':12,
                 'H':8,
                 'I':2,
                 'J':9,
                 'K':9,
                 'L':8.5,
                 'M':9,
                 'N':8,
                 'O':12,
                 'P':8,
                 'Q':11,
                 'R':8,
                 'S':10,
                 'T':9,
                 'U':12,
                 'V':10,
                 'W':12,
                 'X':13,
                 'Y':8,
                 'Z':14}
CAPITAL_LETTER_WIDTHS = []

class TypeWriter:
    def __init__(self, ctx, START_X, START_Y, X_LIMIT, LINE_HEIGHT):
        self.ctx = ctx
        self.START_X = START_X
        self.x = START_X
        self.y = START_Y
        self.X_LIMIT = X_LIMIT
        self.LINE_HEIGHT = LINE_HEIGHT

        self.ctx.set_line_width(LINE_WIDTH)
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self.ctx.move_to(START_X, START_Y)

    def random(self):
        return (random.random()-0.5)*RANDOMNESS_SCALE
    
    def small_random(self):
        return self.random()/10

    def line(self, dx, dy):
        self.ctx.line_to(self.x+dx+self.random(), self.y+dy+self.random())
        self.ctx.stroke()

        self.update_stroke()

    def arc(self, init_x, init_y, x1, y1, x2, y2, xf, yf):
        self.ctx.curve_to(init_x+x1+self.random(), init_y+y1+self.random(), init_x+x2+self.random(), init_y+y2+self.random(), init_x+xf, init_y+yf)
        self.ctx.stroke()

        self.update_stroke()

    # Takes care of flipping the y-axis by subtracting LETTER_HEIGHT on its own. Just pass whatever coords come from the svg file now.
    def new_arc(self, init_x, init_y, x1, y1, x2, y2, xf, yf):
        self.ctx.curve_to(init_x+x1+self.random(), -LETTER_HEIGHT+init_y+y1+self.random(), init_x+x2+self.random(), -LETTER_HEIGHT+init_y+y2+self.random(), init_x+xf, -LETTER_HEIGHT+init_y+yf)
        self.ctx.stroke()

        self.update_stroke()

    def execute(self, init_x, init_y, s):
        tokens = re.split(' |,', s)
        tokens.pop(0)
        tokens.pop(2)
        tokens = [float(x) for x in tokens]
        self.move_to_relative(init_x, init_y, tokens[0], tokens[1])
        self.new_arc(init_x, init_y, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])

    def execute2(self, init_x, init_y, s):
        tokens = re.split(' |,', s)
        tokens.pop(0)
        tokens.pop(2)
        tokens = [float(x) for x in tokens]
        self.move_to_relative(init_x, init_y, tokens[0], tokens[1])
        self.new_arc_without_stroke(init_x, init_y, tokens[2], tokens[3], tokens[4], tokens[5], tokens[6], tokens[7])
        self.new_arc_without_stroke(init_x, init_y, tokens[8], tokens[9], tokens[10], tokens[11], tokens[12], tokens[13])

        self.ctx.stroke()
        self.update_stroke()
    
    def new_arc_without_stroke(self, init_x, init_y, x1, y1, x2, y2, xf, yf):
        self.ctx.curve_to(init_x+x1+self.random(), -LETTER_HEIGHT+init_y+y1+self.random(), init_x+x2+self.random(), -LETTER_HEIGHT+init_y+y2+self.random(), init_x+xf, -LETTER_HEIGHT+init_y+yf)

    def update_stroke(self):
        new_stroke = self.ctx.get_line_width() + self.small_random()*2
        while new_stroke < MIN_LINE_WIDTH or new_stroke > MAX_LINE_WIDTH:
            new_stroke = self.ctx.get_line_width() + self.small_random()*2
        self.ctx.set_line_width(new_stroke)

    def move_by(self, dx, dy):
        self.x += dx + self.random()
        self.y += dy + self.random()
        self.update_point()

    # Moves to coords relative to init_x and init_y. Also flips y so you don't have to care about -14
    def move_to_relative(self, init_x, init_y, x, y):
        self.x = init_x+x+self.random()
        self.y = init_y+(-LETTER_HEIGHT+y)+self.random()
        self.update_point()

    def update_point(self):
        self.ctx.move_to(self.x, self.y)

    def type(self, string):
        for ch in string:
            if ch == '\n':
                self.x = self.START_X
                self.y += self.LINE_HEIGHT
                self.ctx.move_to(self.x, self.y)
                continue
            if ch == ' ':
                self.x += LETTER_SPACING + self.random()*3

            try:
                if ch >= 'A' and ch <= 'Z':
                    doc = minidom.parse(f'letters/{ch}2.svg')  # parseString also exists
                else:
                    doc = minidom.parse(f'letters/{ch}.svg')  # parseString also exists
            except:
                print(f"Letter {ch} file not found")
            
            
            path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
            doc.unlink()

            init_x, init_y = self.x, self.y
            for path in path_strings:
                if len(re.split(' |,', path)) >= 12:
                    self.execute2(init_x, init_y, path)
                else:
                    self.execute(init_x, init_y, path)
            self.x = init_x
            self.y = init_y

            if ch != ' ':
                try:
                    self.x += LETTER_WIDTHS[ch] + self.random()*3
                except:
                    pass
            if self.x > self.X_LIMIT:
                self.x = self.START_X
                self.y += self.LINE_HEIGHT

            self.ctx.move_to(self.x, self.y)
            self.prev_char = ch
