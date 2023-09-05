import cairo
import math
import random
import re

LETTER_SPACING = 12
RANDOMNESS_SCALE = 1.6
LINE_WIDTH = 0.8
MIN_LINE_WIDTH = 0.4
MAX_LINE_WIDTH = 1
LETTER_HEIGHT = 14

LETTER_WIDTHS = [10, 7, 11, 7, 9.5, 6, 7, 7, 6, 3, 6, 3, 10, 7, 8, 10, 8, 10, 7, 6, 8, 8, 8, 10, 7, 9]

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
                pass
            if ch == '1':
                self.x+=5

                init_x, init_y = self.x, self.y
                self.ctx.move_to(self.x, self.y+self.random()*2)
                self.line(0, -14)

                self.x = init_x-2
                self.y = init_y
            if ch == '2':
                init_x, init_y = self.x, self.y
                self.x -= -2+self.random()
                self.y -= 14+self.random()

                #First arc of the 2
                self.ctx.move_to(self.x, self.y)
                x1, y1, x2, y2 = 2.2, -14.6, 12.4, -10.4
                xf, yf = self.random(), self.random()
                self.arc(init_x, init_y, x1, y1, x2, y2, xf, yf)

                # Second arc of 2
                self.x = init_x+xf
                self.y = init_y+yf
                self.ctx.move_to(self.x, self.y)
                self.ctx.curve_to(init_x+2+self.random(), init_y, init_x+8+self.random(), init_y, init_x+10+self.random(), init_y+self.random()*1.5)
                self.ctx.stroke()

                self.update_stroke()

                # Shift by 6 to the right for 2 specifically
                self.x = init_x + 6
                self.y = init_y
            if ch == 'a':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 6.7052927,5.3400492 C -1.747051,5.5468706 -2.1039365,15.898133 8.3681957,12.785046")
                self.execute(init_x, init_y, "M 6.804019,4.6722796 C 8.0085747,11.738112 8.4248638,13.009773 9.1793982,13.900078")

                self.x = init_x
                self.y = init_y
            if ch == 'b':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 0.98271748,2.8413352 C 1.2206829,11.224923 0.740479,13.819642 1.3245322,13.864861 4.6981036,14.126051 9.6130604,5.7763503 1.3672591,8.8871833")

                self.x = init_x
                self.y = init_y
            if ch == 'c':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 7.4020483,5.468452 C -1.0301227,6.1519121 -3.3607625,16.092919 9.4867066,12.930925")

                self.x = init_x
                self.y = init_y
            if ch == 'd':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 5.5318337,6.9466423 C 0.12071194,3.8844523 -3.1155607,16.20167 5.4993013,13.257937")
                self.execute(init_x, init_y, "M 5.694496,2.3270354 C 5.135694,14.286448 5.6985662,11.726133 5.5318339,14.591766")

                self.x = init_x
                self.y = init_y
            if ch == 'e':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 1.1463691,8.3959002 C 4.9370479,11.549864 8.6274631,6.3664306 6.3755507,5.7561691 -1.2083839,3.7009455 -2.652524,19.069651 8.6130375,11.73956")

                self.x = init_x
                self.y = init_y
            if ch == 'f':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.04272685,7.5412883 C 1.6940604,7.6443078 4.4435826,7.2182954 6.1953926,7.0712929")
                self.execute(init_x, init_y, "M 2.9357876,13.873701 C 3.41497,7.1728204 1.6434274,0.85171025 6.2912589,1.7436523")

                self.x = init_x
                self.y = init_y
            if ch == 'g':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 5.4476728,6.772205 C -1.2259767,5.2166626 -1.8119233,17.193257 5.8749412,12.946234")
                self.execute(init_x, init_y, "M 5.5727147,6.5125692 C 5.8332606,19.790134 7.4982198,23.538677 0.12800515,18.182115")

                self.x = init_x
                self.y = init_y
            if ch == 'h':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.70834809,7.1267919 C 5.3882006,6.5004146 5.8439735,7.0610434 5.2066712,14.004469")
                self.execute(init_x, init_y, "M 0.39346032,2.1138993 C 0.77736885,13.08098 0.64970499,13.179499 0.6640228,14.171047")

                self.x = init_x
                self.y = init_y
            if ch == 'i':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 1.2136555,5.7073702 C -0.89860613,6.3148921 2.181473,6.5706907 1.0537814,5.7073701")
                self.execute(init_x, init_y, "M 0.93120306,7.4663866 C 0.93120306,15.895071 0.99098056,13.053422 0.92734276,13.653092")

                self.x = init_x
                self.y = init_y
            if ch == 'j':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.73459421,7.4301414 C 1.1497035,15.489287 0.51353992,22.549752 -4.9768265,16.964034")
                self.execute(init_x, init_y, "M 0.95855421,5.3220563 C -1.1537078,5.9295783 1.9263712,6.1853763 0.79867921,5.3220563")

                self.x = init_x
                self.y = init_y
            if ch == 'k':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.2870182,1.9335963 C 0.46052886,8.9655408 0.43808042,12.06615 0.37765553,14.018573")
                self.execute2(init_x, init_y, "M 5.4080272,3.8369802 C 1.808621,8.0023016 -0.45360496,7.7688787 0.54382397,8.1875719 4.8977157,10.015215 4.1596565,10.334829 4.8944156,13.988361")

                self.x = init_x
                self.y = init_y
            if ch == 'l':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.33233687,1.7825341 C 0.78552347,14.048787 0.72509857,11.964128 0.78552347,14.078999")

                self.x = init_x
                self.y = init_y
            if ch == 'm':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.27005481,5.0361384 C 0.42949949,13.132651 0.49327738,12.040265 0.42949949,13.903747")
                self.execute2(init_x, init_y, "M 0.36046465,6.5870587 C 2.7712391,2.5029781 3.3126263,5.1016957 4.0689448,9.3407898 4.2053322,10.105229 8.2982119,-4.8219688 8.0166818,14.04775")

                self.x = init_x
                self.y = init_y
            if ch == 'n':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.29977924,4.8409222 C 0.45922394,12.937435 0.52300184,12.116961 0.45922394,13.980443")
                self.execute(init_x, init_y, "M 0.45318664,5.740364 C 2.5393504,5.5620297 6.1775309,4.8358411 5.3476023,13.595599")

                self.x = init_x
                self.y = init_y
            if ch == 'o':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 3.962646,5.0546521 C 1.3131624,4.5003679 -2.4793828,12.365246 2.7130091,13.79723 8.5926876,15.418757 7.6955994,5.344871 3.7766079,5.0242904")

                self.x = init_x
                self.y = init_y
            if ch == 'p':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.32601906,4.439307 C 0.40679126,7.568838 0.75320022,15.646698 0.80162632,26.131996")
                self.execute(init_x, init_y, "M 0.40947871,4.7665697 C 14.287956,4.6724352 9.5220622,9.7801015 0.54535695,13.760326")

                self.x = init_x
                self.y = init_y
            if ch == 'q':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 6.4650461,5.7893263 C -1.7122852,1.9562225 -1.9478347,17.851433 7.1194579,12.439823")
                self.execute(init_x, init_y, "M 6.1426591,5.0500189 C 7.31392,19.264887 4.0886434,29.117232 9.0507277,17.773794")

                self.x = init_x
                self.y = init_y
            if ch == 'r':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 0.21148706,4.1088921 C 7.4665056,10.032677 10.781942,13.076517 5.8612138,13.686236 0.8345233,14.309085 0.07819026,10.895006 9.6981944,4.0484669")

                self.x = init_x
                self.y = init_y
            if ch == 's':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 6.1935507,3.7765554 C 1.810348,3.3597524 -2.9945883,7.8404636 3.2025189,8.9428831 11.646978,10.44509 2.6620031,17.436614 0.42297407,12.779864")

                self.x = init_x
                self.y = init_y
            if ch == 't':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 3.589055,1.6022567 C 3.491756,3.1764277 3.8789215,7.3190832 3.7599624,14.057133")
                self.execute(init_x, init_y, "M 0.10269712,6.3045596 C 2.7924895,6.0228314 5.9014338,6.1234514 7.118213,6.0221358")

                self.x = init_x
                self.y = init_y
            if ch == 'u':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.29908789,5.2340386 C -0.0382644,16.544056 6.7496263,16.35698 6.6867513,4.9990412")

                self.x = init_x
                self.y = init_y
            if ch == 'v':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.19227085,4.1872309 C 5.44741,15.69722 0.83342102,18.059933 6.9217489,4.2085947")

                self.x = init_x
                self.y = init_y
            if ch == 'w':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 0.33233687,4.6829285 C 0.64802691,6.8015542 0.84223651,19.181174 2.7795447,11.420304 4.5032109,4.5152848 4.4134292,24.810678 7.1301363,4.8339907")

                self.x = init_x
                self.y = init_y
            if ch == 'x':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.18127463,3.7765552 C 8.5763137,14.139089 9.1154949,13.58229 9.2752196,13.5956")
                self.execute(init_x, init_y, "M 8.0365096,3.8974049 C 3.0479392,12.570135 0.69419113,13.535522 0.63446125,13.565387")

                self.x = init_x
                self.y = init_y
            if ch == 'y':
                init_x, init_y = self.x, self.y

                self.execute(init_x, init_y, "M 0.36029431,4.5593028 C 0.94010876,7.5666666 3.3824459,14.27075 3.7908483,14.040521")
                self.execute(init_x, init_y, "M 7.477198,4.6572263 C 4.5976707,12.293799 1.1367803,17.67687 -0.55544899,19.825257")

                self.x = init_x
                self.y = init_y
            if ch == 'z':
                init_x, init_y = self.x, self.y

                self.execute2(init_x, init_y, "M 0.57403642,4.441229 C 10.433572,4.6240554 11.179933,3.6672888 5.0152655,8.3688466 -2.9105801,14.413588 -0.61557428,13.898892 9.1543702,13.263262")

                self.x = init_x
                self.y = init_y

            if ch != ' ':
                self.x += LETTER_WIDTHS[ord(ch)-ord('a')] + self.random()*3
            if self.x > self.X_LIMIT:
                self.x = self.START_X
                self.y += self.LINE_HEIGHT

            self.ctx.move_to(self.x, self.y)
            self.prev_char = ch
