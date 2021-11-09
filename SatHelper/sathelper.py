class SatHelper:
    nextIntId = 1
    variableIntMap = {}
    intVariableMap = {}
    clauses = []

    def declareVariable(self, name):
        self.variableIntMap.update({name:self.nextIntId})
        self.intVariableMap.update({self.nextIntId:name})
        self.nextIntId = self.nextIntId+1
    
    def variableToInt(self, name):
        if (name in self.variableIntMap):
            return self.variableIntMap[name]
        else:
            raise ValueError("unknown variable with name: " + name)

    def intToVariable(self, id):
        if (id in self.intVariableMap):
            return self.intVariableMap[id]
        else:
            raise ValueError("unknown variable with id: " + id)

    def literalToInt(self, literal):
        intCode = self.variableToInt(self.getVariableName(literal))
        if (self.isNegated(literal)):
            return -intCode
        else:
            return intCode
    
    @staticmethod
    def isNegated(name):
        return name.startswith("-")
        
    @staticmethod
    def getNegated(name):
        if SatHelper.isNegated(name):
            return SatHelper.getVariableName(name)
        else:
            return "-"+name

    @staticmethod
    def getVariableName(name):
        if SatHelper.isNegated(name):
            return name[1:]
        else:
            return name

    def addClause(self, args):
        clause = ""
        for arg in args:
            clause += str(self.literalToInt(arg))+" "
        clause += "0"
        self.clauses.append(clause)
        
    def addImplies(self, arg1, arg2):
        self.addClause([self.getNegated(arg1), arg2])

    def addEquivalent(self, arg1, arg2):
        self.addImplies(arg1, arg2)
        self.addImplies(arg2, arg1)

    def addAtMostOne(self, args):
        for i in range(len(args)-1):
            for j in range(i+1, len(args)):
                self.addClause([self.getNegated(args[i]), self.getNegated(args[j])])

    def addExactlyOne(self, args):
        self.addClause(args)
        self.addAtMostOne(args)
        
    def printFormula(self):
        print("p cnf", self.nextIntId-1, len(self.clauses))
        for clause in self.clauses:
            print(clause)
            
    def printClauseToForceDifferentSolution(self, solution):
        otherSolClause = ""
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                otherSolClause+=str(-value)+" "
        print(otherSolClause + "0")

    def printTrueVariables(self, solution):
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                print(self.intToVariable(value))
