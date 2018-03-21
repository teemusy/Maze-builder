#!/usr/bin/env python3

import math
import random
import cairo
import sys
print(sys.version)

#CONSTANTS
ROWS = 6
COLUMNS = 6
LOOPS = ROWS*COLUMNS
maze = []
WIDTH, HEIGHT = 512, 512
START_X, START_Y = WIDTH/2, 0
CELL_SIZE = 1.0/ROWS
DEBUG_MODE = 1

#cell information
#north, east, south, west, visited
cell = [1,1,1,1,0]
cell_list = []

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

#uses growing tree algorithm to build the maze
#http://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
def build_maze_old (c_list, maze_list):

	for xyz in range (0,LOOPS):
		cell_list_size = len(c_list)
		#choose random cell where to start
		random_cell = random_number_generator(0, cell_list_size-1)
		grid_row = c_list[random_cell][0]
		grid_column = c_list [random_cell][1]
		
		#convert list to int
		grid_row = grid_row[0]
		grid_column = grid_column[0]

		
		directions = 0
		#choose direction, change to random later
		direction_to_carve = 0
		#no switch case in python!!11 :(
		#check all directions first?
		#north
		while directions < 4:
			directions += 1
			
			if direction_to_carve == 0:
				#check that list index is not out of range
				if grid_row > 0:
					if maze_list [grid_row-1][grid_column][4] == 0:
						#add new cell to c_list
						sub = [grid_row-1],[grid_column]
						c_list.append(sub)
						#carve walls from both cells
						maze_list [grid_row][grid_column][0] = 0
						maze_list [grid_row-1][grid_column][3] = 0
						#mark as visited
						maze_list [grid_row][grid_column][4] = 1
						maze_list [grid_row-1][grid_column][4] = 1
						direction_to_carve += 1
			#east
			elif direction_to_carve == 1:
				if grid_column < COLUMNS-1:
					if maze_list [grid_row][grid_column+1][4] == 0:
						#add new cell to c_list
						sub = [grid_row],[grid_column+1]
						c_list.append(sub)
						#carve walls from both cells
						maze_list [grid_row][grid_column][1] = 0
						maze_list [grid_row-1][grid_column+1][4] = 0
						#mark as visited
						maze_list [grid_row][grid_column][4] = 1
						maze_list [grid_row-1][grid_column+1][4] = 1
						direction_to_carve += 1
			#south
			elif direction_to_carve == 2:
				if grid_row < ROWS-1:
					if maze_list [grid_row+1][grid_column][4] == 0:
						#add new cell to c_list
						sub = [grid_row+1],[grid_column]
						c_list.append(sub)
						#carve walls from both cells
						maze_list [grid_row][grid_column][3] = 0
						maze_list [grid_row+1][grid_column][0] = 0
						#mark as visited
						maze_list [grid_row][grid_column][4] = 1
						maze_list [grid_row+1][grid_column][4] = 1
						direction_to_carve += 1
			#west
			elif direction_to_carve == 3:
				if grid_column > 0:
					if maze_list [grid_row][grid_column-1][4] == 0:
						#add new cell to c_list
						sub = [grid_row-1],[grid_column-1]
						c_list.append(sub)
						#carve walls from both cells
						maze_list [grid_row][grid_column][4] = 0
						maze_list [grid_row-1][grid_column-1][1] = 0
						#mark as visited
						maze_list [grid_row][grid_column][4] = 1
						maze_list [grid_row-1][grid_column-1][4] = 1
						direction_to_carve += 1
			else:
				#remove random_cell from clist
				c_list.remove(random_cell)
			directions += 1

		
		
def build_maze (c_list, maze_list):		
	for xyz in range (0,LOOPS):
		#choose random cell from c_list
		#choose random direction
			#check if it's unvisited
			#if so carve path there and add location to c_list
		#repeat
		
		#choose random cell
		cell_list_size = len(c_list)
		#choose random cell where to start
		random_cell = random_number_generator(0, cell_list_size-1)
		grid_row = c_list[random_cell][0]
		grid_column = c_list[random_cell][1]
		grid_row = grid_row[0]
		grid_column = grid_column[0]
		
		#random direction
		random_direction = random_number_generator(0, 3)
		
		
		
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
			
def choose_random_cell (list):
	sub = [[random_number_generator(0, COLUMNS-1)],[random_number_generator(0, ROWS-1)]]
	list.append(sub)

#MAIN LOOP

#init map
fill_map (maze)

#cairo initialization
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)
ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

#choose random starting point
choose_random_cell(cell_list)

build_maze(cell_list, maze)

draw_maze (maze)

if DEBUG_MODE == 1:
	draw_debug (maze)

ctx.stroke()
surface.write_to_png("maze.png")  # Output to PNG


print (cell_list)

