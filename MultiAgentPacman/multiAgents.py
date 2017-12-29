# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

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

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    if successorGameState.isWin():
        return float("inf") - 20
    ghostposition = currentGameState.getGhostPosition(1)
    distancefromghost = util.manhattanDistance(ghostposition, newPos)
    score = max(distancefromghost, 3) + successorGameState.getScore()
    foodlist = newFood.asList()
    closestfood = 100
    for foodpos in foodlist:
        thisdist = util.manhattanDistance(foodpos, newPos)
        if (thisdist < closestfood):
            closestfood = thisdist
    if (currentGameState.getNumFood() > successorGameState.getNumFood()):
        score = score + 100
    if action == Directions.STOP:
        score = score - 3
    score = score - 3 * closestfood
    capsuleplaces = currentGameState.getCapsules()
    if successorGameState.getPacmanPosition() in capsuleplaces:
        score = score + 120
    return score
    # return successorGameState.getScore()

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    def maxvalue(gameState, depth, numghosts):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)
      v = -(float("inf"))
      legalActions = gameState.getLegalActions(0)
      for action in legalActions:
        v = max(v, minvalue(gameState.generateSuccessor(0, action), depth - 1, 1, numghosts))
      return v

    def minvalue(gameState, depth, agentindex, numghosts):
      "numghosts = len(gameState.getGhostStates())"
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)
      v = float("inf")
      legalActions = gameState.getLegalActions(agentindex)
      if agentindex == numghosts:
        for action in legalActions:
          v = min(v, maxvalue(gameState.generateSuccessor(agentindex, action), depth - 1, numghosts))
      else:
        for action in legalActions:
          v = min(v, minvalue(gameState.generateSuccessor(agentindex, action), depth, agentindex + 1, numghosts))
      return v

    legalActions = gameState.getLegalActions()
    numghosts = gameState.getNumAgents() - 1
    bestaction = Directions.STOP
    score = -(float("inf"))
    for action in legalActions:
      nextState = gameState.generateSuccessor(0, action)
      prevscore = score
      score = max(score, minvalue(nextState, self.depth, 1, numghosts))
      if score > prevscore:
        bestaction = action
    return bestaction

    util.raiseNotDefined()



    # agentIndex = 0
    # terminal_state = Directions.STOP
    # actions = gameState.getLegalActions(agentIndex)
    # v = float('-inf')
    #
    # if gameState.getLegalActions(agentIndex) == terminal_state:
    #     return gameState.getLegalActions(agentIndex)
    #
    # for a in actions:
    #     nextAction = gameState.generateSuccessor(agentIndex, a)
    #
    #
    #
    # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"

    # alpha = float('-inf')
    # beta = float('inf')
    #
    # def max_value(state, agentIndex, alpha, beta):
    #     v = float('-inf')
    #
    #     for action in gameState.getLegalActions:
    #         v = max(v, self.min_value(state.generateSuccessor(agentIndex, action),agentIndex + 1, aplha, beta))
    #         if v >= beta:
    #             return  v
    #         alpha = max(alpha, v)
    #     return v
    #
    # def min_value(state, agentIndex, alpha, beta):
    #     v =  float('inf')
    #     for action in gameState.getLegalActions:
    #         v = min(v, self.max_value(state.generateSuccessor(agentIndex, action), agentIndex + 1, aplha, beta))
    #         if v <= alpha:
    #             return v
    #         beta = min(beta, v)
    #     return v

    def maxvalue(gameState, alpha, beta, depth):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)
      v = -(float("inf"))
      legalActions = gameState.getLegalActions(0)
      for action in legalActions:
        nextState = gameState.generateSuccessor(0, action)
        v = max(v, minvalue(nextState, alpha, beta, gameState.getNumAgents() - 1, depth))
        if v >= beta:
          return v
        alpha = max(alpha, v)
      return v

    def minvalue(gameState, alpha, beta, agentindex, depth):
      numghosts = gameState.getNumAgents() - 1
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)
      v = float("inf")
      legalActions = gameState.getLegalActions(agentindex)
      for action in legalActions:
        nextState = gameState.generateSuccessor(agentindex, action)
        if agentindex == numghosts:
          v = min(v, maxvalue(nextState, alpha, beta, depth - 1))
          if v <= alpha:
            return v
          beta = min(beta, v)
        else:
          v = min(v, minvalue(nextState, alpha, beta, agentindex + 1, depth))
          if v <= alpha:
            return v
          beta = min(beta, v)
      return v

    legalActions = gameState.getLegalActions(0)
    bestaction = Directions.STOP
    score = -(float("inf"))
    alpha = -(float("inf"))
    beta = float("inf")
    for action in legalActions:
      nextState = gameState.generateSuccessor(0, action)
      prevscore = score
      score = max(score, minvalue(nextState, alpha, beta, 1, self.depth))
      if score > prevscore:
        bestaction = action
      if score >= beta:
        return bestaction
      alpha = max(alpha, score)
    return bestaction

    util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"

    def maxvalue(gameState, depth):
      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)
      v = -(float("inf"))
      legalActions = gameState.getLegalActions(0)

      for action in legalActions:
        nextState = gameState.generateSuccessor(0, action)
        v = max(v, avgvalue(nextState, gameState.getNumAgents() - 1, depth))
        # if v >= beta:
        #   return v
        # alpha = max(alpha, v)
      return v

    def avgvalue(gameState, agentindex, depth):
      sum = 0

      numghosts = gameState.getNumAgents() - 1

      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      v = float("inf")

      legalActions = gameState.getLegalActions(agentindex)

      for action in legalActions:
        nextState = gameState.generateSuccessor(agentindex, action)
        if agentindex == numghosts:
          sum = sum + maxvalue(nextState, depth - 1)

          # if v <= alpha:
          #   return v
          # beta = min(beta, v)

        else:
          sum = sum + avgvalue(nextState, agentindex + 1, depth)
          # if v <= alpha:
          #   return v
          # beta = min(beta, v)
        v = sum/(len(legalActions))
      return v

    legalActions = gameState.getLegalActions(0)
    bestaction = Directions.STOP
    score = -(float("inf"))
    # alpha = -(float("inf"))
    # beta = float("inf")
    for action in legalActions:
      nextState = gameState.generateSuccessor(0, action)
      prevscore = score
      score = max(score, avgvalue(nextState, 1, self.depth))

      if score > prevscore:
        bestaction = action

      # if score >= beta:
      #   return bestaction
      #
      # alpha = max(alpha, score)
    return bestaction

    util.raiseNotDefined()

  """
  Name: BetterEvaluationFunction
  Purpose:  To be a better evaluation function than the default
  Precondition: the current state of the game is known.  This means we can 
                determine distance between pacman and the nearest "live" ghost,
                how many capsules are left, number of food left and nearest 
                food to pacman.
  Postcondition:Pacman is able to get optimal points because of a mix of rules 
                determining score for eating ghosts in a particular state and 
                relative distance from pacman vs pellets with relative to
                Pacman.
  Notes: Default behavior of pacman didn't take advantage of scared ghosts and 
         focused on food pellets. The idea of the algorithm is to "encourage" 
         Pacman to eat the scared ghost when they appear, but also create a 
         penalty for not approaching available food.  
         In other words, to go after the ghosts, it had to be worth ignoring 
         food.  Also, the further Pacman is away from the food, the higher the
         negative value is.  This range (which I found online and others 
         suggested to me) was between -1.5 and -4.  Because we want Pacman to
         go after scared ghosts when they are available (and within a good
         distance, we make a larger negative value to reinforce the strategy.
         
         Credit to Dan Sway's pseudocode at UC Berkeley
  """
