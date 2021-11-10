#!/bin/env python
# The task is to schedule a meeting of four
# friends: Adam, Bridget, Charles, and Darren
# under the following constraints:
# * Adam can only meet on Monday or Wednesday
# * Bridget cannot meet on Wednesday
# * Charles cannot meet on Friday
# * Darren can only meet on Thursday or Friday


# First, we import the initialized sat helper class.
from SatHelper import sh

# Next, we declare the Boolean variables in this problem.
# In this case one Boolean variable for each day of week.

# This Boolean variable is true if and only if the meeting is on Monday
sh.declareVariable("mo")
# This Boolean variable is true if and only if the meeting is on Tuesday
sh.declareVariable("tu")
# This Boolean variable is true if and only if the meeting is on Wednesday
sh.declareVariable("we")
# This Boolean variable is true if and only if the meeting is on Thursday
sh.declareVariable("th")
# This Boolean variable is true if and only if the meeting is on Friday
sh.declareVariable("fr")

# Now we translate the constraints into clauses.

# Adam can only meet on Monday or Wednesday.
sh.addClause(["mo","tu"])
# Bridget cannot meet on Wednesday.
sh.addClause(["-we"])
# Charles cannot meet on Friday.
sh.addClause(["-fr"])
# Darren can only meet on Thursday or Friday.
sh.addClause(["th","fr"])

# The meeting should take place on one 
# of the weekdays, therefore, at most one
# day can be selected.
sh.addAtMostOne(["mo","tu","we","th","fr"])

# Finally, we print the formula
sh.printFormula()

# If a SAT solver named 'glucose' is located in the current folder
# then the following command will use it to solve the formula and
# print the result.
#sh.solveSat()
