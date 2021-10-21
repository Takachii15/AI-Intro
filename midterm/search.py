# search.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implemen
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """

        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of
        the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state
        after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class CostNode:
    def __init__(self, state, parent, action, fcost):
        self.state = state
        self.parent = parent
        self.action = action
        self.fcost = fcost


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    frontier = util.Stack()
    visited = []
    solution = []

    frontier.push(Node(problem.getStartState(), None, None))
    while frontier.isEmpty() is False:
        node = frontier.pop()
        if problem.isGoalState(node.state) is True:
            tmp = []
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                tmp.append(node.state)
                node = node.parent
            actions.reverse()
            tmp.append(node.state)
            tmp.reverse()
            solution = tmp
            print("E2 = ", solution)
            return actions
        visited.append(node.state)
        for i in problem.expand(node.state):
            if i[0] not in visited:
                frontier.push(Node(i[0], node, i[1]))


def depthFirstSearchT2(problem):
    frontier = util.Stack()
    visited = []
    solution = []

    frontier.push(Node(problem.getStartState(), None, None))
    while frontier.isEmpty() is False:
        node = frontier.pop()
        solution = []
        if problem.isGoalState(node.state) is True:
            tmp = []
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                tmp.append(node.state)
                node = node.parent
            actions.reverse()
            # print("E2 = ", solution)
            return actions
        visited.append(node.state)
        for i in problem.expand(node.state):
            if i[0] not in visited:
                frontier.push(Node(i[0], node, i[1]))
                print(i[0])


def breadthFirstSearch(problem):
    frontier = util.Queue()
    visited = []

    frontier.push(Node(problem.getStartState(), None, None))
    while frontier.isEmpty() is False:
        node = frontier.pop()
        if problem.isGoalState(node.state) is True:
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent
            actions.reverse()
            return actions

        visited.append(node.state)
        for i in problem.expand(node.state):
            frontierState = []
            for j in frontier.list:
                frontierState.append(j.state)
            if i[0] not in visited and i[0] not in frontierState:
                frontier.push(Node(i[0], node, i[1]))


def nullHeuristic(state, problem=None):
    return 0

# TODO: Implement heuristic cost concept to code

# f(n) = g(n) + h(n)
# implement something


def aStarSearch(problem, heuristic=nullHeuristic):
    frontier = util.PriorityQueue()
    visited = []

    frontier.push(CostNode(problem.getStartState(), None, None, 0), 0)
    while frontier.isEmpty() is False:
        node = frontier.pop()
        if problem.isGoalState(node.state) is True:
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent
            actions.reverse()
            return actions

        if (node.state not in visited):
            visited.append(node.state)
            for i in problem.expand(node.state):
                frontierState = []
                for j in frontier.heap:
                    frontierState.append(j[0])
                cost = i[2] + node.fcost
                fcost = cost + heuristic(i[0], problem)
                if i[0] not in visited and i[0] not in frontierState:
                    # print(fcost)
                    frontier.update(CostNode(i[0], node, i[1], fcost), fcost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
dfs2 = depthFirstSearchT2
