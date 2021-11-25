# Simulated annealing optimization for travelling salesman

Performs a simulated annealing optimization to solve travelling salesman problem of finding the shortest route between multiple points written in Python for coursework.

Simulated annealing (SA) is a probabilistic technique for approximating the global optimum of a given function. Specifically, it is a metaheuristic to approximate global optimization in a large search space for an optimization problem. [[Wikipedia](https://en.wikipedia.org/wiki/Simulated_annealing)]

The traveling salesman problem asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?" [[Wikipedia2](https://en.wikipedia.org/wiki/Travelling_salesman_problem)]

For info regarding the coursework assignment see [Travelling salesman.pdf](https://github.com/pitkanenlauri/salesman/blob/main/Travelling%20salesman.pdf).

## How to use

**Requirements:** Python 3.x.x, NumPy, SciPy and Matplotlib

**How to run:**
- cities20.txt is used for cities xy coordinates for where the salesman must visit. If you want to try for cities10.txt or some other change the text file name in line 279 *cities = read_cities_from_file('cities20.txt')* in salesman.py main.
- run in cmd: python salesman.py
- -> outputs the image of shortest distance between points, prints the shortest distance, list of the order to visit cities for shortest distance and running time. Also the list of the cities shortest visiting order is outputted as a text file into the running directory.

## Screenshots

![Shortest route with 20 cities.](/salesman_screenshot_cities20.png)

Solution for shortest route of salesman visiting 20 cities given in cities20.txt.
