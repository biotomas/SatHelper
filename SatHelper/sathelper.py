import subprocess
import sys

class SatHelper:
    nextIntId = 1
    variableIntMap = {}
    intVariableMap = {}
    clauses = []
    softClauses = []
    softClauseTotalWeight = 0

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

    def literalsToIntString(self, args):
        clause = ""
        for arg in args:
            clause += str(self.literalToInt(arg))+" "
        clause += "0"
        return clause

    def addClause(self, literals):
        self.clauses.append(self.literalsToIntString(literals))

    def addSoftClause(self, literals):
        self.addWeightedSoftClause(1, literals)
        
    def addWeightedSoftClause(self, weight, literals):
        self.softClauseTotalWeight += weight
        self.softClauses.append(str(weight) + " " + self.literalsToIntString(literals))
           
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
            
    def printMaxSatFormula(self):
        hardClauseWeight = self.softClauseTotalWeight + 1
        print("p wcnf", self.nextIntId-1, len(self.clauses)+len(self.softClauses), hardClauseWeight)
        for clause in self.clauses:
            print(hardClauseWeight, clause)
        for softClause in self.softClauses:
            print(softClause)
            
    def solveSat(self):
        original_stdout = sys.stdout
        with open('formula.cnf', 'w') as f:
            sys.stdout = f
            self.printFormula()
            sys.stdout = original_stdout # Reset the standard output to its original value
            
        p = subprocess.run(["./glucose", "-model", "formula.cnf"], stdout=subprocess.PIPE, universal_newlines=True)
        solution = list(filter(lambda line: line.startswith("s "), p.stdout.splitlines()))[0][2:]
        print("The formula is", solution)
        if solution == "SATISFIABLE":
            values = list(filter(lambda line: line.startswith("v "), p.stdout.splitlines()))[0][2:]
            self.printTrueVariables(values)
            
    def solveMaxSat(self):
        original_stdout = sys.stdout
        with open('formula.cnf', 'w') as f:
            sys.stdout = f
            self.printMaxSatFormula()
            sys.stdout = original_stdout # Reset the standard output to its original value
            
        p = subprocess.run(["./open-wbo", "formula.cnf"], stdout=subprocess.PIPE, universal_newlines=True)
        solution = list(filter(lambda line: line.startswith("s "), p.stdout.splitlines()))[0][2:]
        print("The result is", solution)
        if solution == "OPTIMUM FOUND":
            values = list(filter(lambda line: line.startswith("v "), p.stdout.splitlines()))[0][2:]
            self.printTrueVariablesCompact(values)
            
    def printClauseToForceDifferentSolution(self, solution):
        otherSolClause = ""
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                otherSolClause+=str(-value)+" "
        print(otherSolClause + "0")

    def printTrueVariables(self, solution):
        print("The following variables are assigned the value True:")
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                print(self.intToVariable(value))
                
    def printTrueVariablesCompact(self, solution):
        print("The following variables are assigned the value True:")
        for index in range(len(solution)):
            if (solution[index] == "1"):
                print(self.intToVariable(index+1))

