"""
Classes for storing and rendering geometric objects

Author: Rajiv Thamburaj
"""

import constants as const
import solids
import numpy as np
import matplotlib.pyplot as plt
import sample
import math
import random

class World(object):
	"""
	Models and renders a 'world' of objects
	"""
	
	def __init__(self):
		"""
		Initializer
		"""
		self.build()
		self.pixels = np.zeros((self.sr.screen_width, self.sr.screen_height, 3))
		
		self.render()
		self.display_image()
	
	def build(self):
		"""
		Places objects in the World
		"""
		# Set up the screen rectangle (stores information to render the scene)
		self.sr = ScreenRect()
		self.sr.screen_width = 200
		self.sr.screen_height = 200
		self.sr.pixel_width = 1.0
		self.sr.num_samples = 1
		self.sr.sampler = sample.UniformSampler(self.sr.num_samples)
		
		# Set up instance variables
		self.background_color = const.BLACK
		self.tracer = MultiplePrimitivesTracer(self)
		self.view_distance = 200
		self.plane_distance = 100
		
		# Sphere 1
		center = np.array([0, -25, 0], float)
		radius = 80
		color = const.RED
		sphere_1 = solids.Sphere(center, radius, color)
		
		# Sphere 2
		center = np.array([0, 30, 0], float)
		radius = 60
		color = const.YELLOW
		sphere_2 = solids.Sphere(center, radius, color)
		
		# Plane
		point = np.array([0, 0, 0], float)
		normal = np.array([0, 1, 1], float)
		color = np.array([0, 0.3, 0], float)
		plane = solids.Plane(point, normal, color)
		
		self.objects = [sphere_1, sphere_2, plane]
	
	def render(self):
		"""
		Renders the image, pixel by pixel
		"""
		# Origin for the rays on the z-axis
		z_w = 100.0
		ray_direction = np.array([0, 0, -1], float)
		# Find the side length of the sample rectangle
		n = int(math.sqrt(self.sr.num_samples))
		
		for i in xrange(0, self.sr.screen_height):
			self.print_progress(i)
			for j in xrange(0, self.sr.screen_width):
				pixel_color = const.BLACK
				n = self.sr.num_samples
				# Loop through all samples
				for p in xrange(n):
					# Get the next sampling point in the set [0,1] x [0,1]
					sample_point = self.sr.sampler.get_square_sample()
					# Find the point within the current pixel to sample
					x = self.sr.pixel_width * (j - 0.5*self.sr.screen_width + sample_point[0])
					y = self.sr.pixel_width * (i - 0.5*self.sr.screen_height + sample_point[1])
					
					ray_origin = np.array([x, y, z_w], float)
					# Add the color to the current value
					pixel_color = pixel_color + self.tracer.trace_ray(ray_origin, ray_direction)

				# Take the average of the colors
				pixel_color = pixel_color*(1.0/self.sr.num_samples)
				# Store the pixel color
				self.add_pixel(i, j, pixel_color)
	
	def render_perspective(self):
		"""
		Renders the image, pixel by pixel, with perspective tracing
		"""
		# Origin for the rays on the z-axis (common)
		ray_origin = np.array([0, 0, self.view_distance], float)
		
		for i in xrange(0, self.sr.screen_height):
			self.print_progress(i)
			for j in xrange(0, self.sr.screen_width):
				# Find the direction of the ray
				d_x = self.sr.pixel_width * (j - 0.5*(self.sr.screen_width - 1.0))
				d_y = self.sr.pixel_width * (i - 0.5*(self.sr.screen_height - 1.0))
				d_z = -self.plane_distance
				ray_direction = np.array([d_x, d_y, d_z], float)
				ray_direction = ray_direction * (1.0/np.linalg.norm(ray_direction))
				
				# Find the color of the pixel and store it
				pixel_color = self.tracer.trace_ray(ray_origin, ray_direction)
				self.add_pixel(i, j, pixel_color)
	
	def print_progress(self, outer_loop_index):
		"""
		Print how far the render has progressed
		"""
		percent_progress = 100.0*outer_loop_index/self.sr.screen_height
		print str(percent_progress) + "%"
	
	def add_pixel(self, row, column, color):
		"""
		Adds the pixel color to the numpy array of pixels
		"""
		if self.sr.gamma != 1.0:
			color = color**(1.0/self.sr.gamma)
		
		x = column
		y = self.sr.screen_height - row - 1
		# The internal coordinates must be mapped to the representation in the array
		self.pixels[y,x] = color
	
	def display_image(self):
		"""
		Displays the image on the screen
		"""
		plt.imshow(self.pixels)
		plt.axis("off")
		plt.show()
		
	def hit_primitives(self, ray_origin, ray_direction):
		"""
		Find the closest hit point for the given ray
		"""
		t_min = float("inf")
		shade_rectangle = ShadeRectangle(self)
		
		# Loop through all objects
		for object in self.objects:
			if object.did_hit(ray_origin, ray_direction, shade_rectangle):
				# Find the closest point of intersection
				if object.t_min < t_min:
					shade_rectangle.did_hit = True
					t_min = object.t_min
					shade_rectangle.color = object.color
		
		return shade_rectangle

class ScreenRect(object):
	"""
	Keeps track of information needed to render the current scene
	"""
	
	def __init__(self):
		"""
		Initializer
		"""
		# Set default values
		self.screen_width = 100
		self.screen_height = 100
		self.pixel_width = 1.0
		self.gamma = 1.0

class ShadeRectangle(object):
	"""
	Keeps track of information needed to shade a ray's hit point
	"""
	
	def __init__(self, world):
		"""
		Initializer
		"""
		self.world = world
		
		self.did_hit = False
		self.normal = None
		self.local_hit_point = None

class Tracer(object):
	"""
	Specifies a set of rules for the way an object should be rendered
	"""
	
	def __init__(self, world):
		"""
		Initializer
		"""
		self.world = world
	
	def trace_ray(self, ray_origin, ray_direction):
		"""
		Determines the color of the pixel for the given ray
		"""
		return const.BLACK

class MultiplePrimitivesTracer(Tracer):
	"""
	Tracer for drawing multiple primitives
	"""
	
	def trace_ray(self, ray_origin, ray_direction):
		"""
		Determines the color of the pixel for the given ray
		"""
		shade_rectangle = self.world.hit_primitives(ray_origin, ray_direction)
		
		if shade_rectangle.did_hit:
			return shade_rectangle.color
		else:
			return self.world.background_color