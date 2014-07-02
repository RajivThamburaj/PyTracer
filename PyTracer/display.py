"""
Classes for storing and rendering geometric objects

Author: Rajiv Thamburaj
"""

import constants as const
import solids
import geometry as geom
import numpy as np
import matplotlib.pyplot as plt
import math
import random

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
		self.num_samples = 1

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
		
		self.render_image()
		self.display_image()
	
	def build(self):
		"""
		Places objects in the World
		"""
		self.sr = ScreenRect()
		self.sr.screen_width = 200
		self.sr.screen_height = 200
		self.sr.num_samples = 4
		
		self.background_color = const.BLACK
		self.tracer = MultiplePrimitivesTracer(self)
		
		center = np.array([0, -25, 0], float)
		radius = 80
		color = const.RED
		sphere_1 = solids.Sphere(center, radius, color)
		
		center = np.array([0, 30, 0], float)
		radius = 60
		color = const.YELLOW
		sphere_2 = solids.Sphere(center, radius, color)
		
		point = np.array([0, 0, 0], float)
		normal = np.array([0, 1, 1], float)
		color = np.array([0, 0.3, 0], float)
		plane = solids.Plane(point, normal, color)
		
		self.objects = [sphere_1, sphere_2, plane]
	
	def render_image(self):
		"""
		Renders the image, pixel by pixel
		"""
		# Origin for the rays on the z-axis
		z_w = 100.0
		ray_direction = np.array([0, 0, -1], float)
		n = int(math.sqrt(self.sr.num_samples))

		for i in xrange(0, self.sr.screen_height):
			print str(100.0*i/self.sr.screen_height) + "%"
			for j in xrange(0, self.sr.screen_width):
				pixel_color = const.BLACK
				
				for p in xrange(n):
					for q in xrange(n):
						x = self.sr.pixel_width * (j - 0.5*self.sr.screen_width + (q+random.random())/n)
						y = self.sr.pixel_width * (i - 0.5*self.sr.screen_height + (p+random.random())/n)
						
						ray_origin = np.array([x, y, z_w], float)
						ray = geom.Ray(ray_origin, ray_direction)
						pixel_color = pixel_color + self.tracer.trace_ray(ray)

				pixel_color = pixel_color*(1.0/self.sr.num_samples)
				self.add_pixel(i, j, pixel_color)
		
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
		
	def hit_primitives(self, ray):
		"""
		Find the closest hit point for the given ray
		"""
		t_min = float("inf")
		shade_rectangle = ShadeRectangle(self)
		
		for object in self.objects:
			if object.did_hit(ray, shade_rectangle):
				if object.t_min < t_min:
					shade_rectangle.did_hit = True
					t_min = object.t_min
					shade_rectangle.color = object.color
		
		return shade_rectangle

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
	
	def trace_ray(self, ray):
		"""
		Determines the color of the pixel for the given ray
		"""
		return const.BLACK

class MultiplePrimitivesTracer(Tracer):
	"""
	Tracer for drawing multiple primitives
	"""
	
	def trace_ray(self, ray):
		"""
		Determines the color of the pixel for the given ray
		"""
		shade_rectangle = self.world.hit_primitives(ray)
		
		if shade_rectangle.did_hit:
			return shade_rectangle.color
		else:
			return self.world.background_color