#!/usr/bin/env python

import math
import random
import cairo

#CONSTANTS
ROWS = 6
COLUMNS = 6
maze = []
WIDTH, HEIGHT = 512, 512
START_X, START_Y = WIDTH/2, 0
CELL_SIZE = 1.0/ROWS
DEBUG_MODE = 1

#cell information
#north, east, south, west, visited
cell = [1,1,1,1,0]

#FUNCTION DECLARATIONS

def print_maze (maze):
	for i in range (0, ROWS):
		for j in range (0, COLUMNS):
			print maze[i][j],
		print "\n"
	
		
def random_number_generator (min, max):	
	return random.randint(min, max)
	
def fill_map (list):
	
	for i in range (0, ROWS):
		sub = []
		for j in range (0, COLUMNS):
			sub.append([random_number_generator (0,1),random_number_generator (0,1),random_number_generator (0,1),random_number_generator (0,1),0])
		list.append(sub)

def draw_maze_old (list):
	#draw vertical lines
	for i in range (0, ROWS+1):
		ctx.move_to(0,  i*CELL_SIZE)
		ctx.line_to(1, i*CELL_SIZE)  # Line to (x,y)
		ctx.set_line_width(0.002)
		ctx.stroke()
	#draw horizontal lines
	for i in range (0, COLUMNS+1):
		ctx.move_to(i*CELL_SIZE,  0)
		ctx.line_to(i*CELL_SIZE, 1)  # Line to (x,y)
		ctx.set_line_width(0.002)
		ctx.stroke()

#Draw maze doesn't check if cell next to it has walls
def draw_maze (list):
	ctx.set_line_width(0.003)
	for i in range (0, ROWS):
		for j in range (0, COLUMNS):
			#draw north
			if list [i][j][0] == 1:
				#first one is x, second y direction
				ctx.move_to(i * CELL_SIZE, j*CELL_SIZE)
				ctx.line_to(i * CELL_SIZE + CELL_SIZE, j*CELL_SIZE)  # Line to (x,y)	
			#draw east
			if list [i][j][1] == 1:
				#first one is x, second y direction
				ctx.move_to(i * CELL_SIZE + CELL_SIZE, j*CELL_SIZE)
				ctx.line_to(i * CELL_SIZE + CELL_SIZE, j*CELL_SIZE + CELL_SIZE)  # Line to (x,y)
			#draw south
			if list [i][j][2] == 1:
				#first one is x, second y direction
				ctx.move_to(i * CELL_SIZE, j*CELL_SIZE+CELL_SIZE)
				ctx.line_to(i * CELL_SIZE + CELL_SIZE, j*CELL_SIZE+CELL_SIZE)  # Line to (x,y)
			#draw west
			if list [i][j][3] == 1:
				#first one is x, second y direction
				ctx.move_to(i * CELL_SIZE, j*CELL_SIZE)
				ctx.line_to(i * CELL_SIZE, j*CELL_SIZE + CELL_SIZE)  # Line to (x,y)


				
def draw_debug (list):
	for i in range (0, ROWS):
		for j in range (0, COLUMNS):
			ctx.select_font_face('Sans')
			ctx.set_font_size(CELL_SIZE*0.10)
			ctx.move_to(i*CELL_SIZE*1.1, j*CELL_SIZE+CELL_SIZE/2)
			ctx.set_source_rgb(0, 0, 0) # yellow
			ctx.show_text("N%dE%dS%dW%d" % (list[i][j][0],list[i][j][1],list[i][j][2],list[i][j][3]))
			
#MAIN LOOP

#choose random starting point
row = random_number_generator(0, COLUMNS-1)
column = random_number_generator(0, ROWS-1)
#fill map with randoms atm
fill_map(maze)

#cairo initialization
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

draw_maze (maze)
if DEBUG_MODE == 1:
	draw_debug (maze)

ctx.stroke()
surface.write_to_png("maze.png")  # Output to PNG

print "ROW %d, COLUMN %d\n" % (row, column)
#print_maze (maze)
print maze [5][5][1]
