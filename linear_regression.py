#!/usr/bin/env python3
# coding: utf-8


import sys


def get_thetas():
	theta_file = "thetas.txt"
	try:
		with open(theta_file, 'r') as f:
			thetas = [float(line.rstrip('\n')) for line in f]
			print(thetas)
			if len(thetas) != 2 or \
			isinstance(thetas[0], (int, float)) is False or \
			isinstance(thetas[1], (int, float)) is False :
				print("File {} is corrupted".format(theta_file))
				sys.exit(1)
			else:
				return thetas[0], thetas[1]
	except IOError:
		return 0, 0

def estimate(theta0, theta1, x):
	return theta0 + (theta1 * x)

if __name__ == "__main__":
	while (1):
		try:
			mileage = int(input("Enter a mileage: "), 10)
			if mileage <= 0:
				print("Enter a positive mileage")
			else:
				theta0, theta1 = get_thetas()
				print("Estimated price is: {}".format(estimate(theta0, theta1, mileage)))
		except ValueError:
			print("Wrong input")