def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  pos = currentGameState.getPacmanPosition()
  currentScore = scoreEvaluationFunction(currentGameState)

  if currentGameState.isLose():
      return -float("inf")
  elif currentGameState.isWin():
      return float("inf")

  # food distance
  foodlist = currentGameState.getFood().asList()
  manhattanDistanceToClosestFood = min(map(lambda x: util.manhattanDistance(pos, x), foodlist))
  distanceToClosestFood = manhattanDistanceToClosestFood

  # number of big dots
  # if we only count the number fo them, he'll only care about
  # them if he has the opportunity to eat one.
  numberOfCapsulesLeft = len(currentGameState.getCapsules())

  # number of foods left
  numberOfFoodsLeft = len(foodlist)

  # ghost distance

  # active ghosts are ghosts that aren't scared.
  scaredGhosts, activeGhosts = [], []
  for ghost in currentGameState.getGhostStates():
      if not ghost.scaredTimer:
          activeGhosts.append(ghost)
      else:
          scaredGhosts.append(ghost)

  def getManhattanDistances(ghosts):
      return map(lambda g: util.manhattanDistance(pos, g.getPosition()), ghosts)

  distanceToClosestActiveGhost = distanceToClosestScaredGhost = 0

  if activeGhosts:
      distanceToClosestActiveGhost = min(getManhattanDistances(activeGhosts))
  else:
      distanceToClosestActiveGhost = float("inf")
  distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)

  if scaredGhosts:
      distanceToClosestScaredGhost = min(getManhattanDistances(scaredGhosts))
  else:
      distanceToClosestScaredGhost = 0  # I don't want it to count if there aren't any scared ghosts

  outputTable = [["dist to closest food", -1.5 * distanceToClosestFood],
                 ["dist to closest active ghost", 2 * (1. / distanceToClosestActiveGhost)],
                 ["dist to closest scared ghost", 2 * distanceToClosestScaredGhost],
                 ["number of capsules left", -3.5 * numberOfCapsulesLeft],
                 ["number of total foods left", 2 * (1. / numberOfFoodsLeft)]]

  score = 1 * currentScore + \
          -1.5 * distanceToClosestFood + \
          -2 * (1. / distanceToClosestActiveGhost) + \
          -2 * distanceToClosestScaredGhost + \
          -25 * numberOfCapsulesLeft + \
          -5 * numberOfFoodsLeft


  return score

  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """




  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    currentScore = scoreEvaluationFunction(currentGameState)

    if currentGameState.isLose():
        return -float("inf")
    elif currentGameState.isWin():
        return float("inf")

    # food distance
    foodlist = currentGameState.getFood().asList()
    manhattanDistanceToClosestFood = min(map(lambda x: util.manhattanDistance(pos, x), foodlist))
    distanceToClosestFood = manhattanDistanceToClosestFood

    # number of big dots
    # if we only count the number fo them, he'll only care about
    # them if he has the opportunity to eat one.
    numberOfCapsulesLeft = len(currentGameState.getCapsules())

    # number of foods left
    numberOfFoodsLeft = len(foodlist)

    # ghost distance

    # active ghosts are ghosts that aren't scared.
    scaredGhosts, activeGhosts = [], []
    for ghost in currentGameState.getGhostStates():
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else:
            scaredGhosts.append(ghost)

    def getManhattanDistances(ghosts):
        return map(lambda g: util.manhattanDistance(pos, g.getPosition()), ghosts)

    distanceToClosestActiveGhost = distanceToClosestScaredGhost = 0

    if activeGhosts:
        distanceToClosestActiveGhost = min(getManhattanDistances(activeGhosts))
    else:
        distanceToClosestActiveGhost = float("inf")
    distanceToClosestActiveGhost = max(distanceToClosestActiveGhost, 5)

    if scaredGhosts:
        distanceToClosestScaredGhost = min(getManhattanDistances(scaredGhosts))
    else:
        distanceToClosestScaredGhost = 0  # I don't want it to count if there aren't any scared ghosts

    outputTable = [["dist to closest food", -1.5 * distanceToClosestFood],
                   ["dist to closest active ghost", 2 * (1. / distanceToClosestActiveGhost)],
                   ["dist to closest scared ghost", 2 * distanceToClosestScaredGhost],
                   ["number of capsules left", -3.5 * numberOfCapsulesLeft],
                   ["number of total foods left", 2 * (1. / numberOfFoodsLeft)]]

    score = 1 * currentScore + \
            -1.5 * distanceToClosestFood + \
            -2 * (1. / distanceToClosestActiveGhost) + \
            -2 * distanceToClosestScaredGhost + \
            -20 * numberOfCapsulesLeft + \
            -4 * numberOfFoodsLeft

    #return score

    util.raiseNotDefined()

