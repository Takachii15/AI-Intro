# multiAgents.py
# --------------
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

from util import manhattanDistance
from game import Directions
import random
import util
from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation
        function.

        Just like in the previous project, getAction takes a GameState and
        returns
        some Directions.X for some X in the set
        {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [
            self.evaluationFunction(gameState, action) for action in legalMoves
        ]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(
            bestIndices)  # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)

        # all relevant component needed
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates
        ]

        near_ghost = 1e9
        # find nearest ghost distance
        for ghost in newGhostStates:
            if newScaredTimes == 0:
                near_ghost = min(
                    near_ghost, manhattanDistance(ghost.getPosition(), newPos)
                    )

        near_food = 1e9
        # find nearest food distance
        for food in newFood.asList():
            near_food = min(near_food, manhattanDistance(food, newPos))

        # if there's no food then distance is 0
        if not newFood.asList():
            near_food = 0

        final_score = (
            childGameState.getScore() - 7 / (near_ghost + 1) - near_food / 3
        )

        return final_score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


# TODO: Minimax

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing
        minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        return self.minimaxSearch(gameState, agentIndex=0, depth=self.depth)[1]

    def minimaxSearch(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), 'STOP'
        if agentIndex == 0:
            return self.maximizer(gameState, agentIndex, depth)
        else:
            return self.minimizer(gameState, agentIndex, depth)

    def maximizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent = 0
            next_depth = depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        max_score = float('-inf')
        max_action = 'STOP'
        for action in actions:
            successor_game_state = gameState.getNextState(agentIndex, action)
            new_score = self.minimaxSearch(
                successor_game_state, next_agent, next_depth)[0]
            if new_score > max_score:
                max_score, max_action = new_score, action
        return max_score, max_action

    def minimizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent = 0
            next_depth = depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        min_score = float('inf')
        min_action = 'STOP'
        for action in actions:
            successor_game_state = gameState.getNextState(agentIndex, action)
            new_score = self.minimaxSearch(
                successor_game_state, next_agent, next_depth)[0]
            if new_score < min_score:
                min_score, min_action = new_score, action
        return min_score, min_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaSearch(
            gameState, 0, self.depth, float('-inf'), float('inf'))[1]

    def alphaBetaSearch(self, gameState, agentIndex, depth, alpha, beta):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), 'STOP'
        if agentIndex == 0:
            return self.alpha(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.beta(gameState, agentIndex, depth, alpha, beta)

    def alpha(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent = 0
            next_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            next_depth = depth
        max_score = float('-inf')
        max_action = 'STOP'
        for action in actions:
            successor_game_state = gameState.getNextState(agentIndex, action)
            new_score = self.alphaBetaSearch(
                successor_game_state, next_agent, next_depth, alpha, beta)[0]
            if new_score > max_score:
                max_score, max_action = new_score, action
            if new_score > beta:
                return new_score, action
            alpha = max(alpha, max_score)
        return max_score, max_action

    def beta(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent = 0
            next_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            next_depth = depth
        min_score = float('inf')
        min_action = 'STOP'
        for action in actions:
            successor_game_state = gameState.getNextState(agentIndex, action)
            new_score = self.alphaBetaSearch(
                successor_game_state, next_agent, next_depth, alpha, beta)[0]
            if new_score < min_score:
                min_score, min_action = new_score, action
            if new_score < alpha:
                return new_score, action
            beta = min(beta, min_score)
        return min_score, min_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and
        self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, 0, self.depth)[1]

    def expectimax(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), 'STOP'
        if agentIndex == 0:
            return self.maximizer(gameState, agentIndex, depth)
        else:
            return self.expectation(gameState, agentIndex, depth)

    def maximizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent = 0
            next_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            next_depth = depth
        max_score = float('-inf')
        max_action = 'STOP'
        for action in actions:
            successor_game_state = gameState.getNextState(agentIndex, action)
            new_score = self.expectimax(
                successor_game_state, next_agent, next_depth)[0]
            if new_score > max_score:
                max_score, max_action = new_score, action
        return max_score, max_action

    def expectation(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent = 0
            next_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            next_depth = depth
        exp_score = 0
        exp_action = 'STOP'
        for action in actions:
            successor_game_state = gameState.getNextState(agentIndex, action)
            exp_score = exp_score + self.expectimax(
                successor_game_state, next_agent, next_depth)[0]
        exp_score = exp_score / len(actions)
        return exp_score, exp_action


def betterEvaluationFunction(currentGameState):
    # all relevant component needed
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [
        ghostState.scaredTimer for ghostState in newGhostStates
    ]

    near_ghost = 1e9
    # find nearest ghost distance
    for ghost in newGhostStates:
        if newScaredTimes == 0:
            near_ghost = min(
                near_ghost, manhattanDistance(ghost.getPosition(), newPos)
                )

    near_food = 1e9
    # find nearest food distance
    for food in newFood.asList():
        near_food = min(near_food, manhattanDistance(food, newPos))

    # if there's no food distance is 0
    if not newFood.asList():
        near_food = 0

    final_score = (
        currentGameState.getScore() - 7 / (near_ghost + 1) - near_food / 3
    )
    return final_score

    # util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
