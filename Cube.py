import pygame
from pygame.locals import *
import random
import sys
import copy
import os

pygame.init()

#set up clock
clock = pygame.time.Clock()
FPS = 5

# game constants
CUBESIZE = 100           # size of small cube. Keep it at least 50. Recommended to keep it a multiple of 10.
CUBENUM = 3            # set if the cube is a 2*2*2, 3*3*3, 4*4*4 or n*n*n type cube.
sizeRatio = 0.3     # tell the proportion of size of secondary cubes

# set up window
WINW = 600
WINH = 600
# check if the cube is between 1*1*1 and 5*5*5 type.
assert 0 < CUBENUM <= 5, "Invalid cube type"
# check if the whole Rubik cube is larger than the window
assert CUBESIZE*(CUBENUM+1) <= WINW, "Window width smaller than cube width."
assert CUBESIZE*(CUBENUM+1) <= WINH, "Window height smaller than cube width."
mainSurface = pygame.display.set_mode((WINW, WINH))
alphaSurface = mainSurface.convert_alpha()
pygame.display.set_caption("Rubik Cube")

# set up color constants for the game
RED = "Red"
GREEN = "Green"
BLUE = "Blue"
YELLOW = "Yellow"
ORANGE = "Orange"
WHITE = "White"

# set up background color
BGCOLOR = (230, 245, 250)
TEXTCOLOR = (120, 120, 120)
BLACK = (0, 0, 0)
HIGHLIGHTCOLOR = (200, 191, 231, 50)

