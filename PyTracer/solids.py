"""
Geometric solids (with intersection methods)

Author: Rajiv Thamburaj
"""

from abc import ABCMeta, abstractmethod
import constants as const
import numpy as np
import math

class Solid(object):
	"""
	Abstract class for a geometric solid
	"""
	
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def did_hit(self, ray, shade_rectangle): pass

class Plane(Solid):
	"""
	Models an infinite plane
	"""
	
	def __init__(self, point, normal, color):
		"""
		Initializer
		"""
		self.point = point
		self.normal = normal
		self.color = color
	
	def did_hit(self, ray, shade_rectangle):
		"""
		Returns True if the given ray intersects the plane, and mutates the
		shade rectangle
		"""
		t_1 = np.dot((self.point-ray.origin), self.normal)
		t_2 = np.dot(ray.direction, self.normal)
		# Avoid division by zero
		if abs(t_2) <= const.EPSILON:
			return False
		t = t_1 / t_2
		
		if t > const.EPSILON:
			self.t_min = t
			# Modify the shade rectangle reference
			shade_rectangle.normal = self.normal
			shade_rectangle.local_hit_point = ray.origin + t*ray.direction
			return True
		return False

class Sphere(Solid):
	"""
	Models a spherical shell
	"""
	
	def __init__(self, center, radius, color):
		"""
		Initializer
		"""
		self.center = center
		self.radius = radius
		self.color = color
	
	def did_hit(self, ray, shade_rectangle):
		"""
		Returns True if the given ray intersects the spherical shell, and mutates
		the shade rectangle
		"""
		difference = ray.origin - self.center
		a = np.dot(ray.direction, ray.direction)
		b = 2.0 * np.dot(difference, ray.direction)
		c = np.dot(difference, difference) - self.radius*self.radius
		discriminant = b*b - 4.0*a*c
		
		if discriminant < 0.0:
			return False
		else:
			discriminant_root = math.sqrt(discriminant)
			denominator = 2.0 * a
			
			# Smaller root first
			t = (-b - discriminant_root) / denominator
			if (t > const.EPSILON):
				self.t_min = t
				shade_rectangle.normal = (difference + t*ray.direction) / self.radius
				shade_rectangle.local_hit_point = ray.origin + t*ray.direction
				return True
			# Larger root next
			t = (-b + discriminant_root) / denominator
			if (t > const.EPSILON):
				self.t_min = t
				shade_rectangle.normal = (difference + t*ray.direction) / self.radius
				shade_rectangle.local_hit_point = ray.origin + t*ray.direction
				return True
		return False