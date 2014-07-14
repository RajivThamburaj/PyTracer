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
	Base class for Sampler objects
	"""
	__metaclass__ = ABCMeta
	
	def __init__(self, num_samples):
		"""
		Initializer
		"""
		self.num_samples = num_samples
		self.sample_index = 0
		# We have 83 sets because 83 is a relatively large (for our purposes) prime number
		self.num_sets = 83
		self.samples = []
		
		# Sample generation is passed on to the subclass
		self.generate_samples()
		self.shuffle_indices()
	
	def get_square_sample(self):
		"""
		Returns the next point to be sampled in the set [0,1] x [0,1]. The sample points are
		generated ahead of time, so we must determine all the sets prior to ray-tracing and
		access the samples sequentially. To avoid sampling errors, we add some randomness to the
		process.
		"""
		# Sets are accessed in a random order to eliminate matching samples in rows/columns
		if (self.sample_index % self.num_samples) == 0:
			self.skip = (random.randrange(999) % self.num_sets) * self.num_samples
		
		# Within the current set, visit the current sample index (making sure not to exceed the
		# bounds of the list)
		index = self.skip + self.shuffled_indices[(self.skip + self.sample_index) % self.num_samples]
		next_sample = self.samples[index]
		self.sample_index += 1
		return next_sample
	
	def shuffle_indices(self):
		"""
		Shuffles sample indices to prevent streaks due to sample correlation
		"""
		self.shuffled_indices = []
		indices = range(self.num_samples)
		
		for i in xrange(self.num_sets):
			random.shuffle(indices)
			self.shuffled_indices += indices
	
	@abstractmethod
	def generate_samples(self): pass

class UniformSampler(Sampler):
	"""
	Samples are distributed uniformly through the rectangular domain.
	The number of samples must be a perfect square.
	"""
	
	def generate_samples(self):
		"""
		Generate the samples on a unit square (optimal for 1 sample)
		"""
		n = int(math.sqrt(self.num_samples))
				
		# Loop through all sampling sets
		for p in xrange(self.num_sets):
			# Loop through all points in two dimensions
			for i in xrange(n):
				for j in xrange(n):
					# Select x- and y-coordinates
					x = (j + 0.5) / n
					y = (i + 0.5) / n
					sample = np.array([x, y], float)
					self.samples.append(sample)

class RandomSampler(Sampler):
	"""
	Samples are varied randomly in the rectangular domain. The number of
	samples can be any integer.
	"""
	
	def generate_samples(self):
		"""
		Generate the samples on a unit square
		"""
		# Loop through all sampling sets
		for p in xrange(self.num_sets):
			# Loop through all points
			for i in xrange(self.num_samples):
				x = random.random()
				y = random.random()
				sample = np.array([x, y], float)
				self.samples.append(sample)

class JitteredSampler(Sampler):
	"""
	Samples are varied within strata in the recangular domain. The number
	of samples must be a perfect square.
	"""
	
	def generate_samples(self):
		"""
		Generate the samples on a unit square
		"""
		n = int(math.sqrt(self.num_samples))
		
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