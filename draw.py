import cairo
from char_gen import TypeWriter

# A4 measurements in points
WIDTH = 793.701
HEIGHT = 1020.472

MARGIN_LEFT = 25 # Actual margin - 25
MARGIN_RIGHT = 100
FIRST_LINE_Y = 157

LINE_HEIGHT = 30.6

NO_OF_LINES = 28

with cairo.SVGSurface("example.svg", WIDTH, HEIGHT) as surface:
    ctx = cairo.Context(surface)
    
    # #LEFT-ROW
    # for i in range(0, 27):
    #     ctx.rectangle(MARGIN_LEFT, FIRST_LINE_Y+LINE_HEIGHT*i, 10, 10)


    # #TOP-RIGHT
    # ctx.rectangle(WIDTH-MARGIN_RIGHT, FIRST_LINE_Y, 10, 10)

    ctx.fill()

    str = "\n\n\n\n\n\n\n\n\n\n\nIn Java, BufferedReader is a class can be used to read text from a character input stream. It belongs to the java.io package. It buffers the input, that is, it stores the input characters in an internal buffer from which the data can be read. This is more efficient than directly reading the data from the input stream. To use BufferedReader to read an input stream, we need to use the following syntax. If we want to use BufferedReader to read input given by user from the console, we need to make an InputStreamReader from the input stream System.in The following code demonstrates how we can do the above"

    writer = TypeWriter(ctx, MARGIN_LEFT, FIRST_LINE_Y, WIDTH-MARGIN_RIGHT, LINE_HEIGHT)
    writer.type(str.lower().replace('.', ' ').replace("'", '').replace(',', ''))
    
