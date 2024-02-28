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


def getStarCoordinates(side):
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

class Kaooa(Turtle):
	def __init__(self):
		super().__init__()
		self.thickness = 3
		self.bgcolor = 'lightgreen'
		# initial positions are all empty
		self.state = ['', '', '', '', '', '', '', '', '', '']
		self.ncrows = 0 # upto 7
		self.begun = False
		self.captured = 0
		
		# An empty screen is created automatically!
		self.screen.title("Kaooa Game")
		self.screen.setup(600, 600)
		self.screen.bgcolor(self.bgcolor)
		
		# get the coordinates of the 10 vertices of the Star
		self.coords = getStarCoordinates(400)

		# choose a location randomly and place a crow there
		loc = random.randint(0, 9)
		self.state[loc] = 'crow'
		
		# render the initial state
		self.renderState()
		self.begun = True



	def renderState(self):
		# re-render the state everytime
		self.reset()
		
		# Set the speed 1-10 (0 is instantaneous)
		speed = 10
		if self.begun: speed = 0
		self.speed(speed)  
		
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
				# blue color to represent the crow
				self.pen(pencolor="blue", pensize=1, speed=speed)
				self.penup()
				self.goto(self.coords[i])
				self.pendown()
				self.dot(18)

			elif self.state[i] == 'vulture':
				pass
			else:
				# draw an empty circles
				self.pen(pencolor="white", fillcolor="white", pensize=1, speed=speed)
				self.penup()
				self.goto(self.coords[i])
				self.pendown()
				self.dot(18)




game = Kaooa()

input("Press Enter to Quit. ")