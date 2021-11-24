# /usr/bin/env python
import sys
import copy
from math import *
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
from itertools import permutations


def read_route_from_file(filename):
    """
    Read a route from the file 'filename'.
    
    For a route of N cities, the file should contain
    the numbers 0,...,N-1 in some order, each number on its
    own line.
    
    The function returns an integer array containing the read numbers.
    """
    
    f = open(filename)
    lines = f.readlines()
    f.close()

    route = [ ]
        
    for line in lines:
        try:
            route.append( int(line) )
        except:
            pass

    return np.array(route)


def read_cities_from_file(filename):
    """
    Read the coordinates of cities from a file.
    
    Each line in the file should contain the x and y coordinates of one city.

    The function returns an N x 2 array containing the coordinates.
    """

    f = open(filename)
    lines = f.readlines()
    f.close()

    cities = [ ]
        
    for line in lines:
        parts = line.split()
        if len(parts) > 0:
            cities.append( [ float(parts[0]), float(parts[1]) ] )

    return np.array(cities)



def show_route(cities, route):
    """
    Plot the route.
    
    The array 'cities' contains the coordinates of the cities.
    The array 'route' contains indices of the cities in the order
    of the route.
    """

    # routeline will store the coordinates of the cities
    # in the order specified by 'route'
    routeline = []
    for place in route:
        routeline.append( cities[place] )
    routeline = np.array(routeline)

    plt.plot(cities[:,0], cities[:,1], 'o')
    plt.plot(routeline[:,0], routeline[:,1],  '-')
    plt.show()


def write_route_to_file(route, filename):
    """
    Write the route to a file name 'filename'.
    
    The route should be an integer array storing the indices
    of the cities in the order of visits. These will be written
    in the file, each number on a separate line.
    """
    writelines = ""    
    for i in route:
        writelines += str(i)+"\n "
    f = open(filename,'w')
    f.write(writelines)
    f.close()    
    
    
def create_random_route(cities):
    """
    Creates a random route between cities.

    Input:
    * cities: a list of coordinates of the cities.
    
    The function returns randomised integer array of cities indices.
    """
    # Create an array of random intergers as city indices.
    rand = random.permutation(len(cities))

    # Add first city also to last place to make trip round.
    route = np.append(rand, rand[0])
    
    return np.array(route)
            

def calculate_distances(cities):
    """
    Calculate the distances between all pairs of cities.
    
    The distances are stored in an N x N array, where the element
    (i,j) is the distance between cities i and j.
    
    The routine returns this array.
    """
    Ncities = len(cities)
    distances = np.array( [[0.0] * Ncities] * Ncities )
    for i in range(len(cities)):
        for j in range(len(cities)):
        
            dx = cities[i,0]-cities[j,0]
            dy = cities[i,1]-cities[j,1]
            distances[i,j] = sqrt(dx*dx + dy*dy)
            distances[j,i] = distances[i,j]
    
    return distances
    
    
def get_trip_length(route, distances):
    """
    Calculates the length of the route.
    
    Input:
    * route: an array storing the indices of cities in the order of visits
    * distances: an array storing the distances between all cities, as
      calculated by calculate_distances()
      
    The function returns the total length.
    """
    trip_length = 0.0

    # Sum the distances between cities, from 1 to 2 + 2 to 3 ... and so on.
    for i in range(len(route)-1):
        trip_length += distances[route[i], route[i+1]]

    return trip_length


def swap_cities(route):
    """
    Make a modification to the travel route.

    Input:
    * route: an array storing the indices of cities in the order of visits

    The function returns the route with having swapped the traveling order
    between two randomly chosen cities.
    """

    # choose cities
    city1 = random.randint(2, len(route)-1)
    while True:
        city2 = random.randint(2, len(route)-1)
        # and make sure that they are not same
        if city1 != city2:
            # also change order if needed
            if city2 < city1:
                city2, city1 = city1, city2
            break

    # make new route parts
    new_route = []
    begin = route[0:city1-1]
    swap = route[city2:city1-2:-1]
    end = route[city2+1:len(route)]

    # create new route with one part swapped
    new_route = np.append(begin, swap)
    new_route = np.append(new_route, end)

    return new_route


def optimize_route(route, distances, 
                    initial_temperature = 50.0, 
                    trials = 100000,
                    final_temperature = 1.0):
    """
    Perform simulated annealing optimization for the route length.
    
    Input:
    * route: an array storing the indices of cities in the order of visits
    * distances: an array storing the distances between all cities, as
      calculated by calculate_distances()
    * initial_temperature: temperature in the beginning
    * final_temperature: temperature in the end
    * trials: the number of times a new route is generated and tried
    
    The function returns the best route found during the simulation.
    """

    # constant for modifying the Boltzmann probability
    k = 0.01
    
    # the current temperature
    temperature = initial_temperature

    # store the current route and best one found so far
    current_route = route
    best_route = route
    shortest_length = get_trip_length(route, distances)

    # the length of the current route
    current_length = shortest_length

    # change of temperature between trials
    dt = (final_temperature - initial_temperature) / (trials-1)

    # run the algorithm
    for i in range(trials):

        # make a modification to travel route
        new_route = swap_cities(current_route)

        # calculate the length of the new route
        new_length = get_trip_length(new_route, distances)
        
        # calculate the change in route length
        dL = new_length - current_length

        # if the new route is shorter, accept it
        if new_length < current_length:
            current_route = copy.deepcopy(new_route)
            current_length = new_length
            route_changed = True
        else:
            R = random.random()
            # if the new route is longer, accept it
            # with the Boltzmann probability
            if R < exp(-dL/k*temperature):
                current_route = copy.deepcopy(new_route)
                current_length = new_length
                route_changed = True
            # otherwise don't
            route_changed = False
            # and discard it altogether
            del new_route

        # test if the new route is the best route,
        # and store it if it is
        if route_changed and new_length < shortest_length:
            best_route = copy.deepcopy(new_route)
            shortest_length = new_length

        # change the temperature
        temperature += dt

    return best_route
    


def main(args):
    """
    The main program.
    """
    
    # read cities from a file
    cities = read_cities_from_file('cities20.txt')

    # Calculate the distances between all cities and
    # store them in a file.
    # This way the distances need not be recalculated
    # over and over again.
    distances = calculate_distances(cities)

    # Initialize the route.
    # 
    # If filename defines a valid route file, it is read.
    # If this fails, create a random sequence.
    filename = ''
    try:
        route = read_route_from_file(filename)
    except:
        route = create_random_route(cities)

    # Calculate the length of the initial route.    
    trip_length = get_trip_length(route, distances)
    best_length = trip_length
    
    # Run the optimization algorithm.
    #
    # Once the algorithm works, you will need to
    # play around with the parameters to find a good solution.
    t_start = time.time()
    route = optimize_route(route, distances, 100.0, 100000, 10.0)
    route = optimize_route(route, distances, 10.0, 100000, 1.0)
    route = optimize_route(route, distances, 1.0, 100000, 0.1)
    route = optimize_route(route, distances, 0.1, 100000, 0.01)
    t_end = time.time()

    # Print the results
    print( "shortest trip distance found: " + str(get_trip_length(route, distances)) )
    print( "shortest trip found: " + str(route) )
    print( "run time " + str(t_end - t_start) )
    
    # Plot the best route and save it.
    show_route(cities, route)
    write_route_to_file(route, "best_route.txt")
    


if __name__ == "__main__":
    random.seed()
    main(sys.argv[1:])
