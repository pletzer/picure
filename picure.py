#!/usr/bin/env python

import numpy
import pywt
import scipy

class Picure:

	def __init__(self, array, wavelet, mode):
		"""
		Constructor
		@param array numpy masked array instance
		@param wavelet wavelet basis, for example: 'db1'
		@param mode for example: 'symmetric'
		@note see 
		"""

		self.wavelet = wavelet
		self.mode = mode

		# number of dimensions
		self.numDims = len(array.shape)

		# invalid indices
		self.invalidInds = numpy.wherearray.mask

		# valid indices
		self.validInds = ~array.mask

		# array with data set to zero at the invalid indices
		self.a0 = numpy.zeros(array.shape)
		self.a0[validInds] = array[validInds]

		# the complementary fields, zero everywhere except at one
		# invalid field index set
		invInds = numpy.where(array.mask)
		numInvInds = len(invInds[0])
		self.invalidIndexSets = []
		for i in range(numInvInds):
			ind = [invInds[d][i] for d in self.numDims]
			self.invalidIndexSets.append(ind)

		self.b = {}
		for ind in self.invalidIndexSets:
			barr = numpy.zeros(array.shape)
			barr[ind] = 1
			self.b[ind] = barr

		# compute the discrete wavelet coefficients of the fields
		self.coefA0 = pywt2.dwt2(self.a0, wavelet, mode)
		self.coefB = {}
		for ind in self.invalidIndexSets:
			coef = pywt.dwt2(self.b[ind], wavelet, mode)
			self.coefB[ind] = coef

	def computeResponse(self, lmda):
		"""
		Compute the "interpolated" response
		@param lmbda the set of coefficents
		@return "cured" data
		"""
		res = self.a0
		for i in range(len(self.invalidIndexSets)):
			ind = self.invalidIndexSets[i]
			res += lmbda[i] * self.b[ind]
		return res

	def computeOptimalCoefficients(self):
		"""
		Compute the optimal coefficients by minimizing a cost function
		@return the set of coefficients
		"""
		def costFunction(lmbda):
			cost = numpy.zeros(self.coefA0[1][2].shape)
			for i in range(len(self.invalidIndexSets)):
				cost += ldamb**2 * self.coefB[ind][1][2]**2
			return numpy.sum(cost)

		lmbda0 = numpy.zeros((self.numDims,))
		lmbda = scipy.optimize.minimize(costFunction, lmbda0)
		return lmbda


##############################################################################
def test():
	pass

if __name__ == '__main__':
	test()