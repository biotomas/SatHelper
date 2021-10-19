# The task is to solve a logical puzzle called Einstein's puzzle
# also known as the Zebra Puzzle (https://en.wikipedia.org/wiki/Zebra_Puzzle)
#
# The Puzzle: There are five houses of different colors next to each 
# other on the same road. In each house lives a man of a different nationality. 
# Every man has his favorite drink, his favorite brand of cigarettes, 
# and keeps pets of a particular kind. The question to be answered is: Who keeps fish?
# Hints:
# (1)  The Englishman lives in the red house.
# (2)  The Swede keeps dogs.
# (3)  The Dane drinks tea.
# (4)  The green house is just to the left of the white one.
# (5)  The owner of the green house drinks coffee.
# (6)  The Pall Mall smoker keeps birds.
# (7)  The owner of the yellow house smokes Dunhills.
# (8)  The man in the center house drinks milk.
# (9)  The Norwegian lives in the first house.
# (10) The Blend smoker has a neighbor who keeps cats.
# (11) The man who smokes Blue Masters drinks bier.
# (12) The man who keeps horses lives next to the Dunhill smoker.
# (13) The German smokes Prince.
# (14) The Norwegian lives next to the blue house.
# (15) The Blend smoker has a neighbor who drinks water.

import sathelper
sh = sathelper.SatHelper()

# From the hints we can extract the following categories and values
houses = ["h1","h2","h3","h4","h5"]
colors = ["red","green","blue","yellow","white"]
nationality = ["english","swede","dane","norwegian","german"]
cigarettes = ["pall-mall","dunhill","blend","blue-masters","prince"]
drink = ["tea","coffee","milk","bier","water"]
pet = ["dog","bird","cat","horse","fish"]

# Now we can declare the variables.
# For each house and each value from all the categories
# we have one Boolean variable, like "h1,green", "h4,dog", ...
# meaning "house 1 is green", "h4 owner has a dog", ...
for house in houses:
    for x in colors: sh.declareVariable(house+","+x)
    for x in nationality: sh.declareVariable(house+","+x)
    for x in cigarettes: sh.declareVariable(house+","+x)
    for x in drink: sh.declareVariable(house+","+x)
    for x in pet: sh.declareVariable(house+","+x)

# Now we translate all the rules of type "if a house has
# property A then it has property B" by adding an equivalence
# for each house. For example "The Englishman lives in the red house"
# gets translated to 5 equivalences like "h1,english is equivalent
# to h1,red", "h2,english is equivalent to h2,red", ...
for house in houses:
    #1 englishman lives in red house
    sh.addEquivalent(house+",english", house+",red")
    #2 sweede has dogs
    sh.addEquivalent(house+",swede", house+",dog")
    #3 dane drinks tea
    sh.addEquivalent(house+",dane", house+",tea")
    #5 green drinks coffee
    sh.addEquivalent(house+",green", house+",coffee")
    #6 pall mal keep birds
    sh.addEquivalent(house+",pall-mall", house+",bird")
    #7 yellow smokes dunhill
    sh.addEquivalent(house+",yellow", house+",dunhill")
    #11 blue-masters drinks bier
    sh.addEquivalent(house+",blue-masters", house+",bier")
    #13 german smokes prince
    sh.addEquivalent(house+",german", house+",prince")
    
# Now the rules about neighbouring houses

#4 green house is left of white
sh.addEquivalent("h1,green","h2,white")
sh.addEquivalent("h2,green","h3,white")
sh.addEquivalent("h3,green","h4,white")
sh.addEquivalent("h4,green","h5,white")

#8 center house drinks milk
sh.addClause(["h3,milk"])

#9 norwegian in first house
sh.addClause(["h1,norwegian"])

