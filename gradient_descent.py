#!/usr/bin/env python3
# coding: utf-8

import sys
import csv
import matplotlib.pyplot as plt
import numpy as np


def get_dataset(path):
	try:
		map = {}
		with open(path, 'r') as f:
			f.readline()
			for line in f:
				x, y = line.split(',')
				map[float(x)] = float(y)
		return map
	except IOError:
		print('Could not open file: {}'.format(path))
		sys.exit(-1)


def save_thetas(thetas):
	theta_file = "thetas.txt"
	try:
		with open(theta_file, 'w+') as f:
			f.write("{0}\n{1}".format(thetas[0], thetas[1]))
	except IOError:
		print("Could not open file {}".format(theta_file))
		sys.exit(-1)


def normalize_dataset(map):
	return {(x) / max(map) : (y) / max(map.values()) for x, y in map.items()}


def unnormalize(map, thetas):
	maximum = max(map.values())
	return thetas[0] * maximum,  thetas[1] * maximum / max(map)


def show_graph(dataset, thetas, equation):
	plt.scatter(*zip(*sorted(dataset.items())))
	plt.title("Price of a car depending on its mileage")
	plt.xlabel("mileage(km)")
	plt.ylabel("price(€)")
	plt.axis([0, max(dataset) + 10000, 0, max(dataset.values()) + 1000])
	x = np.linspace(min(dataset) - 1000, max(dataset) + 10000)
	y = equation(thetas[1], thetas[0])(x)
	plt.plot(x, y,\
		color='#FF0000', \
		label='{:.3f}x + {:.3f}'.format(thetas[1], thetas[0]) \
	)
	plt.legend(loc="best")
	plt.show()


def get_linear_function(a, b):
	def f(x):
		return (a * x + b)
	return f


def distance(map, g):
	return float(sum(g(km, price) for km, price in map.items())) / len(map)


def train(map):
	thetas, learningRate = [0.0, 0.0], 1.5
	i, cost = 0, 100
	while i < 1000:
		f = get_linear_function(thetas[1], thetas[0])
		thetas[0] -= learningRate * distance(map, lambda km, price: f(km) - price)
		thetas[1] -= learningRate * distance(map, lambda km, price: (f(km) - price) * km)
		old_cost = cost
		cost = distance(map, lambda km, price: (f(km) - price)**2)
		if abs(old_cost - cost) < 10e-11:
			break
		i += 1
	print(i)
	return thetas


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print('usage: {} <csv_file>'.format(__file__))
		sys.exit(-1)
	path = sys.argv[1]
	dataset = get_dataset(path)
	map = normalize_dataset(dataset)
	thetas = unnormalize(dataset, train(map))
	print(thetas)
	save_thetas(thetas)
	show_graph(dataset, thetas, get_linear_function)
