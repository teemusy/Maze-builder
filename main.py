#!/usr/bin/env python3

import math
import random
import cairo
import sys
print(sys.version)

#TODO
#add library for directions

#CONSTANTS
ROWS = 50
COLUMNS = 50
LOOPS = ROWS*COLUMNS
WIDTH, HEIGHT = 512, 512
START_X, START_Y = WIDTH/2, 0
CELL_SIZE = 1.0/ROWS
DEBUG_MODE = 0


maze = []

#FUNCTION DECLARATIONS

def print_maze (maze):
	for i in range (0, ROWS):
		for j in range (0, COLUMNS):
			print (maze[i][j]),
		print ("\n")
	
		
def random_number_generator (min, max):	
	return random.randint(min, max)
	
def fill_map (list):
	for i in range (0, ROWS):
		sub = []
		for j in range (0, COLUMNS):
			sub.append([1,1,1,1,0])
		list.append(sub)

#binary tree algorithm
#http://weblog.jamisbuck.org/2011/2/1/maze-generation-binary-tree-algorithm
#rows/columns and x/y mixed
def build_binary_maze (maze_list):
	for i in range (0, ROWS):
		for j in range (0, COLUMNS):
			#0 north, 1 west
			#x,y coordinates
			random_direction = random_number_generator(0, 1)
			print ("Random %d" % (random_direction))
			print ("i:%d j:%d" % (i, j))
			
			if random_direction == 0:
				if j > 0: 
					print("Carve north")
					maze_list [i][j][0] = 0
					maze_list [i][j-1][2] = 0
				elif i > 0:
					print("Carve west")
					maze_list [i][j][3] = 0
					maze_list [i-1][j][1] = 0
				

					
			if random_direction == 1:
				if i > 0:
					print("Carve west")
					maze_list [i][j][3] = 0
					maze_list [i-1][j][1] = 0
				elif j > 0:
					print("Carve north")
					maze_list [i][j][0] = 0
					maze_list [i][j-1][2] = 0
					
					
		j = 0


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
			ctx.show_text("N%dE%dS%dW%dv%d" % (list[i][j][0],list[i][j][1],list[i][j][2],list[i][j][3],list[i][j][4]))
			

#MAIN LOOP

#init map
fill_map (maze)

#cairo initialization
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas


#build_maze(cell_list, maze)
build_binary_maze(maze)

draw_maze (maze)

if DEBUG_MODE == 1:
	#maze[2][1][0] = 5
	draw_debug (maze)

	
ctx.stroke()
surface.write_to_png("maze.png")  # Output to PNG


