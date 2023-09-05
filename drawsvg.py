"""\
Usage: drawsvg.py file
file  - one SVG file (from Inkscape!) that is all simple paths

"""
##    svg2py Copyright  (C)  2007 Donn.C.Ingle
##
##    Contact: donn.ingle@gmail.com - I hope this email lasts.
##
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##     ( at your option )  any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
##

import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo
from pyparsing import *
import os, sys
from elementtree import ElementTree as et

# Create a GTK+ widget on which we will draw using Cairo
class Screen(gtk.DrawingArea):

    # Draw in response to an expose-event
    __gsignals__ = { "expose-event": "override" }

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # Fill the background with gray
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

# GTK mumbo-jumbo to show the widget in a window and quit when it's closed
def run(Widget):
    window = gtk.Window()
    window.set_size_request(400, 400)
    window.connect("delete-event", gtk.main_quit)
    widget = Widget()
    widget.show()
    window.add(widget)
    window.present()
    gtk.main()

## Do the drawing ##

class Shapes(Screen):
    def draw(self, ctx, width, height):

        #Build a string of cairo commands
        cairo_commands = ""
        command_list = []
        for tokens in paths:
            for command,couples in tokens[:-1]: #looks weird, but it works :)
                c = couples.asList()
                if command == "M":
                    cairo_commands += "ctx.move_to(%s,%s);" % (c[0],c[1])
                if command == "C":
                    cairo_commands += "ctx.curve_to(%s,%s,%s,%s,%s,%s);" % (c[0],c[1],c[2],c[3],c[4],c[5])
                if command == "L":
                    cairo_commands += "ctx.line_to(%s,%s);" % (c[0],c[1])
                if command == "Z":
                    cairo_commands += "ctx.close_path();"

            command_list.append(cairo_commands) #Add them to the list
            cairo_commands = ""
        #Draw it. Only stroked, to fill as per the SVG drawing is another whole story.
        ctx.set_source_rgb(1,0,0)
        for c in command_list:
            exec(c)
        ctx.stroke()


#Check args:
if len(sys.argv) < 2:
    raise SystemExit(__doc__)
file = sys.argv[1]

## Pyparsing grammar:
## With HUGE help from Paul McGuire <paul@alanweberassociates.com>
## Thanks!
dot = Literal(".")
comma = Literal(",").suppress()
floater = Combine(Optional("-") + Word(nums) + dot + Word(nums))
## Unremark to have numbers be floats rather than strings.
#floater.setParseAction(lambda toks:float(toks[0]))
couple = floater + comma + floater
M_command = "M" + Group(couple)
C_command = "C" + Group(couple + couple + couple)
L_command = "L" + Group(couple)
Z_command = "Z"
svgcommand = M_command | C_command | L_command | Z_command
phrase = OneOrMore(Group(svgcommand))

## Find and open the svg file
xml_file = os.path.abspath(__file__)
xml_file = os.path.dirname(xml_file)
xml_file = os.path.join(xml_file, file)

tree = et.parse(xml_file)

ns = "http://www.w3.org/2000/svg" #The XML namespace.
paths = []
for group in tree.getiterator('{%s}g' % ns):
    for e in group.getiterator('{%s}path' % ns):
        p = e.get("d")
        tokens = phrase.parseString(p.upper())
        paths.append(tokens) # paths is a global var.

run(Shapes)