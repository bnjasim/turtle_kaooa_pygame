from turtle import Turtle
import time
import math
import random

def find_intersection_point(p1, p2, p3, p4):
	"""
	find the point of intersection of two lines defined by l1=(p1,p2) and l2=(p3,p4)

	Args: 4 points in the (x, y) coordinates
	Returns: the point of intersection (x, y)

	Raises: ValueError if the lines are parallel
	"""
	x1, y1 = p1
	x2, y2 = p2
	x3, y3 = p3
	x4, y4 = p4

	# Calculate slopes
	if x2 - x1 != 0:
		m1 = (y2 - y1) / (x2 - x1)
	else:
		m1 = float('inf')  # Parallel to y-axis
	if x4 - x3 != 0:
		m2 = (y4 - y3) / (x4 - x3)
	else:
		m2 = float('inf')  # Parallel to y-axis

	# Check for parallel lines
	if m1 == m2:
		# Lines are parallel, no intersection
	    raise ValueError("Parallel lines has no point of intersection")

	# Calculate y-intercepts
	b1 = y1 - m1 * x1
	b2 = y3 - m2 * x3

	# Calculate intersection point
	if m1 != float('inf') and m2 != float('inf'):
		x_intersect = (b2 - b1) / (m1 - m2)
	elif m1 == float('inf'):  # Line 1 is parallel to y-axis
		x_intersect = x1
	else:  # Line 2 is parallel to y-axis
		x_intersect = x3
	    
	y_intersect = m1 * x_intersect + b1

	return x_intersect, y_intersect


def get_star_coordinates(side):
	"""
	Find the coordinates of all the 10 vertices of a star with center at (0,0)
	"""
	cos_18 = math.cos(math.radians(18))
	tan_18 = math.tan(math.radians(18))
	cos_36 = math.cos(math.radians(36))
	sin_36 = math.sin(math.radians(36))

	half_side = side/2
	h = half_side/cos_18
	r = half_side * tan_18
	a = h * cos_36
	b = h * sin_36

	# vertices
	v0 = (-half_side, r)
	v1 = (half_side, r)
	v2 = (-a, -b)
	v3 = (0, h)
	v4 = (a, -b)

	# find the inner vertices as the points of intersection of lines
	v5 = find_intersection_point(v1, v2, v0, v4)
	v6 = find_intersection_point(v2, v3, v0, v4)
	v7 = find_intersection_point(v0, v1, v2, v3)
	v8 = find_intersection_point(v0, v1, v3, v4)
	v9 = find_intersection_point(v1, v2, v3, v4)

	return [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9]


def euclidean_distance(p1, p2):
    """
    Calculate the Euclidean distance between two points in 2D space.

    Parameters:
    p1 (tuple): Coordinates of the first point (x1, y1).
    p2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
    float: The Euclidean distance between the two points.
    """
    x1, y1 = p1
    x2, y2 = p2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


