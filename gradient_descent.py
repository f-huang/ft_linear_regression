#!/usr/bin/env python3
# coding: utf-8

import sys
import csv

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


def mean(numbers):
	return float(sum(numbers) / max(len(numbers), 1))


def estimate_price(theta0, theta1, x):
	return theta0 + theta1 * x;


def normalize_dataset(map):
	mean_x = mean(map)
	mean_y = mean(map.values())
	range_x = (max(map) - min(map))
	range_y = (max(map.values()) - min(map.values()))
	return {(x) / max(map) : (y) / max(map.values()) for x, y in map.items()}


def unnormalize_theta_0(map, theta0):
	return theta0 * max(map.values())


def unnormalize_theta_1(map, theta1):
	return theta1 * max(map.values()) / max(map)


def train(map):
	theta0 = 0
	theta1 = 0
	learningRate = 1.5
	m = len(map)
	i = 0
	while i < 500:
		tmp_theta0 = (learningRate * sum(
			estimate_price(theta0, theta1, km) - price
			for km, price in map.items())) / m
		tmp_theta1 = (learningRate * sum(
			(estimate_price(theta0, theta1, km) - price) * km
			for km, price in map.items())) / m
		if abs(theta1 - theta1 - tmp_theta1) < 10e-11:
			break
		theta0 -= tmp_theta0
		theta1 -= tmp_theta1
		i += 1
	print(i)
	return theta0, theta1


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print('usage: {} <csv_file>'.format(__file__))
		sys.exit(-1)
	path = sys.argv[1]
	dataset = get_dataset(path)
	map = normalize_dataset(dataset)
	thetas = train(map)
	thetas = unnormalize_theta_0(dataset, thetas[0]), \
		unnormalize_theta_1(dataset, thetas[1])
	print(thetas)
	save_thetas(thetas)