class makeNewCube:    # Make a new solved Rubik cude with Red cubes on the front face
	def __init__(self):
		# Set up the Front, Back, Right, Left, Down and Up faces.
		# make each face as list of lists like this: [[COLOR, COLOR, COLOR],[COLOR, COLOR, COLOR],[COLOR, COLOR, COLOR]]
		self.FRONT = [[RED]*CUBENUM for i in range(CUBENUM)]
		self.BACK = [[ORANGE]*CUBENUM for i in range(CUBENUM)]
		self.RIGHT =[[GREEN]*CUBENUM for i in range(CUBENUM)]
		self.LEFT = [[YELLOW]*CUBENUM for i in range(CUBENUM)]
		self.DOWN = [[BLUE]*CUBENUM for i in range(CUBENUM)]
		self.UP = [[WHITE]*CUBENUM for i in range(CUBENUM)]

		# set up list of lists to store rectangle value of each block of Front, Right and Up faces only
		self.f_RECTS = [[""]*CUBENUM for i in range(CUBENUM)]
		#self.b_RECTS = [[""]*CUBENUM for i in range(CUBENUM)]
		self.r_RECTS = [[""]*CUBENUM for i in range(CUBENUM)]
		#self.l_RECTS = [[""]*CUBENUM for i in range(CUBENUM)]
		#self.d_RECTS = [[""]*CUBENUM for i in range(CUBENUM)]
		self.u_RECTS = [[""]*CUBENUM for i in range(CUBENUM)]

		# set up a list to store the previous moves on the cube
		self.pre_moves = []

	def drawFace(self, face, firstRun, position, sizeRatio):    #draws the given face
		# codes below draw the Front, Right and Up faces which make the main Cube
		if face == "front":
			# I determined the ratio of height and width of each block in each face by doing calculations & experiments
			# So don't change anything with the size and other variables
			size = (round(sizeRatio*76*CUBESIZE/113), round(sizeRatio*153*CUBESIZE/226))
			# In original size, each block image needs to be shifted 24 pixel down from previous cube.
			# So here the each block will be shifted according to the image dimension
			YSHIFT = round(sizeRatio*CUBESIZE*25/226, 2)         # tells how much pixel show each block be shifted down
			x = position[0]                    #starting x-coordinate pixel position of the cube
			y = position[1]
			for i in range(len(self.FRONT)):
				for j in range(len(self.FRONT[i])):
					cubeColor = self.FRONT[i][j]
					cubeImg = pygame.transform.scale(pygame.image.load("Images/Front/%s.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x+i*size[0], y-j*size[1]+(i+j)*YSHIFT)
					self.f_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(30)

		if face == "right":
			YSHIFT = round(sizeRatio*CUBESIZE*50/226, 2)       # in full size, the lefttop of the block is 50 pixel below the lefttop of the image
			if position == TOPRIGHT:
				x = position[0] + CUBENUM*round(sizeRatio*75*CUBESIZE/113, 2)
				y = position[1] - (CUBENUM-1)*round(sizeRatio*CUBESIZE*27/226, 2)
			elif position == MID:
				x = position[0] + CUBENUM*round(sizeRatio*75*CUBESIZE/113, 2)
				y = position[1] + CUBENUM*round(sizeRatio*CUBESIZE*24/226, 2) - YSHIFT
			size = (round(sizeRatio*45*CUBESIZE/113), round(sizeRatio*177*CUBESIZE/226))
			for i in range(len(self.RIGHT)):
				for j in range(len(self.RIGHT[i])):
					if position == MID:
						cubeColor = self.RIGHT[i][j]
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Sides/%s.png" % cubeColor), size)
					elif position == TOPRIGHT:
						cubeColor = self.RIGHT[CUBENUM-1-i][j]
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Sides/%s_reverse.png" % cubeColor), (round(size[0]*1.1), size[1]))
					cubeRect = cubeImg.get_rect()
					if position == MID:
						cubeRect.topleft = (x+i*size[0], y-j*size[1]+(j-i)*YSHIFT)
						self.r_RECTS[i][j] = cubeRect
					elif position == TOPRIGHT:
						cubeRect.topleft = (x+i*size[0], y-j*size[1]+(i+j)*YSHIFT)
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(30)

		if face == "up":
			YSHIFT1 = round(sizeRatio*CUBESIZE*25/226, 2)
			YSHIFT2 = round(sizeRatio*CUBESIZE*46/226, 2)
			XSHIFT = round(sizeRatio*CUBESIZE*89/226, 2)
			x = position[0]
			y = position[1] - (CUBENUM-1)*round(sizeRatio*153*CUBESIZE/226, 2) - YSHIFT2 + (CUBENUM-1)*round(sizeRatio*CUBESIZE*24/226, 2)
			size = (round(sizeRatio*1.06*CUBESIZE), round(sizeRatio*73*CUBESIZE/226))
			for i in range(len(self.UP)):
				for j in range(len(self.UP[i])):
					cubeColor = self.UP[i][j]
					cubeImg = pygame.transform.scale(pygame.image.load("Images/Up/%s.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x+i*size[0]+(j-i)*XSHIFT, y+i*YSHIFT1-j*YSHIFT2)
					self.u_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(30)

		# codes below draw a small cube (size: 25% of main cube) showing Back, Left and Down faces
		if face == "back":
			# same as for Front face but this is one has smaller dimension i.e 0.25 of front face
			size = (round(sizeRatio*76*CUBESIZE/113), round(sizeRatio*153*CUBESIZE/226))
			YSHIFT = round(sizeRatio*CUBESIZE*27/226, 2)
			x = position[0]
			y = position[1]
			for i in range(len(self.BACK)):
				for j in range(len(self.BACK[i])):
					cubeColor = self.BACK[i][j]
					if position == TOPRIGHT:
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Front/%s_reverse.png" % cubeColor), size)
					elif position == TOPLEFT:
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Front/%s.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					if position == TOPRIGHT:
						cubeRect.topleft = (x+i*size[0], y-j*size[1]+(j-i)*YSHIFT)
					elif position == TOPLEFT:
						cubeRect.topleft = (x+i*size[0], y-j*size[1]+(i+j)*YSHIFT)
					#cube.b_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(30)

		if face == "left":
			# same as of Right face but smaller
			YSHIFT = round(sizeRatio*CUBESIZE*47/226, 2)
			size = (round(sizeRatio*45*CUBESIZE/113), round(sizeRatio*175*CUBESIZE/226))
			if position == TOPLEFT:
				x = position[0] - size[0]
				y = position[1]
			for i in range(len(self.LEFT)):
				for j in range(len(self.LEFT[i])):
					cubeColor = self.LEFT[i][j]
					if position == TOPLEFT:
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Sides/%s.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x-i*size[0], y-j*size[1]+(i+j)*YSHIFT)
					#cube.l_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(30)

		if face == "down":
			# same as of Up face but smaller
			YSHIFT1 = round(sizeRatio*CUBESIZE*23/226, 2)
			YSHIFT2 = round(sizeRatio*CUBESIZE*45/226, 2)
			XSHIFT1 = round(sizeRatio*CUBESIZE*81/226, 2)
			XSHIFT2 = round(sizeRatio*CUBESIZE*84/226, 2)
			if position == TOPRIGHT:
				x = position[0]
				y = position[1] + round(sizeRatio*153*CUBESIZE/226) - YSHIFT1
			elif position == TOPLEFT:
				x = position[0]-XSHIFT1*1.03
				y = position[1]+round(sizeRatio*153*CUBESIZE/226)-round(sizeRatio*CUBESIZE*27/226, 2)
			size = (round(sizeRatio*1.04*CUBESIZE), round(sizeRatio*72*CUBESIZE/226))
			for i in range(len(self.DOWN)):
				for j in range(len(self.DOWN[i])):
					cubeColor = self.DOWN[i][j]
					if position == TOPRIGHT:
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Up/%s_reverse.png" % cubeColor), (round(size[0]*1.1), size[1]))
					elif position == TOPLEFT:
						cubeImg = pygame.transform.scale(pygame.image.load("Images/Up/%s.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					if position == TOPRIGHT:
						cubeRect.topleft = (x+i*(size[0]-XSHIFT1)+j*XSHIFT2, y-i*(YSHIFT1+0.5)+j*YSHIFT2)
					elif position == TOPLEFT:
						cubeRect.topleft = (x+i*size[0]-(i+j)*XSHIFT2, y+i*YSHIFT1+j*YSHIFT2)
					#cube.d_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(30)

	def drawCube(self, faces, firstRun, position, sizeRatio):
		# draw front, (right/left) and (top/down) faces.
		for face in faces:
			self.drawFace(face, firstRun, position, sizeRatio)
		if firstRun and position == MID:
			self.shuffleCube()

	def rotateLayer(self, dir, column, row):        # make necessary changes to adjust the colors in faces before swapping them
		# While rotating the layers, the (0, 0) coordinate of one face may not be the (0, 0) coordinate of another face.
		# So we determine the new correct coordinate of the blocks in the new layer and then put them there.

		# Right and left faces are rotated in both vertical and horizontal rotations. So we will always need them
		dupe_right = copy.deepcopy(self.RIGHT)
		dupe_left = copy.deepcopy(self.LEFT)
		if dir in ["Up", "Down"]:
			# make duplicate lists for each face that will change while rotating the layers Up or Down (vertically)
			dupe_up = copy.deepcopy(self.UP)
			dupe_down = copy.deepcopy(self.DOWN)
			# column value is in the string to ease iteration: if we need to rotate column with index 1, column = "1"
			# if we need to rotate all 3 columns of a face, column = "012"
			column = str(column)
			for x in column:
				x = int(x)      # x value is converted from string to integer as it will be used in indexing later
				for y in range(CUBENUM):
					if dir == "Up":
						for dupeFace, face in [dupe_right, self.DOWN], [dupe_up, self.RIGHT], [dupe_left, self.UP], [dupe_down, self.LEFT]:
							if dupeFace == dupe_right:
								dupeFace[x][CUBENUM-1-y] = face[CUBENUM-1-y][CUBENUM-1-x]
							elif dupeFace == dupe_down:
								dupeFace[y][CUBENUM-1-x] = face[CUBENUM-1-x][CUBENUM-1-y]
							elif dupeFace == dupe_left:
								dupeFace[CUBENUM-1-x][CUBENUM-1-y] = face[CUBENUM-1-y][x]
							elif dupeFace == dupe_up:
								dupeFace[CUBENUM-1-y][x] = face[x][y]
					if dir == "Down":
						for dupeFace, face in [dupe_right, self.UP], [dupe_up, self.LEFT], [dupe_left, self.DOWN], [dupe_down, self.RIGHT]:
							if dupeFace == dupe_right:
								dupeFace[x][CUBENUM-1-y] = face[y][x]
							elif dupeFace == dupe_up:
								dupeFace[y][x] = face[CUBENUM-1-x][y]
							elif dupeFace == dupe_left:
								dupeFace[CUBENUM-1-x][CUBENUM-1-y] = face[y][CUBENUM-1-x]
							elif dupeFace == dupe_down:
								dupeFace[CUBENUM-1-y][CUBENUM-1-x] = face[x][CUBENUM-1-y]

			# assign the changed duplicated faces to original faces.
			self.RIGHT, self.UP, self.LEFT, self.DOWN = dupe_right, dupe_up, dupe_left, dupe_down
		if dir in ["Left", "Right"]:
			dupe_front = copy.deepcopy(self.FRONT)
			dupe_back = copy.deepcopy(self.BACK)
			row = str(row)
			if dir == "Right":
				hFaces = [dupe_front, self.LEFT, dupe_right, self.FRONT, dupe_back, self.RIGHT, dupe_left, self.BACK]     # faces at horizontal plane
			elif dir == "Left":
				hFaces = [dupe_front, self.RIGHT, dupe_right, self.BACK, dupe_back, self.LEFT, dupe_left, self.FRONT]
			for x in range(CUBENUM):
				row = int(row)
				for i in range(0, len(hFaces), 2):
					if (hFaces[i] == dupe_back) or (hFaces[i] in [dupe_left] and dir == "Right") or (hFaces[i] == dupe_right and dir == "Left"):
						hFaces[i][x][row] =hFaces[i+1][CUBENUM-1-x][row]
						continue
					hFaces[i][x][row] =hFaces[i+1][x][row]
			self.FRONT, self.RIGHT, self.BACK, self.LEFT = dupe_front, dupe_right, dupe_back, dupe_left

	def rotateFace(self, face, direction, frequency):      # when layers at edges are rotated horizontally or vertically, face adjacent to that layer also needs to rotate
		# rotateFace is different from rotateLayer function. This function rotates the colors within the same face in a clockwise or anti-clockwise direction
		dupe_face = copy.deepcopy(face)  # make a copy of the required face
		for f in range(frequency):          # rotates the layer Clockwise/Anticlockwise for given times such that it rotates 90 degree in each turn
			final_dupe_face = copy.deepcopy(dupe_face)
			for x in range(CUBENUM):
				for y in range(CUBENUM):
					if direction == "C":            # for clockwise rotation
						dupe_face[y][CUBENUM-1-x] = final_dupe_face[x][y]
					elif direction == "AC":        # for anticlockwise rotation
						dupe_face[CUBENUM-1-y][x] = final_dupe_face[x][y]
			final_dupe_face = copy.deepcopy(dupe_face)
		return final_dupe_face

	def rotateCube(self, clicked, dir, eventPos, time, appendMove):
		time += 2/FPS       # rotating the cube slows down the game so increasing time here too to keep the time tick normal
		if appendMove:
			if dir in ["Left", "Right"]:
				opp_dir = [d for d in ["Left", "Right"] if dir != d][0]
			elif dir in ["Up", "Down"]:
				opp_dir = [d for d in ["Up", "Down"] if dir != d][0]
			try:
				self.pre_moves.append([clicked, opp_dir, eventPos])
				if len(self.pre_moves) > 10:        # only store previous 10 moves
					self.pre_moves.remove(self.pre_moves[0])    # delete the oldest move
			except UnboundLocalError:       # sometime when the cube is rotated fast, this error arise: "UnboundLocalError: local variable 'opp_dir' referenced before assignment"
				return
		if clicked[0]:          # if clicked on cube, only rotate the clicked layer to given direction
			rectPos = (None, None)
			# get the coordinate of the clicked rect in the form of (0, 0), (1, 2)
			for rect in [self.f_RECTS, self.r_RECTS, self.u_RECTS]:
				for y in range(CUBENUM):
					for x in range(CUBENUM):
						if rect[x][y] == clicked[1]:
							rectPos = (x, y, rect)  # store the (x, y) coordinate of the clicked rectangle and the face where it lies.
							break           # break y's for-loop
					if rectPos != (None, None):
						break   # break x's for-loop if required rectangle found

			# distinguish the row and column of the selected cube
			column, row = rectPos[0], rectPos[1]
			if dir in ["Up", "Down"] and rectPos[2] != self.u_RECTS:        # up and down motion should not be accepted by the Up face.
				if dir == "Up":      # rotate the layer to upward by exchanging the colors from one face to other face up to it.
					if eventPos[0] > self.r_RECTS[0][0].left:      # if the layer to move lies on the right face
						self.rotateLayer(dir, column, row)        # the faces needs to be rotated and adjusted before swapping
						#  if the rotating layer is in edge, rotate the adjacent face too
						if column == 0:
							self.FRONT = self.rotateFace(self.FRONT, "AC", 1)
						elif column == CUBENUM-1:
							self.BACK = self.rotateFace(self.BACK, "AC", 1)
					elif eventPos[0] < self.r_RECTS[0][0].left:     # if the layer to move lies on the front face
						self.BACK[column].reverse()
						# ordinary swapping of faces
						self.FRONT[column], self.UP[column], self.BACK[column], self.DOWN[column] = \
							self.DOWN[column], self.FRONT[column], self.UP[column], self.BACK[column]
						self.BACK[column].reverse()

						if column == 0:
							self.LEFT = self.rotateFace(self.LEFT, "AC", 1)
						elif column == CUBENUM-1:
							self.RIGHT = self.rotateFace(self.RIGHT, "C", 1)
				elif dir == "Down":     # rotate the layer to upward by exchanging the colors from one face to other face down to it.
					if eventPos[0] > self.r_RECTS[0][0].left:      # if the layer to move lies on the right face
						self.rotateLayer(dir, column, row)
						if column == 0:
							self.FRONT = self.rotateFace(self.FRONT, "C", 1)
						elif column == CUBENUM-1:
							self.BACK = self.rotateFace(self.BACK, "C", 1)
					elif eventPos[0] < self.r_RECTS[0][0].left:     # if the layer to move lies on the front face
						self.BACK[column].reverse()
						self.FRONT[column], self.UP[column], self.BACK[column], self.DOWN[column] = \
							self.UP[column], self.BACK[column], self.DOWN[column], self.FRONT[column]
						self.BACK[column].reverse()

						if column == 0:
							self.LEFT = self.rotateFace(self.LEFT, "C", 1)
						elif column == CUBENUM-1:
							self.RIGHT = self.rotateFace(self.RIGHT, "AC", 1)
			if dir in ["Left", "Right"] and rectPos[2] != self.u_RECTS:
		        # rotate the layer right or left only if click over front or right faces' block
				# using the direction value, the required rotation is done through the rotateLayer function for both Left and Right directions
				self.rotateLayer(dir, column, row)
				if dir == "Left":
					if row == 0:
						self.DOWN = self.rotateFace(self.DOWN, "AC", 1)
					elif row == CUBENUM-1:
						self.UP = self.rotateFace(self.UP, "C", 1)
				elif dir == "Right":
					if row == 0:
						self.DOWN = self.rotateFace(self.DOWN, "C", 1)
					elif row == CUBENUM-1:
						self.UP = self.rotateFace(self.UP, "AC", 1)
		else:           # if not clicked on cube, rotate the whole cube to given direction

			if dir == "Right":
				for c in range(CUBENUM):
					self.BACK[c].reverse()
					self.RIGHT[c].reverse()
				self.FRONT, self.RIGHT, self.BACK, self.LEFT = \
					self.LEFT, self.FRONT, self.rotateFace(self.RIGHT, "C", 2), self.rotateFace(self.BACK, "C", 2)
				self.DOWN = self.rotateFace(self.DOWN, "C", 1)
				self.UP = self.rotateFace(self.UP, "AC", 1)
			elif dir == "Left":
				for c in range(CUBENUM):
					self.LEFT[c].reverse()
					self.BACK[c].reverse()
				self.FRONT, self.RIGHT, self.BACK, self.LEFT = \
					self.RIGHT, self.rotateFace(self.BACK, "C", 2), self.rotateFace(self.LEFT, "C", 2), self.FRONT
				self.DOWN = self.rotateFace(self.DOWN, "AC", 1)
				self.UP = self.rotateFace(self.UP, "C", 1)
			elif dir == "Up":
				columns = [str(i) for i in range(CUBENUM)]      #columns = all columns of the face. column = only the column of the selected block
				columns = "".join(columns)
				if eventPos[0] < self.r_RECTS[0][0].left:
					for c in range(CUBENUM):
						self.BACK[c].reverse()
						self.UP[c].reverse()
					self.FRONT, self.UP, self.BACK, self.DOWN = \
						self.DOWN, self.FRONT,self.UP, self.BACK
					self.RIGHT = self.rotateFace(self.RIGHT, "C", 1)
					self.LEFT = self.rotateFace(self.LEFT, "AC", 1)
				elif eventPos[0] > self.r_RECTS[0][0].left:
					self.rotateLayer(dir, columns, None)
					self.FRONT = self.rotateFace(self.FRONT, "AC", 1)
					self.BACK = self.rotateFace(self.BACK, "AC", 1)
			elif dir == "Down":
				columns = [str(i) for i in range(CUBENUM)]
				columns = "".join(columns)
				if eventPos[0] < self.r_RECTS[0][0].left:
					for c in range(CUBENUM):
						self.BACK[c].reverse()
					self.FRONT, self.UP, self.BACK, self.DOWN =  \
						self.UP, self.BACK, self.DOWN, self.FRONT
					self.BACK = self.reverseColumns(self.BACK, columns)
					self.RIGHT = self.rotateFace(self.RIGHT, "AC", 1)
					self.LEFT = self.rotateFace(self.LEFT, "C", 1)
				elif eventPos[0] > self.r_RECTS[0][0].left:
					self.rotateLayer(dir, columns, None)
					self.FRONT = self.rotateFace(self.FRONT, "C", 1)
					self.BACK = self.rotateFace(self.BACK, "C", 1)

	def reverseColumns(self, face, columns):
		dupe_face = copy.deepcopy(face)
		for i in columns:
			i = int(i)
			for y in range(CUBENUM):
				dupe_face[i][y] = face[i][CUBENUM-1-y]
		return dupe_face

	def shuffleCube(self):
		frequency = random.randint(40, 70)       # number of times to rotate the cube while suffling
		all_dir = ["Left", "Right", "Up", "Down"]
		for i in range(frequency):
			dir = random.choice(all_dir)            # randomly choose a direction
			x, y = random.randint(self.f_RECTS[0][0].left - 10, self.r_RECTS[CUBENUM-1][CUBENUM-1].right +10), \
			       random.randint(self.u_RECTS[0][CUBENUM-1].top - 10, self.r_RECTS[0][0].bottom+10)             # random coordinate around the main cube
			clicked = onCube(x, y)      # determine if the coordinate lies on the cube
			self.rotateCube(clicked, dir, (x, y), 0, False)       # rotate the whole cube if coordinate outside the cube, else rotate the given layer only

def calculateDistance(x, y, point):         # a function that return the distance between (x, y) and given point
	return pygame.math.Vector2(x, y).distance_to(point)

def onCube(x, y):               # tells if the cursor is on the cube. If it is, it returns information required to highlight the cube
	# RECTS = cube.f_RECTS or cube.r_RECTS or cube.u_RECTS. list (inside RECTS) = [rect1, rect2, rect3] or [rect4. rect5, rect6] or [rect7, rect8, rect9]
	# then r = rect1 or rect2. . . . . or rect9
	# rects holds the rectangles with which the cursor is colliding
	rects = [r for RECTS in [cube.f_RECTS, cube.r_RECTS, cube.u_RECTS] for list in RECTS for r in list if r.collidepoint(x, y)]     # information about this long list comprehension is given above
	# centers then stores the center values of rectangles in the rects list
	centers = [r.center for r in rects]
	# distances stores the distance of cursor from each center in centers list
	distances = [calculateDistance(x, y, c) for c in centers]
	# if cursor collides with cube's rectangles
	if len(rects) != 0:
		if distances.count(min(distances)) == 1:
		# if two or more centers are not in equal distance from the cursor, return True and the rectangle with the nearest center to highlight
			return [True, rects[distances.index(min(distances))]]
	# if cursor is in equal distance to more than one center or if cursor doesn't collide with any of the rectangles, return False and None
	return [False, None]

def highlightCube(image, rect):         # Highlights the given rect with the given highlight image
	imageRect = image.get_rect()
	imageRect.center = rect.center
	mainSurface.blit(image, imageRect)

def showArrow(clicked, dir, eventPos):            # when a layer is rotated in the given direction, an arrow is drawn to show the direction of rotation
	arrowImg = None
	if clicked[0]:
		if dir in ["Up", "Down"]:
			for i in range(CUBENUM):
				if clicked[1] in cube.f_RECTS[i]:
					if dir =="Up":
						arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Up_front.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
					elif dir == "Down":
						arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Down_front.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
					arrowRect = arrowImg.get_rect()
					arrowRect.center = (clicked[1].centerx, cube.f_RECTS[i][CUBENUM-1].top)
				elif clicked[1] in cube.r_RECTS[i]:
					if dir == "Up":
						arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Up_right.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
					elif dir == "Down":
						arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Down_right.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
					arrowRect = arrowImg.get_rect()
					arrowRect.center = (clicked[1].centerx, cube.r_RECTS[i][CUBENUM-1].top+0.1*CUBESIZE)
		elif dir in ["Left", "Right"]:
			for i in range(CUBENUM):
				if clicked[1] in cube.f_RECTS[i]+cube.r_RECTS[i]:
					if dir == "Left":
						arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Left.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
					elif dir == "Right":
						arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Right.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
					arrowRect = arrowImg.get_rect()
					if clicked[1] in cube.f_RECTS[i]:
						arrowRect.center = cube.f_RECTS[CUBENUM-1][cube.f_RECTS[i].index(clicked[1])].midright
					elif clicked[1] in cube.r_RECTS[i]:
						arrowRect.center = cube.r_RECTS[0][cube.r_RECTS[i].index(clicked[1])].midleft
		if arrowImg != None:
			mainSurface.blit(arrowImg, arrowRect)
	else:
		if dir in ["Up", "Down"]:
			if eventPos[0] < cube.f_RECTS[CUBENUM-1][0].right:
				if dir =="Up":
					arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Up_front.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
				elif dir == "Down":
					arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Down_front.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
				arrowRect = arrowImg.get_rect()
				for i in range(CUBENUM):
					arrowRect.center = cube.f_RECTS[i][CUBENUM-1].midtop
					mainSurface.blit(arrowImg, arrowRect)
			elif eventPos[0] > cube.f_RECTS[CUBENUM-1][0].right:
				if dir == "Up":
					arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Up_right.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
				elif dir == "Down":
					arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Down_right.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
				arrowRect = arrowImg.get_rect()
				for i in range(CUBENUM):
					arrowRect.center = (cube.r_RECTS[i][CUBENUM-1].centerx, cube.r_RECTS[i][CUBENUM-1].top + 0.1*CUBESIZE)
					mainSurface.blit(arrowImg, arrowRect)
		elif dir in ["Left", "Right"]:
			if dir == "Left":
				arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Left.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
			elif dir == "Right":
				arrowImg = pygame.transform.scale(pygame.image.load("Images/Arrows/Right.png"), (round(CUBESIZE/2), round(CUBESIZE/2)))
			arrowRect = arrowImg.get_rect()
			for i in range(CUBENUM):
				arrowRect.center = cube.f_RECTS[CUBENUM-1][i].midright
				mainSurface.blit(arrowImg, arrowRect)
	pygame.display.update()
	pygame.time.wait(200)

def getDir(p1, p2):
	# analyzes user's horizontal and vertical movement and returns direction according
	# to which type of movement was more
	horizontalMove = p2[0] - p1[0]
	verticalMove = p2[1] - p1[1]
	if abs(horizontalMove) > abs(verticalMove) and abs(horizontalMove) >= CUBESIZE/4:         # if cursor moved more horizontally (atleast the quater of cubesize)
		if horizontalMove < 0:          # when cursor moves left, horizontalMove's value becomes negative
			return "Left"
		else:                       # if positive, cursor moved right
			return "Right"
	elif abs(horizontalMove) < abs(verticalMove) and abs(verticalMove) >= CUBESIZE/4:           # if cursor moved more vertically (atleast the quater of cubesize)
		if verticalMove < 0:            # when cursor moves up, verticalMove's value is negative
			return "Up"
		else:               # if positive, cursor moved down
			return "Down"

def writeText(text, textcolor, size, pos_hint,  returnTextInfo):        # writes the given text in given size in the given position on the screen
	# pos_hint = (n, n) which is the center of the text and here 0 <= n <= 1. It kinda tell the position of center of text in relative of the window
	# if the pos_hint is given pixel coordinates greater than 1, it is processed as pixel corrdinates of the text's topleft corner.
	font = pygame.font.SysFont("Comic Sans MS", size, True)
	textObj = font.render(text, True, textcolor)
	textRect = textObj.get_rect()
	if 0 <= pos_hint[0] <= 1:
		textRect.centerx = pos_hint[0]*WINW
	else:
		textRect.left = pos_hint[0]
	if 0 <= pos_hint[1] <= 1:
		textRect.centery = pos_hint[1]*WINH
	else:
		textRect.top = pos_hint[1]
	if returnTextInfo:
		return textObj, textRect
	mainSurface.blit(textObj, textRect)

def buttonMoveAnimation(obj, rect, rectColor, dir):            # animates the given button by moving it right or left
	speed = 5
	if dir == "Left":
		while rect.right > 0:
			rect.left -= speed
			pygame.draw.rect(mainSurface, rectColor, pygame.Rect(rect.left-5, rect.top-2, rect.width+10, rect.height+4))
			mainSurface.blit(obj, rect)
			pygame.display.update()
			pygame.time.wait(20)
	if dir == "Right":
		while rect.left < WINW:
			rect.left += speed
			pygame.draw.rect(mainSurface, rectColor, pygame.Rect(rect.left-5, rect.top-2, rect.width+10, rect.height+4))
			mainSurface.blit(obj, rect)
			pygame.display.update()
			pygame.time.wait(20)

def showTime(time):
	minute, second = divmod(int(time), 60)
	hour = 0
	if minute >= 60:
		hour, minute = divmod(minute, 60)
	secObj, secRect = writeText(str(second), TEXTCOLOR, 30, (0.5, 0.1), True)
	minObj, minRect = writeText(str(minute), TEXTCOLOR, 30, (0.5, 0.1), True)
	hourObj, hourRect = writeText(str(hour), TEXTCOLOR, 30, (0.5, 0.1), True)
	minRect.midtop = (WINW/2, 15)
	if second < 10:
		secRect.topleft = (minRect.right+25, 15)
	else:
		secRect.topleft = (minRect.right+17, 15)
	if minute < 10:
		hourRect.topright = (minRect.left-25, 15)
	else:
		hourRect.topright = (minRect.left-20, 15)
	clockSize = (140, 70)
	clockImg = pygame.transform.scale(pygame.image.load("Images/Clock.png"), clockSize)
	clockRect = clockImg.get_rect()
	clockRect.center = minRect.center
	#pygame.draw.rect(mainSurface, BGCOLOR, pygame.Rect(hourRect.left, 10, secRect.right-hourRect.left, secRect.height))
	for obj, rect in [[clockImg, clockRect], [secObj, secRect], [minObj, minRect], [hourObj, hourRect]]:
		mainSurface.blit(obj, rect)

def instructions(pos_hint):
	pygame.event.clear()
	while True:
		mainSurface.fill(BGCOLOR)
		writeText("Instructions", TEXTCOLOR, 50, (0.5, 0.1), False)
		writeText("There are three cubes. The big cube shows the front, right and up faces and", BLACK, 15, (15, 100), False)
		writeText("the one on the top right corner of the screen shows the back, down", BLACK, 15, (15, 115), False)
		writeText("and right faces and the one on the top left corner shows the back, down ", BLACK, 15, (15, 130), False)
		writeText("and left faces. Click and drag the cursor to rotate the cube.", BLACK, 15, (15, 145), False)
		writeText("NOTE: Only the main cube takes the rotation instructions.", pygame.Color("red"), 15, (15, 160), False)
		writeText("To rotate the layer, click on the layer & drag.", BLACK, 15, (15, 175), False)
		writeText("To rotate the whole cube, click outside the cube & drag.", BLACK, 15, (15, 190), False)
		writeText("You can pause/resume the game by clicking on the game status at bottom.", pygame.Color("blue"), 15, (15, 205), False)
		writeText("Press 'Backspace' to get back to the start page.", BLACK, 15, (15, 220), False)
		writeText("Press 'Space' to undo the previous move (max 10 moves).", BLACK, 15, (15, 235), False)
		writeText("Press 'L' to load saved data & 'S' to save your cube.", BLACK, 15, (15, 250), False)

		backObj, backRect = writeText("Back", pygame.Color("white"), 30, (0.07, 0.7), True)
		pygame.draw.rect(mainSurface, pygame.Color("red"), pygame.Rect(0, backRect.top-2, backRect.width+20, backRect.height+4))
		mainSurface.blit(backObj, backRect)
		pygame.draw.rect(mainSurface, pygame.Color("green"), pygame.Rect(WINW-(backRect.width+30), backRect.top-2, backRect.width+30, backRect.height+4))
		writeText("Start", pygame.Color("white"), 30, (0.92, 0.7), False)
		taskObj, taskRect = writeText("Task", pygame.Color("white"), 30, pos_hint, True)
		pygame.draw.rect(mainSurface, BLACK, pygame.Rect(taskRect.left-5, taskRect.top-2, taskRect.width+10, taskRect.height+4))
		mainSurface.blit(taskObj, taskRect)
		pygame.display.update()

		event = pygame.event.wait()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			if taskRect.collidepoint(event.pos):
				initialPos = event.pos
			else:
				initialPos = (None, None)
		if event.type == MOUSEMOTION:
			try:
				if initialPos != (None, None):
					pos_hint[0] = event.pos[0]/WINW
			except:
				pass
		if event.type == MOUSEBUTTONUP:
			finalPos = event.pos
			if initialPos != (None, None) and initialPos != finalPos:
				dir = getDir(initialPos, finalPos)
				buttonMoveAnimation(taskObj, taskRect, BLACK, dir)
				pos_hint[0] = 0.5
				if dir == "Right":
					cube = makeNewCube()
					return True, True
				elif dir == "Left":
					return False, False
			initialPos = (None, None)

def undoCube(time, clockRunning, pauseObj, pauseRect):             # undo the last move
	if cube.pre_moves != []:
		if not clockRunning:
			buttonMoveAnimation(pauseObj, pauseRect, pygame.Color("red"), "Left")
		cube.rotateCube(cube.pre_moves[-1][0], cube.pre_moves[-1][1], cube.pre_moves[-1][2], time, False)
		showArrow(cube.pre_moves[-1][0], cube.pre_moves[-1][1], cube.pre_moves[-1][2])
		cube.pre_moves.remove(cube.pre_moves[-1])           # remove the move being undone

def textBox(text, size, color, pos_hint):        # draw a textbox with the given text written
	textObj, textRect = writeText(text, color, size, pos_hint, True)
	if text.isdigit() or text == "":
		textRect.width = 20
		textRect.center = (pos_hint[0]*WINW, pos_hint[1]*WINH)
	pygame.draw.rect(mainSurface, pygame.Color("white"), pygame.Rect(textRect.left-2, textRect.top-2, textRect.width+4, textRect.height+4))
	mainSurface.blit(textObj, textRect)
	return textRect

def cubeSolved():            # check if all faces of the cube is solved
	solvedFaces = 0         # stores how many cubes are solved
	for face in [cube.FRONT, cube.RIGHT, cube.BACK, cube.LEFT, cube.UP, cube.DOWN]:
		color_to_check = face[0][0]         # retrives the color in the start of the face & later checks if the face has only this color in it
		for x in range(CUBENUM):
			for y in range(CUBENUM):
				if face[x][y] == color_to_check:
					continue
				return False        # return false if there are other colors in the face
		# the program reaches here only if the previous face had only one color in it
		solvedFaces += 1        # so update the number of faces solved
	if solvedFaces == 6:        # if all faces solved
		return True

def save_load(mode, time):            # saves or loads the game progress
	global cube, CUBENUM
	if mode == "save":              # save the game's current time and all the colors at each face
		with open("saveData.txt", "w") as file:
			cube_colors = str(time)
			for face in [cube.FRONT, cube.RIGHT, cube.BACK, cube.LEFT, cube.UP, cube.DOWN]:
				face_colors = ""            # Stores the color data of the given face
				for column in range(CUBENUM):
					for row in range(CUBENUM):
						face_colors += face[column][row] + " "
				cube_colors += "\n%s" % face_colors
			file.write(cube_colors)
	elif mode == "load":
		cubenum = 0         # store what type of cube was saved i.e 2*2*2 or 3*3*3 or other. Defaults to 0
		if os.path.isfile("saveData.txt"):
			with open("saveData.txt") as file:
				data = file.readlines()
				t = data[0].strip("\n")     # remove the "\n" string from the end
				data.remove(data[0])       # remove the time info from the data
				data = [line.split() for line in data]  # convert data from ["a b c d" "1 2 3 4"] format to [["a", "b", "c", "d"], ["1", "2", "3", "4"]]
				# check if the data from the saveData.txt is corrupted or invalid
				l = [len(item) for item in data]
				if l.count(l[0]) != 6:      # if all the items don't have same number of items
					return [False, "Inconsistent number of items."]         # return the data was not loaded along with the reason
				cubenum = int(pow(l[0], 0.5))
				if cubenum != pow(l[0], 0.5):       # if the number of items in each face is not a perfect square
					return [False, "Faces are rectangular, not square."]
				CUBENUM = cubenum
				dupe_cube = makeNewCube()
				ALLFACE = [dupe_cube.FRONT, dupe_cube.RIGHT, dupe_cube.BACK, dupe_cube.LEFT, dupe_cube.UP, dupe_cube.DOWN]
				for i in range(len(ALLFACE)):
					for x in range(cubenum):
						ALLFACE[i][x] = data[i][x*cubenum:(x+1)*cubenum]
				return [True, dupe_cube, eval(t)]     # return True to tell data was loaded successfully.
		else:           # if file doesn't exist, return False
			return [False, "File not found."]
		pass

def main():
	global cube, CUBENUM, TOPLEFT, TOPRIGHT, MID, CUBESIZE, sizeRatio
	solvingCube = clockRunning = False             # tells the current status of the program & clock.
	HIGHLIGHT = clickedOnCube = SELECTED = [False, None]          # 1) Highlight given rectangle if True. 2) Check on which block the mouse was clicked
	taskPos_Hint = [0.5, 0.7]
	input_CUBENUM = "Write here the number of cubes you want in each column"
	while True:
		mainSurface.fill(BGCOLOR)
		# codes for texts on the screen
		writeText("Rubik Cube", TEXTCOLOR, 50, (0.5, 0.1), False)
		writeText("Drag to choose.", TEXTCOLOR, 18, (0.5, 0.62), False)
		instObj, instRect = writeText("Instruction", pygame.Color("grey"), 30, (0.15, 0.7), True)
		pygame.draw.rect(mainSurface, pygame.Color("yellow"), pygame.Rect(0, instRect.top-2, instRect.width+20, instRect.height+4))
		mainSurface.blit(instObj, instRect)
		pygame.draw.rect(mainSurface, pygame.Color("green"), pygame.Rect(WINW-(instRect.width), instRect.top-2, instRect.width, instRect.height+4))
		writeText("Start", pygame.Color("white"), 30, (0.88, 0.7), False)
		taskObj, taskRect = writeText("Task", pygame.Color("white"), 30, taskPos_Hint, True)
		pygame.draw.rect(mainSurface, BLACK, pygame.Rect(taskRect.left-5, taskRect.top-2, taskRect.width+10, taskRect.height+4))
		mainSurface.blit(taskObj, taskRect)
		writeText("Press 'L' to load your saved game.", TEXTCOLOR, 18, (0.5, 0.48), False)
		userCUBENUM = textBox(input_CUBENUM, 20, BLACK, (0.5, 0.55))
		if SELECTED[0]:
			pygame.draw.line(mainSurface, pygame.Color("red"), (userCUBENUM.bottomleft), (userCUBENUM.bottomright), 2)
		pygame.display.update()
		# event handling
		event = pygame.event.wait()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			if userCUBENUM.collidepoint(event.pos) and not SELECTED[0]:
				if input_CUBENUM == "Write here the number of cubes you want in each column":
					input_CUBENUM = ""
				SELECTED = [True, userCUBENUM]
			else:
				SELECTED = [False, None]
				if input_CUBENUM == "":
					input_CUBENUM = "Write here the number of cubes you want in each column"
			if taskRect.collidepoint(event.pos):
				initialPos = event.pos
			else:
				initialPos = (None, None)
		if event.type == MOUSEMOTION:
			try:
				if initialPos != (None, None):
					taskPos_Hint[0] = event.pos[0]/WINW
			except:
				pass
		if event.type == MOUSEBUTTONUP:
			finalPos = event.pos
			if initialPos != (None, None) and initialPos != finalPos:
				dir = getDir(initialPos, finalPos)
				buttonMoveAnimation(taskObj, taskRect, BLACK, dir)
				taskPos_Hint[0] = 0.5
				if dir == "Right":
					if input_CUBENUM in ("1 2 3 4 5").split():
						CUBENUM = int(input_CUBENUM)
					else:
						CUBENUM = 3
					cube = makeNewCube()
					solvingCube = True
					firstRun = True
					time = 0
				elif dir == "Left":
					solvingCube, firstRun = instructions(taskPos_Hint)
					if solvingCube:
						if input_CUBENUM in ("1 2 3 4 5").split():
							CUBENUM = int(input_CUBENUM)
						cube = makeNewCube()
						time = 0
			initialPos = (None, None)
		if event.type == KEYDOWN:
			if event.key == ord("l"):
				cube = makeNewCube()
				load = save_load("load", 0)
				if load[0]:
					writeText("Cube loaded!", TEXTCOLOR, 24, (0.5, 0.42), False)
					pygame.display.update()
					pygame.time.wait(300)
					cube = load[1]
					solvingCube = True
					firstRun = False
					time = load[2]
				else:
					writeText("File corrupted: "+load[1], pygame.Color("red"), 20, (0.5, 0.42), False)
					pygame.display.update()
					pygame.time.wait(400)
			if SELECTED[0]:
				if chr(event.key) in ("1 2 3 4 5").split():
					input_CUBENUM = chr(event.key)
				if event.key == K_BACKSPACE:
					input_CUBENUM = input_CUBENUM[:-1]
		# start page ends and game starts
		while solvingCube:
			if CUBENUM > 4:
				CUBESIZE = 60
				sizeRatio = 0.4
				# constants for positions of cubes
				TOPRIGHT = (WINW - CUBESIZE*((CUBENUM+1)*sizeRatio), CUBENUM*round(sizeRatio*153*CUBESIZE/226, 2))
				TOPLEFT = (CUBESIZE*0.65*((CUBENUM)*sizeRatio), CUBENUM*round(sizeRatio*153*CUBESIZE/226, 2))
				MID = ((WINW-CUBENUM*CUBESIZE)/2, (CUBENUM)*1.2*CUBESIZE)
			else:
				CUBESIZE = 100
				sizeRatio = 0.3
				# constants for positions of cubes
				TOPRIGHT = (WINW - CUBESIZE*(CUBENUM/2.5), CUBENUM*round(sizeRatio*153*CUBESIZE/226, 2))
				TOPLEFT = (CUBESIZE*(CUBENUM/5), CUBENUM*round(sizeRatio*153*CUBESIZE/226, 2))
				MID = ((WINW-CUBENUM*CUBESIZE)/2, (CUBENUM+0.5)*CUBESIZE)
			mainSurface.fill(BGCOLOR)
			cube.drawCube(["back", "right", "down"], firstRun, TOPRIGHT, sizeRatio)
			cube.drawCube(["back", "left", "down"], firstRun, TOPLEFT, sizeRatio)
			cube.drawCube(["front", "right", "up"], firstRun, MID, 1)
			firstRun= EVENT = False
			showTime(time)
			allSolved = cubeSolved()
			# show status of the game
			if not allSolved:
				if clockRunning:
					time += 1/FPS
					runningObj, runningRect = writeText("Running!", pygame.Color("white"), 30, (0.5, 0.95), True)
					runningRect.top = WINH-(runningRect.height+4)
					pygame.draw.rect(mainSurface, pygame.Color("blue"), (0, runningRect.top-2, WINW, runningRect.height+4))
					mainSurface.blit(runningObj, runningRect)
				else:
					pauseObj, pauseRect = writeText("Paused!", pygame.Color("white"), 30, (0.5, 0.95), True)
					pauseRect.top = WINH-(pauseRect.height+4)
					pygame.draw.rect(mainSurface, pygame.Color("red"), (0, pauseRect.top-2, WINW, pauseRect.height+4))
					mainSurface.blit(pauseObj, pauseRect)
				# highlighting the cube
				if HIGHLIGHT[0]:                # if HIGHLIGHT[0] set to True
					for i in range(CUBENUM):
						if HIGHLIGHT[1] in cube.f_RECTS[i]:             # if the rectanlge to highlight is in FRONT face
							hImg = pygame.transform.scale(pygame.image.load("Images/Front/Highlight.png"), (round(76*CUBESIZE/113), round(153*CUBESIZE/226)))
							break       # break the for loop
						elif HIGHLIGHT[1] in cube.r_RECTS[i]:           # if the rectanlge to highlight is in RIGHT face
							hImg = pygame.transform.scale(pygame.image.load("Images/Sides/Highlight.png"), (round(42*CUBESIZE/113), round(177*CUBESIZE/226)))
							break
						elif HIGHLIGHT[1] in cube.u_RECTS[i]:           # if the rectanlge to highlight is in UP face
							hImg = pygame.transform.scale(pygame.image.load("Images/Up/Highlight.png"), (round(1.06*CUBESIZE), round(73*CUBESIZE/226)))
							break
					highlightCube(hImg, HIGHLIGHT[1])       # highlight the rect at HIGHLIGHT[1] using the hImg image
			else:           # if game solved
				solveObj, solveRect = writeText("Congrats!", pygame.Color("white"), 30, (0.5, 0.95), True)
				solveRect.top = WINH-(solveRect.height+4)
				pygame.draw.rect(mainSurface, pygame.Color("green"), (0, solveRect.top-2, WINW, solveRect.height+4))
				mainSurface.blit(solveObj, solveRect)
			# event handling
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYUP:
					if event.key == K_BACKSPACE:
						solvingCube = False
						break           # break the for event loop without checking other events
					elif event.key == K_SPACE:
						if not allSolved:
							undoCube(time, clockRunning, pauseObj, pauseRect)
							clockRunning = True
							break
					elif event.key == K_s:
						if not allSolved:
							save_load("save", time)
				if not allSolved:
					if event.type == MOUSEMOTION:
						mx, my = event.pos
						HIGHLIGHT = onCube(mx, my)
						if HIGHLIGHT[0]:
							break
					if event.type == MOUSEBUTTONDOWN:
						initialPos = event.pos
						if not clockRunning:
							if pygame.Rect(0, pauseRect.top-2, WINW, pauseRect.height+4).collidepoint(initialPos):
								buttonMoveAnimation(pauseObj, pauseRect, pygame.Color("red"), "Left")
								clockRunning = True
								initialPos = (None, None)
								break
						else:
							if pygame.Rect(0, runningRect.top-2, WINW, runningRect.height+4).collidepoint(initialPos):
								buttonMoveAnimation(runningObj, runningRect, pygame.Color("blue"), "Right")
								clockRunning = False
								initialPos = (None, None)
								break
						clickedOnCube = onCube(event.pos[0], event.pos[1])
					if event.type == MOUSEBUTTONUP:
						finalPos = event.pos
						if initialPos != (None, None) and initialPos != finalPos:
							if not clockRunning:
								buttonMoveAnimation(pauseObj, pauseRect, pygame.Color("red"), "Left")
								clockRunning = True
							dir = getDir(initialPos, finalPos)
							cube.rotateCube(clickedOnCube, dir, initialPos, time, True)
							showArrow(clickedOnCube, dir, initialPos)
						initialPos = (None, None)
			pygame.display.update()
			clock.tick(FPS)

if __name__ == "__main__":
	main()
