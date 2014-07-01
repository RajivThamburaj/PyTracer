"""
Geometry methods for ray tracing

Author: Rajiv Thamburaj
"""

class Ray(object):
	"""
	Models a physical ray
	"""
	
	def __init__(self, origin, direction):
		"""
		Initializer
		"""
		self.origin = origin
		self.direction = direction