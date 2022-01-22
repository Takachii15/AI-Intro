# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from bayesNet import Factor
import operator as op
import util
import functools


def joinFactorsByVariableWithCallTracking(callTrackingList=None):
    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin = [
            factor for factor in factors
            if joinVariable in factor.variablesSet()
        ]
        currentFactorsNotToJoin = [
            factor for factor in factors
            if joinVariable not in factor.variablesSet()
        ]

        # typecheck portion
        numVariableOnLeft = len([
            factor for factor in currentFactorsToJoin
            if joinVariable in factor.unconditionedVariables()
        ])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError(
                "The joinBy variable can only appear in one factor as an \nunconditioned variable. \n"
                + "joinVariable: " + str(joinVariable) + "\n" + ", ".join(
                    map(str, [
                        factor.unconditionedVariables()
                        for factor in currentFactorsToJoin
                    ])))

        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable


joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation

    Input factors is a list of factors.

    You should calculate the set of unconditioned variables and conditioned
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input
    (such as getProbability and setProbability) can handle
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [
        set(factor.unconditionedVariables()) for factor in factors
    ]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError(
                "unconditionedVariables can only appear in one factor. \n" +
                "unconditionedVariables: " + str(intersect) +
                "\nappear in more than one input factor.\n" +
                "Input factors: \n" + "\n".join(map(str, factors)))

    "*** YOUR CODE HERE ***"
    variableDicts = {}
    conditionedVars = []
    unconditionedVars = []

    for factor in factors:
        # Store variables domain dict
        variableDicts = factor.variableDomainsDict()

        # Get unconditioned variables from setOfUnconditioned
        if len(factor.unconditionedVariables()) > 1:
            for var in factor.unconditionedVariables():
                unconditionedVars.append(var)
        else:
            unconditionedVars.append(str(
                factor.unconditionedVariables().pop()))

        # store list of conditioned variables
        if factor.conditionedVariables() == set():
            continue
        elif not str(sorted(
                factor.conditionedVariables()).pop()) in conditionedVars:
            conditionedVars.append(
                str(sorted(factor.conditionedVariables()).pop()))

    temp = list(conditionedVars)
    for var in temp:
        if var in unconditionedVars:
            conditionedVars.remove(var)

    fact = Factor(unconditionedVars, conditionedVars, variableDicts)
    finalDicts = fact.getAllPossibleAssignmentDicts()

    for dict in finalDicts:
        fact.setProbability(dict, 1)

    for finalDict in finalDicts:
        finalKeyList = list(finalDict.keys())

        for factor in factors:
            dicts = factor.getAllPossibleAssignmentDicts()
            for dict in dicts:
                keyList = list(dict.keys())
                if set(keyList).issubset(set(finalKeyList)):
                    tempVal = 1
                    for key in keyList:
                        if not dict[key] == finalDict[key]:
                            tempVal = 0
                    if tempVal == 1:
                        fact.setProbability(
                            finalDict,
                            fact.getProbability(finalDict) *
                            factor.getProbability(dict))

    print(variableDicts)
    return fact
    "*** END YOUR CODE HERE ***"


def eliminateWithCallTracking(callTrackingList=None):
    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" +
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))

        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
        variableDicts = {}
        conditionedVars = []
        unconditionedVars = []

        tempDicts = factor.getAllPossibleAssignmentDicts()

        for var in factor.unconditionedVariables():
            if not var == eliminationVariable:
                unconditionedVars.append(var)

        for var in factor.conditionedVariables():
            if not var == eliminationVariable:
                conditionedVars.append(var)

        temp = []
        for dict in tempDicts:
            keyList = list(dict.keys())
            for key in keyList:
                if not key == eliminationVariable:
                    if key not in temp:
                        temp2 = []
                        temp.append(key)
                        for anotherDict in tempDicts:
                            if not anotherDict[key] in temp2:
                                temp2.append(anotherDict[key])
                        variableDicts[key] = temp2

        # set new factor as 'Fact'
        fact = Factor(
            unconditionedVars, conditionedVars, factor.variableDomainsDict())

        finalDicts = fact.getAllPossibleAssignmentDicts()

        for finalDict in finalDicts:
            finalKeys = list(finalDict.keys())
            finalKeyProb = 0
            for dict in tempDicts:
                if set(finalKeys).issubset(set(list(dict.keys()))):
                    val = 1
                    for finalKey in finalKeys:
                        if not dict[finalKey] == finalDict[finalKey]:
                            val = 0
                    if val == 1:
                        finalKeyProb = finalKeyProb + factor.getProbability(
                            dict)

            fact.setProbability(finalDict, finalKeyProb)

        return fact
        "*** END YOUR CODE HERE ***"

    return eliminate


eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists
    of the input factor's conditioned variables as well as any of the
    input factor's unconditioned variables with exactly one entry in their
    domain.  Since there is only one entry in that variable's domain, we
    can either assume it was assigned as evidence to have only one variable
    in its domain, or it only had one entry in its domain to begin with.
    This blurs the distinction between evidence assignments and variables
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table
    is 1. This should be a new factor, not a modification of this factor in 
    place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print("Factor failed normalize typecheck: ", factor)
            raise ValueError("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" +
                            str(factor))

    "*** YOUR CODE HERE ***"
    alpha = 0
    variableDicts = factor.variableDomainsDict()
    conditionedVars = list(factor.conditionedVariables())
    unconditionedVars = sorted(factor.unconditionedVariables())

    evidence = {}
    temp = list(unconditionedVars)
    for var in temp:
        if len(variableDicts[var]) == 1:
            conditionedVars.append(var)
            unconditionedVars.remove(var)
            evidence[var] = variableDicts[var]

    evidenceKeyList = list(evidence.keys())

    # result factor set as 'Fact'
    fact = Factor(
        unconditionedVars, conditionedVars, factor.variableDomainsDict())

    for dict in factor.getAllPossibleAssignmentDicts():
        flag = 1
        for key in evidenceKeyList:
            if not str(dict[key]) == evidence[key][0]:
                flag = 0
        if flag == 1:
            alpha = alpha + factor.getProbability(dict)

    if alpha == 0:
        return None

    alpha = 1 / alpha

    for dict in factor.getAllPossibleAssignmentDicts():
        fact.setProbability(dict, alpha * factor.getProbability(dict))

    return fact
    "*** END YOUR CODE HERE ***"
