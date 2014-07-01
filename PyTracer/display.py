"""
Classes for storing and rendering geometric objects

Author: Rajiv Thamburaj
"""

import constants as const
import solids
import geometry as geom
import numpy as np
import matplotlib.pyplot as plt

class World(object):
	"""
	Models and renders a 'world' of objects
	"""
	
	def __init__(self):
		"""
		Initializer
		"""
		self.pixels = np.zeros((const.SCREEN_WIDTH, const.SCREEN_HEIGHT, 3))
		
		self.build()
		self.render_image()
	
	def build(self):
		"""
		Places objects in the World
		"""
		self.tracer = SphereTracer(self)
		
		center = np.array([0, 0, 0], float)
		radius = 85.0
		self.sphere = solids.Sphere(center, radius)
	
	def render_image(self):
		"""
		Renders the image, pixel by pixel
		"""
		# Origin for the rays on the z-axis
		z_w = 100.0
		ray_direction = np.array([0, 0, -1], float)
		
		for i in xrange(0, const.SCREEN_HEIGHT):
			for j in xrange(0, const.SCREEN_WIDTH):
				x = const.PIXEL_WIDTH * (j - 0.5*(const.SCREEN_WIDTH - 1.0))
				y = const.PIXEL_WIDTH * (i - 0.5*(const.SCREEN_HEIGHT - 1.0))
				
				ray_origin = np.array([x, y, z_w], float)
				ray = geom.Ray(ray_origin, ray_direction)
				pixel_color = self.tracer.trace_ray(ray)
				
				self.add_pixel(i, j, pixel_color)
		
		self.display_image()
		
	def add_pixel(self, row, column, color):
		"""
		Adds the pixel color to the numpy array of pixels
		"""
		x = column
		y = const.SCREEN_HEIGHT - row - 1
		self.pixels[x,y] = color
	
	def display_image(self):
		"""
		Displays the image on the screen
		"""
		plt.imshow(self.pixels)
		plt.show()

class ShadeRectangle(object):
	"""
	Keeps track of information needed to shade a ray's hit point
	"""
	
	def __init__(self, world):
		"""
		Initializer
		"""
		self.world = world
		
		self.normal = None
		self.hit_point = None
		self.did_hit = False

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

class SphereTracer(Tracer):
	"""
	Tracer for drawing a single sphere
	"""
	
	def trace_ray(self, ray):
		"""
		Determines the color of the pixel for the given ray
		"""
		self.shade_rectangle = ShadeRectangle(self.world)
		if self.world.sphere.did_hit(ray, self.shade_rectangle):
			return const.RED
		else:
			return const.BLACK