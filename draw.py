import cairo
from char_gen import TypeWriter

# A4 measurements in points
WIDTH = 793.701
HEIGHT = 1020.472

MARGIN_LEFT = 25 # Actual margin - 25
MARGIN_RIGHT = 25
FIRST_LINE_Y = 157

LINE_HEIGHT = 30.6

NO_OF_LINES = 28

with cairo.SVGSurface("example.svg", WIDTH, HEIGHT) as surface:
    ctx = cairo.Context(surface)

    writer = TypeWriter(ctx, MARGIN_LEFT, FIRST_LINE_Y, WIDTH-MARGIN_RIGHT, LINE_HEIGHT)
    writer.type("                     Experiment No. 12 \n\nAim -\nTo test if the HandwriteTonic100 prints us an assignment which looks handwritten.\n\nTheory -\nIn Java, BufferedReader is a class; can be used to read text from a character input stream. It belongs to the java.io package. It buffers the input, that is: it stores the input characters in an internal buffer from which the data can be read. This is more efficient than directly reading the data from the input stream. To use BufferedReader to read an input stream, we need to use the following syntax. If we want to use BufferedReader to read input given by user from the console, we need to make an InputStreamReader from the input stream System.in The following code demonstrates how we can do the above. You got it. I tried that before, but I was setting the imagesurface as source AND ONLY THEN doing thre scaling operation. So, it is necessary to scale FIRST and only then set the source. Thanks. \n\nJeremy Flores solved my problem very well by scaling the target surface before setting the imagesurface as source. Even though, perhaps some day you actually NEED to resize a Surface (or transform it in any way), so I will briefly describe the rationale used in my alternate answer (already included in the question), deduced after thoroughly reading the docs:")
    writer.type("\nTo test if the HandwriteTonic100 prints us an assignment which looks handwritten. In Java, BufferedReader is a class; can be used to read text from a character input stream. It belongs to the java.io package. It buffers the input, that is: it stores the input characters in an internal buffer from which the data can be read.")

