"""
Classes for sampling multiple points

Author: Rajiv Thamburaj
"""

from abc import ABCMeta, abstractmethod
import math
import numpy as np
import random

class Sampler(object):
	"""
	Base class for a sampler
	"""
	
	def __init__(self, num_samples):
		"""
		Initializer
		"""
		self.num_samples = num_samples
		self.sample_index = 0
		self.num_sets = 80
		
		self.generate_samples()
	
	def next_sample(self):
		"""
		Returns the next point to be sampled in the set [0,1] x [0,1]
		"""
		sample_size = self.num_samples * self.num_sets
		next_sample = (self.samples[self.sample_index % sample_size])
		self.sample_index += 1
		return next_sample
		

class JitteredSampler(Sampler):
	"""
	Samples are varied randomly in each rectilinear subspace. The number
	of samples must be a perfect square.
	"""
	
	def generate_samples(self):
		"""
		Generate the samples on a unit square
		"""
		n = int(math.sqrt(self.num_samples))
		self.samples = []
		
		# Loop through all sampling sets
		for p in xrange(self.num_sets):
			# Loop through all points in two dimensions
			for i in xrange(n):
				for j in xrange(n):
					# Select x- and y-coordinates randomly
					x = (j + random.random()) / n
					y = (i + random.random()) / n
					sample = np.array([x, y], float)
					self.samples.append(sample)
	
	