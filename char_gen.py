from xml.dom import minidom

import cairo
import math
import random
import re

LETTER_SPACING = 12
RANDOMNESS_SCALE = 2
LINE_WIDTH = 0.8
MIN_LINE_WIDTH = 0.6
MAX_LINE_WIDTH = 0.9
LETTER_HEIGHT = 14
AVG_LETTER_WIDTH = 11

LETTER_WIDTHS = {'a':9, 
                 'b':6, 
                 'c':10, 
                 'd':6, 
                 'e':8.5, 
                 'f':5, 
                 'g':6, 
                 'h':6, 
                 'i':2,
                 'j':1, 
                 'k':4.5, 
                 'l':2, 
                 'm':9, 
                 'n':6, 
                 'o':7, 
                 'p':9, 
                 'q':7, 
                 'r':9, 
                 's':6, 
                 't':5, 
                 'u':7, 
                 'v':7, 
                 'w':7, 
                 'x':9, 
                 'y':6, 
                 'z':8,
                 'A':9,
                 'B':9,
                 'C':10,
                 'D':9,
                 'E':8,
                 'F':8,
                 'G':11,
                 'H':7,
                 'I':1,
                 'J':8,
                 'K':8,
                 'L':7.5,
                 'M':8,
                 'N':7,
                 'O':11,
                 'P':7,
                 'Q':10,
                 'R':7,
                 'S':9,
                 'T':8,
                 'U':11,
                 'V':9,
                 'W':11,
                 'X':12,
                 'Y':7,
                 'Z':13,
                 '0':9,
                 '1':3,
                 '2':9,
                 '3':7,
                 '4':9,
                 '5':7.5,
                 '6':7,
                 '7':6,
                 '8':7,
                 '9':6,
                 '.':3,
                 ',':3,
                 "'": 3,
                 ';':3,
                 '-':9,
                 ':':3,
                 '\n':0,
                 }

SPECIAL_CHARS = {".": "period",
                 ",": "comma",
                 "'": "apostrophe",
                 ";":"semicolon",
                 '-':"hyphen",
                 ":": "colon"}

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
        self.y = init_y+(-LETTER_HEIGHT+y)+self.random()*2
        self.update_point()

    def update_point(self):
        self.ctx.move_to(self.x, self.y)

    def next_line(self):
        self.x = self.START_X
        self.y += self.LINE_HEIGHT
        self.ctx.move_to(self.x, self.y)

    def space_bar(self):
        self.x += LETTER_SPACING + abs(self.random()*3)

    def type(self, string):
        words = string.split(' ')
        for word in words:
            init_x = self.x
            for ch in word:
                try:
                    init_x += LETTER_WIDTHS[ch]
                except:
                    print(f"Letter width for {ch} not found.")
            if init_x >= self.X_LIMIT:
                self.next_line()

            for ch in word:
                if ch == '\n':
                    self.next_line()
                    continue
                if ch == ' ':
                    self.space_bar()
                    continue                    
                try:
                    if ch >= 'A' and ch <= 'Z':
                        doc = minidom.parse(f'letters/{ch}2.svg')
                    elif ch >= 'a' and ch <= 'z' or ch >= '0' and ch <= '9':
                        doc = minidom.parse(f'letters/{ch}.svg')
                    else:
                        doc = minidom.parse(f'letters/{SPECIAL_CHARS[ch]}.svg')
                except:
                    print(f"Letter {ch} file not found")
                
                
                path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
                doc.unlink()

                init_x, init_y = self.x, self.y + self.small_random()*3
                for path in path_strings:
                    if len(re.split(' |,', path)) >= 12:
                        self.execute2(init_x, init_y, path)
                    else:
                        self.execute(init_x, init_y, path)
                self.x = init_x
                self.y = init_y

                if ch != ' ':
                    try:
                        self.x += LETTER_WIDTHS[ch] + abs(self.random())
                    except:
                        pass
                
                if self.x > self.X_LIMIT:
                    self.x = self.START_X
                    self.y += self.LINE_HEIGHT

                self.ctx.move_to(self.x, self.y)
                self.prev_char = ch
            self.space_bar()