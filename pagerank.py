# PageRank example
# MACS 30121 A'15
#
# This file contains the functions necessary to compute the PageRank of nodes
# in a graph where nodes represent websites and edges represent links 
# between websites.
#
# You can import the individual functions, or run pagerank.py as a program:
#
#    python3 pagerank.py <-r or -m> <file name> <number of steps>
#
# Where:
#
# - Specify "-r" to use the random surfer model, or "-m" to use Markov chains.
# - <file name> is the name of the file containing the graph
# - <number of steps> is the number of steps to take in the simulation.
#

import sys
import random

def read_graph(filename):
    '''
    Reads a graph from a file, and returns a matrix of counts (as a
    list-of-lists, where each entry (i,j) is the number of links from
    node i to j, and a list with the out-degrees of each node.

    Inputs:
        filename: (string) name of file containing the graph

    Returns: tuple w/
        List of lists of int with matrix of link counts
        List of integers with out-degrees of each node.
    '''

    try:
        f = open(filename)
    except (OSError, IOError) as e:
        print("Error opening file {}: {}".format(filename, e))
        sys.exit(1)

    try:
        n = int(f.readline())
        out_degree = [0]*n
        counts = []
        for i in range(n):
            counts.append([0]*n)        

        tokens = f.read().strip().split()

        assert(len(tokens) % 2 == 0)

        while len(tokens) > 0:
            u = int(tokens.pop(0))
            v = int(tokens.pop(0))

            out_degree[u] += 1
            counts[u][v] += 1

    except (OSError, IOError) as e:
        print("Error reading file {}: {}".format(filename, e))
        sys.exit(1)

    f.close()

    return counts, out_degree


def compute_transition(counts, out_degree):
    '''  
    Compute the transition matrix for the graph.  This matrix tells
    us, for each (i,j), the probability that, if the random surfer is
    in node i, the next page they visit is j.

    Inputs:
        counts: (list of lists of int)  matrix of link counts
        out_degree: (list of integers) out-degrees of each node.

    Returns: list of lists of floats representing the transition matrix
    '''

    n = len(out_degree)

    transition_matrix = []
    for i in range(n):
        transition_matrix.append([0]*n)   

    for i in range(n):
        for j in range(n):
            transition_matrix[i][j] = (0.9 * counts[i][j]/out_degree[i]) + (0.1 * 1/n)

    return transition_matrix


def make_one_move(transition_matrix, page):
    '''
    Compute the next page for the random surfer based on the current
    page and the transition matrix

    Inputs:
        transition_matrix: (list of lists of floats)
        page: (int) The current page the random surfer is on

    Returns: (int) next page the random surfer will visit
    '''
    n = len(transition_matrix)
    r = random.uniform(0.0, 1.0)
    psum = 0.0

    for j in range(n):
        psum += transition_matrix[page][j]
        if psum >= r:
            return j


def random_surfer(transition_matrix, num_steps):
    '''
    Simulate the random surfer using the given transition matrix for
    the specified number of steps

    Inputs:
        transition_matrix (list of lists of floats) representing the
            transition matrix  
        num_steps: (int) number of steps to run the simulation

    Returns: Nothing (prints out the rank of each page)
    '''

    n = len(transition_matrix)
    page = 0
    times_visited = [0]*n

    for t in range(num_steps):
        page = make_one_move(transition_matrix, page)
        times_visited[page] += 1

    for count in times_visited:
        v = count / num_steps
        print("{:.3f}".format(v), end=" ")
    print()


def markov_mixing(transition_matrix, num_steps):
    '''
    Compute the page ranks using num_steps vector-matrix
    multiplications.

    Inputs:
        transition_matrix: (list of lists of floats) representing the transition matrix
        num_steps: (int) Number of matrix multiplications to perform

    Returns: Nothing (prints out the rank of each page)
    '''

    n = len(transition_matrix)
    rank = [0]*n
    rank[0] = 1.0

    for t in range(num_steps):
        new_rank = [0]*n

        for i in range(n):
            for j in range(n):
                new_rank[i] = new_rank[i] + rank[j] * transition_matrix[j][i]

        rank = new_rank

    for r in rank:
        print("{:.3f}".format(r), end=" ")
    print()


if __name__ == "__main__":

    if len(sys.argv) != 4 or sys.argv[1] not in ("-r","-m"):
        print("Usage: {} <-r or -m> <file name> <number of steps>".format(sys.argv[0]))
        sys.exit(1)
    
    counts, out_degree = read_graph(sys.argv[2])

    transition_matrix = compute_transition(counts, out_degree)

    num_steps = int(sys.argv[3])

    if sys.argv[1] == "-r":
        random_surfer(transition_matrix, num_steps)
    elif sys.argv[1] == "-m":
        markov_mixing(transition_matrix, num_steps)

