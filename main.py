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

DEBUG_MODE = 0

#cmd line arguments

if sys.argv[len(sys.argv)-1] == "-d":
	DEBUG_MODE = 1
	ROWS = 5
	COLUMNS = 5
	print ("Debug mode on")
if sys.argv[len(sys.argv)-1] == "-b":
	algo_chooser = 1
else:
	algo_chooser = 0

CELL_SIZE = 1.0/ROWS
maze = []
c_list = []
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

#Growing tree algo
def build_tree_maze (c_list, maze_list):

	for xyz in range (0,LOOPS*100):
		#choose random cell from c_list
		#choose random direction
			#check if it's unvisited
			#if so carve path there and add location to c_list
			#if not check next direction until all directions have been checked
		#remove visited cell from list
		#repeat
		cell_list_size = len(c_list)
		#break loop if cell list size == 0
		if cell_list_size == 0:
			break
		
		#choose random cell where to start
		random_cell = 0
		if cell_list_size > 0:
			random_cell = random_number_generator(0, cell_list_size-1)
		
		grid_row = c_list[random_cell][0]
		grid_column = c_list [random_cell][1]
		
		#convert list to int
		grid_row = grid_row[0]
		grid_column = grid_column[0]
		n = e = s = w = 0
		found_legal_direction = 0
		#loop until all directions checked or found legal direction
		while (n == 0 or e == 0 or s == 0 or w == 0) and found_legal_direction == 0:
			direction_to_carve = random_number_generator (0, 3)
			if direction_to_carve == 0:
				n = 1		
			elif direction_to_carve == 1:
				e = 1		
			elif direction_to_carve == 2:
				s = 1		
			elif direction_to_carve == 3:
				w = 1
			
			
			#north
			if direction_to_carve == 0:
				
				#check if north is legal direction and cell in north has not been visited
				if grid_column > 0:
					if maze_list[grid_row][grid_column-1][4] == 0:
						#add direction to c_list
						sub = [grid_row],[grid_column-1]
						c_list.append(sub)
						#add visited flag
						maze_list[grid_row][grid_column-1][4] = 1
						#carve wall
						maze_list[grid_row][grid_column][0] = 0
						maze_list[grid_row][grid_column-1][2] = 0
						found_legal_direction = 1			
			
			#east
			if direction_to_carve == 1:
				
				#check if east is legal direction and cell in east has not been visited
				if grid_row < COLUMNS-1:
						if maze_list[grid_row+1][grid_column][4] == 0:
							#add direction to c_list
							sub = [grid_row+1],[grid_column]
							c_list.append(sub)
							#add visited flag
							maze_list[grid_row+1][grid_column][4] = 1
							#carve wall
							maze_list[grid_row][grid_column][1] = 0
							maze_list[grid_row+1][grid_column][3] = 0
							found_legal_direction = 1			
					
			#south
			if direction_to_carve == 2:
				
				#check if south is legal direction and cell in south has not been visited
				if grid_column < ROWS-1:
					if maze_list[grid_row][grid_column+1][4] == 0:
						#add direction to c_list
						sub = [grid_row],[grid_column+1]
						c_list.append(sub)
						#add visited flag
						maze_list[grid_row][grid_column+1][4] = 1
						#carve wall
						maze_list[grid_row][grid_column][2] = 0
						maze_list[grid_row][grid_column+1][0] = 0
						found_legal_direction = 1			
					
			#west
			if direction_to_carve == 3:
				
				#check if west is legal direction and cell in west has not been visited
				if grid_row > 0 and maze_list[grid_row-1][grid_column][4] == 0:
					#add direction to c_list
					sub = [grid_row-1],[grid_column]
					c_list.append(sub)
					#add visited flag
					maze_list[grid_row-1][grid_column][4] = 1
					#carve wall
					maze_list[grid_row][grid_column][3] = 0
					maze_list[grid_row-1][grid_column][1] = 0
					found_legal_direction = 1
		
		if n == 1 and e == 1 and s == 1 and w == 1:
			c_list.pop(random_cell)
		
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

choose_random_cell(c_list)

if algo_chooser == 1:
	build_binary_maze(maze)
else:
	build_tree_maze(c_list, maze)

draw_maze (maze)

if DEBUG_MODE == 1:
	#maze[2][1][0] = 5
	draw_debug (maze)

print (c_list)
ctx.stroke()
surface.write_to_png("maze.png")  # Output to PNG


