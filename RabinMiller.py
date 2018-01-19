#!/usr/bin/python
import sys
import random


def exp(x, y, N):
	if y == 0:
		return 1
	z = exp(x, y/2, N)
	if y % 2 == 0:
		return z*z % N
	else:
		return x*z*z % N

def gcd(x, y):
	if y == 0:
		return x
	else:
		return gcd(y, x%y)


def getNontrivialFactors(N, b):
	p = gcd(N, b + 1)
	q = N/p
	return "%d * %d" % (p, q)

def RabinMiller(N, k):
	if  N == 2:
		print("2 is prime!")
		return
	#Start by factoring N - 1 into 2^r*d 
	r = 0
	d = N - 1
	while d % 2 == 0:
		d /= 2
		r += 1

	#Randomly select as to be tested dependent on passed in for k
	if N <= k + 2:
		a_list = range(2, N)
	else:
		a_list = random.sample(range(2, N), k)

	#define exception to allow us to continue primary loop in nested loops
	class ContinueWitnessLoop(Exception): pass
	
	#Iterate through the chosen a's testing to see if any a's are witnesses 
	for a in a_list:
		try: 
			#Now calculate b = a^d. If b = 1 or -1 (mod N), then probably prime
			b = exp(a, d, N)
			if b == 1 or b == N - 1:
				continue #N probably prime, so continue checking values for other a
			
			#Now progressively square the b each step till we get to a^(2^(r - 1)*d)
			#if a b is -1, then it is probably prime, and 1 then it is definitely composite so return
			for i in range(r - 1):
				b = b*b % N
				if b == 1:
					#We have found a nontrivial square root of 1!! N must be composite!!
					print("%d is composite with Non-Trivial Factors: %s" % (N, getNonTrivialFactors(N, b)))
					return
				if b == -1:
					#N passes fermat, so it is probably prime. So contiue witness loop
					raise ContinueWitnessLoop()
			
			#if we have exited the r loop, then that means a^(2^(r - 1)) is neither 1 nor -1, 
			#so know that it is composite, but can't find nontrivial root
			print("%d is composite" % N)
			
		except ContinueWitnessLoop:
			pass
	
	#If we have made it out of the witness loop, all a's told us its probably prime, so it's probably prime
	print("%d is probably prime with prob: %.4f" % (N, 1-(.25)**k))

def main(args):
	if len(args) < 2:
		print("ERROR. Program arguments not valid.\nUSAGE: RabinMiller.py [NUMBER_TO_TEST] [K-value (default = 10)]\n")
		return
	if len(args) > 2:
		k = int(args[2])
	else:
		k = 10
	N = int(args[1]);
	RabinMiller(N, k)
	
if __name__ == "__main__":
	main(sys.argv)