#10 blend has neighbour with cats
sh.addEquivalent("h1,blend","h2,cat")
sh.addClause(["-h2,blend","h1,cat","h3,cat"])
sh.addClause(["-h3,blend","h2,cat","h4,cat"])
sh.addClause(["-h4,blend","h3,cat","h5,cat"])
sh.addEquivalent("h5,blend","h4,cat")

#12 horses has neighbour with dunhill
sh.addEquivalent("h1,horse","h2,dunhill")
sh.addClause(["-h2,horse","h1,dunhill","h3,dunhill"])
sh.addClause(["-h3,horse","h2,dunhill","h4,dunhill"])
sh.addClause(["-h4,horse","h3,dunhill","h5,dunhill"])
sh.addEquivalent("h5,horse","h4,dunhill")

#14 norwegian next to blue
sh.addEquivalent("h1,norwegian","h2,blue")
sh.addClause(["-h2,norwegian","h1,blue","h3,blue"])
sh.addClause(["-h3,norwegian","h2,blue","h4,blue"])
sh.addClause(["-h4,norwegian","h3,blue","h5,blue"])
sh.addEquivalent("h5,norwegian","h4,blue")

#15 blend next to water
sh.addEquivalent("h1,blend","h2,water")
sh.addClause(["-h2,blend","h1,water","h3,water"])
sh.addClause(["-h3,blend","h2,water","h4,water"])
sh.addClause(["-h4,blend","h3,water","h5,water"])
sh.addEquivalent("h5,blend","h4,water")

# This little helper function will be useful later.
# It adds a given prefix to each string in the 
# given list.
def addPrefix(prefix, list):
    result = []
    for item in list:
        result.append(prefix+","+item)
    return result

#at least one color/drink/cigarettes/... assigned to each house
for house in houses:
    sh.addClause(addPrefix(house, colors))
    sh.addClause(addPrefix(house, drink))
    sh.addClause(addPrefix(house, cigarettes))
    sh.addClause(addPrefix(house, pet))
    sh.addClause(addPrefix(house, nationality))

# each color/drink/cigarettes/... is assigned to at most one house
for x in colors: sh.addAtMostOne(["h1,"+x,"h2,"+x,"h3,"+x,"h4,"+x,"h5,"+x])
for x in nationality: sh.addAtMostOne(["h1,"+x,"h2,"+x,"h3,"+x,"h4,"+x,"h5,"+x])
for x in cigarettes: sh.addAtMostOne(["h1,"+x,"h2,"+x,"h3,"+x,"h4,"+x,"h5,"+x])
for x in drink: sh.addAtMostOne(["h1,"+x,"h2,"+x,"h3,"+x,"h4,"+x,"h5,"+x])
for x in pet: sh.addAtMostOne(["h1,"+x,"h2,"+x,"h3,"+x,"h4,"+x,"h5,"+x])

# print the formula for the SAT solver
sh.printFormula()

# here you can copy the result from
# the SAT solver to see solution
result = "-1 -2 -3 4 -5 -6 -7 -8 9 -10 -11 12 -13 -14 -15 -16 -17 -18 -19 20 -21 -22 23 -24 -25 -26 -27 28 -29 -30 -31 -32 33 -34 -35 -36 -37 38 -39 -40 41 -42 -43 -44 -45 -46 -47 -48 49 -50 51 -52 -53 -54 -55 56 -57 -58 -59 -60 61 -62 -63 -64 -65 -66 -67 68 -69 -70 -71 72 -73 -74 -75 -76 77 -78 -79 -80 -81 -82 -83 -84 85 -86 -87 -88 -89 90 -91 92 -93 -94 -95 -96 -97 -98 -99 100 -101 -102 -103 -104 105 -106 107 -108 -109 -110 -111 -112 -113 114 -115 -116 -117 -118 119 -120 121 -122 -123 -124 -125 0"

# this command will the print the variables that are True in result
# sh.printTrueVariables(result)

# with the following command you can print a clause
# that will require a different solution than the given solution
# sh.printClauseToForceDifferentSolution(result)