#!/bin/env python
# The task is to find a maximum clique in a given graph.
# See https://en.wikipedia.org/wiki/Clique_problem
# In this example we will encode to Partial Maximum Satisfiability

# First, we import the initialized sat helper class.
from SatHelper import sh
import numpy as np

# Read graph from input file. We will represent the graph
# in the form of an incidence matrix called 'matrix'
f = open("data/graph.dimacs", "r")
lines = f.readlines()
f.close()

for line in lines:
   if line.startswith("c "):
      continue
   if line.startswith("p edge"):
   	parts = line.split(" ")
   	vertices = int(parts[2])
   	matrix = np.zeros((vertices+1,vertices+1))
   if line.startswith("e "):
      parts = line.split(" ")
      vertex1 = int(parts[1])
      vertex2 = int(parts[2])
      matrix[vertex1, vertex2] = 1
      matrix[vertex2, vertex1] = 1

# Declare the Boolean variables, one variable for each vertex
# which represents whether the given vertex is in the clique
for v in range(1, vertices+1):
	sh.declareVariable("v"+str(v))
	
# Add hard clauses to say that if there is no edge between two
# vertices then they cannot both be in the clique
for vertex1 in range(1,vertices+1):
	for vertex2 in range(vertex1+1,vertices+1):
		# if there is no edge between vertex1 and vertex2
	   if (matrix[vertex1,vertex2] == 0):
			# add a clause that allows at most one of them in the clique
			sh.addClause(["-v"+str(vertex1), "-v"+str(vertex2)])

# Add unit soft clauses for each vertex, we want to have as
# many vertices as possible in the clique
for v in range(1, vertices+1):
	sh.addSoftClause(["v"+str(v)])

sh.printMaxSatFormula()

# If a MaxSAT solver named 'open-wbo' is located in the current folder
# then the following command will use it to solve the formula and
# print the result.

#sh.solveMaxSat()

