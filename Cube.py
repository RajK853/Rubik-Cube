import pygame
from pygame.locals import *
import random
import sys
import copy

pygame.init()

# game constants
CUBESIZE = 100           # size of small cube. Keep it at least 50. Recommended to keep it a multiple of 10.
CUBENUM = 3            # set if the cube is a 2*2*2, 3*3*3, 4*4*4 or n*n*n type cube.

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

	def drawFace(self, face, firstRun):    #draws the given face
		# codes below draw the Front, Right and Up faces which make the main Cube
		if face == "front":
			# I determined the ratio of height and width of each block in each face by doing calculations & experiments
			# So don't change anything with the size and other variables
			size = (round(76*CUBESIZE/113), round(153*CUBESIZE/226))
			# In original size, each block image needs to be shifted 24 pixel down from previous cube.
			# So here the each block will be shifted according to the image dimension
			YSHIFT = round(CUBESIZE*25/226, 2)         # tells how much pixel show each block be shifted down
			x = 0.1*WINW                    #starting x-coordinate pixel position of the cube
			y = WINH - 2*round(153*CUBESIZE/226, 2)
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
						pygame.time.wait(50)
		if face == "right":
			YSHIFT = round(CUBESIZE*50/226, 2)       # in full size, the lefttop of the block is 46 pixel below the lefttop of the image
			x = 0.1*WINW + CUBENUM*round(75*CUBESIZE/113, 2)
			y = WINH - 2*round(153*CUBESIZE/226, 2) + CUBENUM*round(CUBESIZE*24/226, 2) - YSHIFT
			size = (round(43*CUBESIZE/113), round(177*CUBESIZE/226))
			for i in range(len(self.RIGHT)):
				for j in range(len(self.RIGHT[i])):
					cubeColor = self.RIGHT[i][j]
					cubeImg = pygame.transform.scale(pygame.image.load("Images/Sides/%s.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x+i*size[0], y-j*size[1]+(j-i)*YSHIFT)
					self.r_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(50)
		if face == "up":
			YSHIFT1 = round(CUBESIZE*25/226, 2)
			YSHIFT2 = round(CUBESIZE*46/226, 2)
			XSHIFT = round(CUBESIZE*89/226, 2)
			x = 0.1*WINW
			y = WINH - (CUBENUM+1)*round(153*CUBESIZE/226, 2) - YSHIFT2 + (CUBENUM-1)*round(CUBESIZE*24/226, 2)
			size = (round(1.06*CUBESIZE), round(73*CUBESIZE/226))
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
						pygame.time.wait(50)

		# codes below draw a small cube (size: 25% of main cube) showing Back, Left and Down faces
		if face == "back":
			# same as for Front face but this is one has smaller dimension i.e 0.25 of front face
			size = (round(0.3*76*CUBESIZE/113), round(0.3*153*CUBESIZE/226))
			YSHIFT = round(0.3*CUBESIZE*27/226, 2)
			x = WINW - CUBESIZE*(CUBENUM/2.5)
			y = CUBENUM*round(0.3*153*CUBESIZE/226, 2)
			for i in range(len(self.BACK)):
				for j in range(len(self.BACK[i])):
					cubeColor = self.BACK[i][j]
					cubeImg = pygame.transform.scale(pygame.image.load("Images/Front/%s_reverse.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x+i*size[0], y-j*size[1]+(j-i)*YSHIFT)
					#cube.b_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(50)
		if face == "left":
			# same as of Right face but smaller
			YSHIFT = round(0.3*CUBESIZE*46/226, 2)
			x = WINW - CUBESIZE*(CUBENUM/2.5) + CUBENUM*round(0.3*76*CUBESIZE/113, 2)
			y = CUBENUM*(round(0.3*153*CUBESIZE/226, 2)) - (CUBENUM-1)*round(0.3*CUBESIZE*27/226, 2)
			size = (round(0.3*42*CUBESIZE/113), round(0.3*175*CUBESIZE/226))
			for i in range(len(self.LEFT)):
				for j in range(len(self.LEFT[i])):
					cubeColor = self.LEFT[i][j]
					cubeImg = pygame.transform.scale(pygame.image.load("Images/Sides/%s_reverse.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x+i*size[0], y-j*size[1]+(i+j)*YSHIFT)
					#cube.l_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(50)
		if face == "down":
			# same as of Up face but smaller
			YSHIFT1 = round(0.3*CUBESIZE*23/226, 2)
			YSHIFT2 = round(0.3*CUBESIZE*45/226, 2)
			XSHIFT1 = round(0.3*CUBESIZE*81/226, 2)
			XSHIFT2 = round(0.3*CUBESIZE*84/226, 2)
			x = WINW - CUBESIZE*(CUBENUM/2.5)
			y = (CUBENUM+1)*round(0.3*145*CUBESIZE/226, 2)
			size = (round(0.31*CUBESIZE), round(0.3*72*CUBESIZE/226))
			for i in range(len(self.DOWN)):
				for j in range(len(self.DOWN[i])):
					cubeColor = self.DOWN[i][j]
					cubeImg = pygame.transform.scale(pygame.image.load("Images/Up/%s_reverse.png" % cubeColor), size)
					cubeRect = cubeImg.get_rect()
					cubeRect.topleft = (x+i*(size[0]-XSHIFT1)+j*XSHIFT2, y-i*YSHIFT1+j*YSHIFT2)
					#cube.d_RECTS[i][j] = cubeRect
					mainSurface.blit(cubeImg, cubeRect)
					if firstRun:
						pygame.display.update()
						pygame.time.wait(50)

	def drawCube(self, firstRun):
		# draw front, (right/left) and (top/down) faces.
		for face in ["front", "right", "up", "back", "left", "down"]:
			self.drawFace(face, firstRun)
		if firstRun:
			self.shuffleCube()
			pass

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
								dupeFace[x][CUBENUM-1-y] = face[y][CUBENUM-1-x]
							elif dupeFace == dupe_down:
								dupeFace[y][CUBENUM-1-x] = face[CUBENUM-1-x][y]
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
								dupeFace[CUBENUM-1-x][y] = face[y][CUBENUM-1-x]
							elif dupeFace == dupe_down:
								dupeFace[y][CUBENUM-1-x] = face[x][CUBENUM-1-y]

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
					hFaces[i][x][row] =hFaces[i+1][x][row]
			self.FRONT, self.RIGHT, self.BACK, self.LEFT = [hFaces[i] for i in range(0, len(hFaces), 2)]

	def rotateFace(self, face, direction):      # when layers at edges are rotated horizontally or vertically, face adjacent to that layer also needs to rotate
		# rotateFace is different from rotateLayer function. This function rotates the colors within the same face in a clockwise or anti-clockwise direction
		dupe_face = copy.deepcopy(face)  # make a copy of the required face
		for x in range(CUBENUM):
			for y in range(CUBENUM):
				if direction == "C":            # for clockwise rotation
					dupe_face[y][CUBENUM-1-x] = face[x][y]
				elif direction == "AC":        # for anticlockwise rotation
					dupe_face[CUBENUM-1-y][x] = face[x][y]
		return dupe_face

	def rotateCube(self, clicked, dir, eventPos):
		if clicked[0]:          # if clicked on cube, only rotate the clicked layer to given direction
			print("Rotate layer to %s" % dir)
			rectPos = (None, None)
			# get the coordinate of the clicked rect in the form of (0, 0), (1, 2)
			for rect in [self.f_RECTS, self.r_RECTS, self.u_RECTS]:
				for y in range(CUBENUM):
					for x in range(CUBENUM):
						if rect[x][y] == clicked[1]:
							rectPos = (x, y)
							break           # break y's for-loop
					if rectPos != (None, None):
						break   # break x's for-loop if required rectangle found
			print("(x, y) : (%s, %s)" % (rectPos[0], rectPos[1]))
			# distinguish the row and column of the selected cube
			column, row = rectPos
			if dir in ["Up", "Down"]:
				if dir == "Up":      # rotate the layer to upward by exchanging the colors from one face to other face up to it.
					if eventPos[0] > self.r_RECTS[0][0].left:      # if the layer to move lies on the right face
						self.rotateLayer(dir, column, row)        # the faces needs to be rotated and adjusted before swapping
						#  if the rotating layer is in edge, rotate the adjacent face too
						if column == 0:
							self.FRONT = self.rotateFace(self.FRONT, "AC")
						elif column == CUBENUM-1:
							self.BACK = self.rotateFace(self.BACK, "C")
					elif eventPos[0] < self.r_RECTS[0][0].left:     # if the layer to move lies on the front face
						self.BACK[column].reverse()
						# ordinary swapping of faces
						self.FRONT[column], self.UP[column], self.BACK[column], self.DOWN[column] = \
							self.DOWN[column], self.FRONT[column], self.UP[column], self.BACK[column]
						self.BACK[column].reverse()

						if column == 0:
							self.LEFT = self.rotateFace(self.LEFT, "AC")
						elif column == CUBENUM-1:
							self.RIGHT = self.rotateFace(self.RIGHT, "C")
				elif dir == "Down":     # rotate the layer to upward by exchanging the colors from one face to other face down to it.
					if eventPos[0] > self.r_RECTS[0][0].left:      # if the layer to move lies on the right face
						self.rotateLayer(dir, column, row)

						if column == 0:
							self.FRONT = self.rotateFace(self.FRONT, "C")
						elif column == CUBENUM-1:
							self.BACK = self.rotateFace(self.BACK, "AC")
					elif eventPos[0] < self.r_RECTS[0][0].left:     # if the layer to move lies on the front face
						self.BACK[column].reverse()
						self.FRONT[column], self.UP[column], self.BACK[column], self.DOWN[column] = \
							self.UP[column], self.BACK[column], self.DOWN[column], self.FRONT[column]
						self.BACK[column].reverse()

						if column == 0:
							self.LEFT = self.rotateFace(self.LEFT, "C")
						elif column == CUBENUM-1:
							self.RIGHT = self.rotateFace(self.RIGHT, "AC")
			if dir in ["Left", "Right"]:
				for item in self.f_RECTS+self.r_RECTS:
					if clicked[1] in item:      # rotate the layer right or left only if click over front or right faces' block
						# using the direction value, the required rotation is done through the rotateLayer function for both Left and Right directions
						self.rotateLayer(dir, column, row)
						if dir == "Left":
							if row == 0:
								self.DOWN = self.rotateFace(self.DOWN, "AC")
							elif row == CUBENUM-1:
								self.UP = self.rotateFace(self.UP, "C")
						elif dir == "Right":
							if row == 0:
								self.DOWN = self.rotateFace(self.DOWN, "C")
							elif row == CUBENUM-1:
								self.UP = self.rotateFace(self.UP, "AC")
						break
		else:           # if not clicked on cube, rotate the whole cube to given direction
			print("Rotate the whole cube to %s" % dir)
			if dir == "Right":
				self.FRONT, self.RIGHT, self.BACK, self.LEFT = \
					self.LEFT, self.FRONT, self.RIGHT, self.BACK
				self.DOWN = self.rotateFace(self.DOWN, "C")
				self.UP = self.rotateFace(self.UP, "AC")
			elif dir == "Left":
				self.FRONT, self.RIGHT, self.BACK, self.LEFT = \
					self.RIGHT, self.BACK, self.LEFT, self.FRONT
				self.DOWN = self.rotateFace(self.DOWN, "AC")
				self.UP = self.rotateFace(self.UP, "C")
			elif dir == "Up":
				if eventPos[0] < self.r_RECTS[0][0].left:
					for c in range(CUBENUM):
						self.BACK[c].reverse()
					self.FRONT, self.UP, self.BACK, self.DOWN = \
						self.DOWN, self.FRONT, self.UP, self.BACK
					for c in range(CUBENUM):
						self.BACK[c].reverse()
					self.RIGHT = self.rotateFace(self.RIGHT, "C")
					self.LEFT = self.rotateFace(self.LEFT, "AC")
				elif eventPos[0] > self.r_RECTS[0][0].left:
					columns = [str(i) for i in range(CUBENUM)]      #columns = all columns of the face. column = only the column of the selected block
					columns = "".join(columns)
					self.rotateLayer(dir, columns, None)
					self.FRONT = self.rotateFace(self.FRONT, "AC")
					self.BACK = self.rotateFace(self.BACK, "C")
			elif dir == "Down":
				if eventPos[0] < self.r_RECTS[0][0].left:
					for c in range(CUBENUM):
						self.BACK[c].reverse()
					self.FRONT, self.UP, self.BACK, self.DOWN =  \
						self.UP, self.BACK, self.DOWN, self.FRONT
					for c in range(CUBENUM):
						self.BACK[c].reverse()
					self.RIGHT = self.rotateFace(self.RIGHT, "AC")
					self.LEFT = self.rotateFace(self.LEFT, "C")
				elif eventPos[0] > self.r_RECTS[0][0].left:
					columns = [str(i) for i in range(CUBENUM)]
					columns = "".join(columns)
					self.rotateLayer(dir, columns, None)
					self.FRONT = self.rotateFace(self.FRONT, "C")
					self.BACK = self.rotateFace(self.BACK, "AC")

	def shuffleCube(self):
		frequency = random.randint(10, 20)       # number of times to rotate the cube while suffling
		all_dir = ["Left", "Right", "Up", "Down"]
		for i in range(frequency):
			dir = random.choice(all_dir)            # randomly choose a direction
			x, y = random.randint(0, WINW), random.randint(2*WINH/3, WINH)             # random coordinate of the screen
			clicked = onCube(x, y)      # determine if the coordinate lies on the cube
			self.rotateCube(clicked, dir, (x, y))       # rotate the whole cube if coordinate outside the cube, else rotate the given layer only

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

def getDir(p1, p2):
	# analyzes user's horizontal and vertical movement and returns direction according
	# to which type of movement was more
	horizontalMove = p2[0] - p1[0]
	verticalMove = p2[1] - p1[1]
	if abs(horizontalMove) > abs(verticalMove):         # if cursor moved more horizontally
		if horizontalMove < 0:          # when cursor moves left, horizontalMove's value becomes negative
			return "Left"
		else:                       # if positive, cursor moved right
			return "Right"
	elif abs(horizontalMove) < abs(verticalMove):           # if cursor moved more vertically
		if verticalMove < 0:            # when cursor moves up, verticalMove's value is negative
			return "Up"
		else:               # if positive, cursor moved down
			return "Down"

def writeText(text, textcolor, rectcolor, size, pos_hint,  returnTextInfo):        # writes the given text in given size in the given position on the screen
	# pos_hint = (n, n) which is the center of the text and here 0 <= n <= 1. It kinda tell the position of center of text in relative of the window
	# if the pos_hint is given pixel coordinates greater than 1, it is processed as pixel corrdinates of the text's topleft corner.
	font = pygame.font.SysFont("Comic Sans MS", size, True)
	textObj = font.render(text, True, textcolor, rectcolor)
	textRect = textObj.get_rect()
	if 0 <= pos_hint[0] <= 1 and 0 <= pos_hint[1] <= 1:
		textRect.center = (pos_hint[0]*WINW, pos_hint[1]*WINH)
	else:
		textRect.topleft = (pos_hint[0], pos_hint[1])
	if returnTextInfo:
		return textObj, textRect
	mainSurface.blit(textObj, textRect)

def buttonMoveAnimation(obj, rect, dir):            # animates the given button by moving it right or left
	speed = 5
	if dir == "Left":
		while rect.right > 0:
			rect.left -= speed
			pygame.draw.rect(mainSurface, BLACK, pygame.Rect(rect.left-5, rect.top-2, rect.width+10, rect.height+4))
			mainSurface.blit(obj, rect)
			pygame.display.update()
			pygame.time.wait(20)
	if dir == "Right":
		while rect.left < WINW:
			rect.left += speed
			pygame.draw.rect(mainSurface, BLACK, pygame.Rect(rect.left-5, rect.top-2, rect.width+10, rect.height+4))
			mainSurface.blit(obj, rect)
			pygame.display.update()
			pygame.time.wait(20)

def instructions(pos_hint):
	pygame.event.clear()
	while True:
		mainSurface.fill(BGCOLOR)
		writeText("Instructions", TEXTCOLOR, None, 50, (0.5, 0.1), False)
		writeText("There are two cubes. The big cube shows the front, right and up faces and", BLACK, None, 15, (15, 100), False)
		writeText("the small cube on the top right corner of the screen shows the back, down", BLACK, None, 15, (15, 115), False)
		writeText("and left faces of the cube. Click and slide the cursor to rotate the cube.", BLACK, None, 15, (15, 130), False)
		writeText("NOTE: Only the main cube takes the rotation instructions.", pygame.Color("red"), None, 15, (15, 145), False)
		writeText("To rotate the layer, click on the layer & slide.", BLACK, None, 15, (15, 160), False)
		writeText("To rotate the whole cube, click outside the cube & slide.", BLACK, None, 15, (15, 175), False)
		writeText("Press 'Backspace' to get back to the start page.", BLACK, None, 15, (15, 190), False)

		backObj, backRect = writeText("Back", pygame.Color("white"), None, 30, (0.07, 0.7), True)
		pygame.draw.rect(mainSurface, pygame.Color("red"), pygame.Rect(0, backRect.top-2, backRect.width+20, backRect.height+4))
		mainSurface.blit(backObj, backRect)
		pygame.draw.rect(mainSurface, pygame.Color("green"), pygame.Rect(WINW-(backRect.width+30), backRect.top-2, backRect.width+30, backRect.height+4))
		writeText("Start", pygame.Color("white"), None, 30, (0.92, 0.7), False)
		taskObj, taskRect = writeText("Task", pygame.Color("white"), None, 30, pos_hint, True)
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
				buttonMoveAnimation(taskObj, taskRect, dir)
				pos_hint[0] = 0.5
				if dir == "Right":
					cube = makeNewCube()
					return True, True
				elif dir == "Left":
					return False, False
			initialPos = (None, None)

def main():
	global cube
	solvingCube = False             # tells the current status of the program
	HIGHLIGHT = clickedOnCube = [False, None]          # 1) Highlight given rectangle if True. 2) Check on which block the mouse was pressed
	taskPos_Hint = [0.5, 0.7]
	while True:
		mainSurface.fill(BGCOLOR)
		# codes for texts on the screen
		writeText("Rubik Cube", TEXTCOLOR, None, 50, (0.5, 0.1), False)
		writeText("Drag to choose.", TEXTCOLOR, None, 18, (0.5, 0.62), False)
		instObj, instRect = writeText("Instruction", pygame.Color("grey"), None, 30, (0.15, 0.7), True)
		pygame.draw.rect(mainSurface, pygame.Color("yellow"), pygame.Rect(0, instRect.top-2, instRect.width+20, instRect.height+4))
		mainSurface.blit(instObj, instRect)
		pygame.draw.rect(mainSurface, pygame.Color("green"), pygame.Rect(WINW-(instRect.width), instRect.top-2, instRect.width, instRect.height+4))
		writeText("Start", pygame.Color("white"), None, 30, (0.88, 0.7), False)
		taskObj, taskRect = writeText("Task", pygame.Color("white"), None, 30, taskPos_Hint, True)
		pygame.draw.rect(mainSurface, BLACK, pygame.Rect(taskRect.left-5, taskRect.top-2, taskRect.width+10, taskRect.height+4))
		mainSurface.blit(taskObj, taskRect)
		pygame.display.update()
		# event handling
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
					taskPos_Hint[0] = event.pos[0]/WINW
			except:
				pass
		if event.type == MOUSEBUTTONUP:
			finalPos = event.pos
			if initialPos != (None, None) and initialPos != finalPos:
				dir = getDir(initialPos, finalPos)
				buttonMoveAnimation(taskObj, taskRect, dir)
				taskPos_Hint[0] = 0.5
				if dir == "Right":
					cube = makeNewCube()
					solvingCube = True
					firstRun = True
				elif dir == "Left":
					solvingCube, firstRun = instructions(taskPos_Hint)
					if solvingCube:
						cube = makeNewCube()
			initialPos = (None, None)

		while solvingCube:
			EVENT = False
			mainSurface.fill(BGCOLOR)
			cube.drawCube(firstRun)
			firstRun = False
			# event handling
			while not EVENT:
				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
						sys.exit()
					if event.type == KEYUP:
						if event.key == K_BACKSPACE:
							solvingCube = False
							EVENT = True
							break
					if event.type == MOUSEMOTION:
						mx, my = event.pos
						HIGHLIGHT = onCube(mx, my)
						if HIGHLIGHT[0]:
							EVENT = True            # set the EVENT to True only if the cursor is over the cube
							break
					if event.type == MOUSEBUTTONDOWN:
						initialPos = event.pos
						clickedOnCube = onCube(event.pos[0], event.pos[1])
					if event.type == MOUSEBUTTONUP:
						finalPos = event.pos
						if initialPos != (None, None) and initialPos != finalPos:
							dir = getDir(initialPos, finalPos)
							cube.rotateCube(clickedOnCube, dir, initialPos)
							# directly use the direction from getDir function and don't store in dir
						EVENT = True
						initialPos = (None, None)
				# highlighting the cube
				if HIGHLIGHT[0]:                # if HIGHLIGHT[0] set to True
					for i in range(CUBENUM):
						if HIGHLIGHT[1] in cube.f_RECTS[i]:             # if the rectanlge to highlight is in FRONT face
							hImg = pygame.transform.scale(pygame.image.load("Images/Front/Highlight.png"), (round(76*CUBESIZE/113), round(153*CUBESIZE/226)))
							break
						elif HIGHLIGHT[1] in cube.r_RECTS[i]:           # if the rectanlge to highlight is in RIGHT face
							hImg = pygame.transform.scale(pygame.image.load("Images/Sides/Highlight.png"), (round(42*CUBESIZE/113), round(177*CUBESIZE/226)))
							break
						elif HIGHLIGHT[1] in cube.u_RECTS[i]:           # if the rectanlge to highlight is in UP face
							hImg = pygame.transform.scale(pygame.image.load("Images/Up/Highlight.png"), (round(1.06*CUBESIZE), round(73*CUBESIZE/226)))
							break
					highlightCube(hImg, HIGHLIGHT[1])
				pygame.display.update()

if __name__ == "__main__":
	main()