class Kaooa(Turtle):
	def __init__(self):
		super().__init__()
		self.thickness = 3
		self.bgcolor = 'lightgreen'
		# speed varies from 1-10 (slowest to fastest). 0 is instantaneous!!
		self.speed_val = 0 
		# initial positions are all empty
		self.state = ['', '', '', '', '', '', '', '', '', '']
		self.captured = 0
		self.gameover = False
		self.locked_vertex = -1 # unlocked
		
		# An empty screen is created automatically!
		self.screen.title("Kaooa Game")
		self.screen.setup(600, 600)
		self.screen.bgcolor(self.bgcolor)

		# declare extra turtles to display text
		self.text_turtle = Turtle()
		self.turn_turtle = Turtle()
		
		# get the coordinates of the 10 vertices of the Star
		self.coords = get_star_coordinates(400)

		# the adjacency matrix of the vertices of the star
		self.adj = [
			[0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
			[0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
			[0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
			[0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
			[1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
			[1, 0, 0, 1, 0, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
			[0, 1, 0, 0, 1, 1, 0, 0, 1, 0]
		]

		# the jump over positions (x,y) from index i -
		# mean the vulture can jump from i to y through x.
		self.jump = [
			[(7,8), (6,5)],
			[(8,7), (9,5)],
			[(6,7), (5,9)],
			[(7,6), (8,9)],
			[(5,6), (9,8)],
			[(9,1), (6,0)],
			[(5,4), (7,3)],
			[(6,2), (8,1)],
			[(9,4), (7,0)],
			[(8,3), (5,2)],
		]

		# render the initial state
		self.render_state()
		self.play_game()

	def color_dot_white(self, point):
		# draw an white circles at coords of 'point'
		self.pen(pencolor="white", fillcolor="white", pensize=1, speed=self.speed_val)
		self.penup()
		self.goto(point)
		self.pendown()
		self.dot(18)

	def color_dot_blue(self, point):
		# blue color to represent a crow
		self.pen(pencolor="blue", pensize=1, speed=self.speed_val)
		self.penup()
		self.goto(point)
		self.pendown()
		self.dot(24)

	def color_dot_red(self, point):
		# red color to represent a vulture
		self.pen(pencolor="red", pensize=1, speed=self.speed_val)
		self.penup()
		self.goto(point)
		self.pendown()
		self.dot(24)

	def lock_crow_dot(self):
		point = self.coords[self.locked_vertex]
		# violet color to represent a locked crow 
		self.pen(pencolor="purple", pensize=1, speed=self.speed_val)
		self.penup()
		self.goto(point)
		self.pendown()
		self.dot(22)

	def unlock_crow_dot(self):
		point = self.coords[self.locked_vertex]
		self.color_dot_blue(point)

	def place_circle_text(self, point):
		"""paint a dot with blue color to represent a crow at the text area"""
		self.text_turtle.pen(fillcolor="blue", pensize=1, speed=self.speed_val)
		self.text_turtle.penup()
		self.text_turtle.goto(point)
		self.text_turtle.pendown()
		self.text_turtle.begin_fill()
		self.text_turtle.circle(10)
		self.text_turtle.end_fill()

	def erase_dot(self, point):
		# first replace the dot with the background color
		self.pen(pencolor=self.bgcolor, pensize=1, speed=self.speed_val)
		self.penup()
		self.goto(point)
		self.pendown()
		self.dot(24)
		# place a white dot
		self.color_dot_white(point)

	def show_gameover_status(self, message=""):
		"""show a text message in the texta area"""
		# reset the turtle
		self.text_turtle.clear()
		self.text_turtle.hideturtle()  # Hide the turtle icon
		pos = self.coords[2]
		# change y position
		pos = (pos[0]+180, pos[1]-70)
		self.text_turtle.penup()
		self.text_turtle.goto(pos)
		self.text_turtle.pendown()
		# Print the Text
		self.text_turtle.write(message, move=True, font=("Arial", 28, "normal"), align="center")
	
	def show_turn_info(self):
		"""show whose turn is next"""
		t = self.turn_turtle
		# reset the turtle to clear the text area
		t.clear()
		t.hideturtle()  # Hide the turtle icon
		pos = self.coords[3]
		# change y position
		pos = (pos[0]+250, pos[1]+60)
		t.penup()
		t.goto(pos)
		t.pendown()
		# Print the Text
		text_to_display = "Turn: "
		text_to_display += "vulture" if self.vturn else "crows"
		t.write(text_to_display, move=False, font=("Arial", 11, "normal"), align="right")

	def set_vturn(self, status):
		"""
		set vulture's turn to the input boolean value
		"""
		self.vturn = status
		# re-render the turn info area
		self.show_turn_info()

	def show_crows_status(self):
		"""show the remaining crows number graphically"""
		t = self.text_turtle
		# reset the turtle
		t.clear()
		t.hideturtle()  # Hide the turtle icon
		pos = self.coords[2]
		# change y position
		pos = (pos[0], pos[1]-50)
		t.penup()
		t.goto(pos)
		t.pendown()
		# Print the Text
		t.write("Crows:", move=True, font=("Arial", 14, "normal"), align="left")
		pos = (pos[0]+50, pos[1])
		# show a blue circle for each crow
		ncrows_placed = sum([x=='crow' for x in self.state]) + self.captured
		ncrows_remaining = 7 - ncrows_placed
		for _ in range(ncrows_remaining):
			# position slightly to the right
			pos = (pos[0]+30, pos[1])
			self.place_circle_text(pos)

		# Show captured crows in the next line
		pos = self.coords[2]
		pos = (pos[0], pos[1]-100)
		t.penup()
		t.goto(pos)
		t.pendown()
		# Print the Text
		t.write("Captured:", move=True, font=("Arial", 14, "normal"), align="left")
		pos = (pos[0]+50, pos[1])
		# show a blue circle for each crow
		for i in range(self.captured):
			# position slightly to the right
			pos = (pos[0]+30, pos[1])
			self.place_circle_text(pos)


	def render_state(self):
		# re-render the state everytime
		self.reset()
		
		# Set the speed 1-10 (0 is instantaneous)
		self.speed(self.speed_val)  
		
		self.hideturtle()  # Hide the turtle icon
		# set thickness of the lines
		self.pensize(self.thickness)
		# Draw the pentagon
		self.penup()
		self.goto(self.coords[0])
		self.pendown()
		for vertex in self.coords[1:5]:
			self.goto(vertex)
		self.goto(self.coords[0])  # Connect back to the first vertex

		# draw circles
		# set thickness of the lines to small
		for i in range(10):
			if self.state[i] == 'crow':
				self.color_dot_blue(self.coords[i])

			elif self.state[i] == 'vulture':
				self.color_dot_red(self.coords[i])
			else:
				self.color_dot_white(self.coords[i])

		self.show_crows_status()

	def move_vulture(self, prev_vertex, new_vertex):
		""" 
		move the vulture from prev_vertex to the new_vertex 
		"""
		self.state[prev_vertex] = ''
		self.erase_dot(self.coords[prev_vertex])
		self.state[new_vertex] = 'vulture'
		self.color_dot_red(self.coords[new_vertex])
		# change turns
		self.set_vturn(False)
		
	def check_any_vmove_possible(self, vloc):
		"""
		check if any move possible for the vulture at location vloc
		"""
		# check if any nearby move possible
		for loc, val in enumerate(self.adj[vloc]):
			if val and self.state[loc] == '':
				return True

		# check for any jump-over locations possible
		for middle, target in self.jump[vloc]:
			if self.state[target] == '':
				return True

		return False

	def capture_crow(self, crow_vertex):
		self.state[crow_vertex] = ''
		self.erase_dot(self.coords[crow_vertex])
		self.captured += 1
		# re-render the crow status area
		self.show_crows_status()
		# set crows turn
		self.set_vturn(False)
		
		if self.captured >= 4:
			# Game Over!
			time.sleep(1)
			self.show_gameover_status("Vulture Won the Game!")
			self.gameover = True
			# Exit the game!
			# self.screen.bye()
			return

	def check_vulture_jumping_over(self, prev_vertex, selected_vertex):
		# check if vulture is jumping over a crow
		for middle, target in self.jump[prev_vertex]:
			# the middle vertex should have a crow to jump-over
			if selected_vertex != target or self.state[middle] != 'crow': continue
			# else jump the vulture
			self.move_vulture(prev_vertex, selected_vertex)
			# capture the crow
			self.capture_crow(middle)

	def vulture_turn(self, selected_vertex):
		# check if it's the first move of the user
		if 'vulture' not in self.state:
			self.state[selected_vertex] = 'vulture'
			self.color_dot_red(self.coords[selected_vertex])
			# change turns
			self.set_vturn(False)
			return
		
		prev_vertex = self.state.index('vulture')
		# the clicked location has to be either nearby or a jump-over location
		# check if clicking on a nearby vertex
		if self.adj[prev_vertex][selected_vertex]:
			self.move_vulture(prev_vertex, selected_vertex)
			return

		self.check_vulture_jumping_over(prev_vertex, selected_vertex)

	def check_vulture_trapped(self):
		"""
		check if the vulture is trapped by the crows
		"""
		# initial state; no trapping obviously!
		if 'vulture' not in self.state: return False

		# if all adjacent vertices are occupied by crows & no jumpover as well
		vloc = self.state.index('vulture')
		if not self.check_any_vmove_possible(vloc):
			# Game Over!
			time.sleep(1)
			self.show_gameover_status("Crows Won the Game!")
			self.gameover = True
			# Exit the game!
			# self.screen.bye()
			return

	def place_another_crow(self, selected_vertex):
		"""
		place a crow in an empty location
		"""
		# place the crow on the selected vertex
		self.state[selected_vertex] = 'crow'
		self.color_dot_blue(self.coords[selected_vertex])
		# re-render the crow status area
		self.show_crows_status()
		# set vulture turn!
		self.set_vturn(True)
		self.check_vulture_trapped()

	def lock_crow_vertex(self, selected_vertex):
		# unlock any previously locked vertex
		if self.locked_vertex != -1:
			self.unlock_crow_dot()

		self.locked_vertex = selected_vertex
		self.lock_crow_dot()

	def move_a_crow(self, prev_vertex, new_vertex):
		""" 
		move a crow from the prev_vertex to the new_vertex 
		"""
		self.state[prev_vertex] = ''
		self.erase_dot(self.coords[prev_vertex])
		self.state[new_vertex] = 'crow'
		self.color_dot_blue(self.coords[new_vertex])
		# change turns
		self.set_vturn(True)
		self.check_vulture_trapped()

	def move_an_existing_crow(self, selected_vertex):
		"""
		move a crow from a location to a nearby empty location in two user clicks
		"""
		# if a crow vertex is not locked already
		if self.locked_vertex < 0:
			# ignore clicking on an empty location
			if self.state[selected_vertex] != 'crow': return
			# else lock the clicked (crow) vertex 
			self.lock_crow_vertex(selected_vertex)

		elif self.state[selected_vertex] == 'crow': 
			# change the lock to the clicked (crow) vertex 
			self.lock_crow_vertex(selected_vertex)
		else:
			# move only if the selected vertex is adjacent to the locked vertex
			if self.adj[self.locked_vertex][selected_vertex]:
				self.move_a_crow(self.locked_vertex, selected_vertex)
				# remove any lock
				self.locked_vertex = -1


	def crows_turn(self, selected_vertex):
		"""
		let the crows make a move; two possibilities (place/move)
		"""
		# count how many crows are already placed on the board
		ncrows_placed = sum([x=='crow' for x in self.state]) + self.captured
		if ncrows_placed < 7:
			# ignore clicking on a crow location again
			if self.state[selected_vertex] == 'crow': return
			self.place_another_crow(selected_vertex)
		else:
			self.move_an_existing_crow(selected_vertex)
		

	def user_clicked(self, x, y):
		# no move if game is over
		if self.gameover: return

		# find the nearest vertex to the clicked position
		dists = [euclidean_distance((x,y), c) for c in self.coords]
		nearest_vertex = dists.index(min(dists))
		# the clicked position should be reasonably close to one of the vertices
		if min(dists) > 20: return

		if self.vturn:
			# the clicked vertex should be empty
			if self.state[nearest_vertex] != '': return
			self.vulture_turn(nearest_vertex)
		else:
			# ignore clicking on vulture location
			if self.state[nearest_vertex] == 'vulture': return
			self.crows_turn(nearest_vertex)


	def play_game(self):
		"""
		Play the kaooa game taking turns.
		The user plays vulture & the system plays the crows.
		"""
		# crows start the game
		self.set_vturn(False)
		# listener for user clicks on an empty circle's vicinity
		self.screen.onclick(self.user_clicked)
		# print("Game ended!")
		


game = Kaooa()
input("Press Enter to Quit. ")