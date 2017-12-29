# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
import random, util, math


class QLearningAgent(ReinforcementAgent):
    """
    Q-Learning Agent

    Functions you should fill in:
      - computeValueFromQValues
      - computeActionFromQValues
      - getQValue
      - getAction
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions for a state
  """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.q_vals = util.Counter()

    def getQValue(self, state, action):
        """
      Returns Q(state,action)
      Should return 0.0 if we have never seen a state
      or the Q node value otherwise
    """
        "*** YOUR CODE HERE ***"
        return self.q_vals[(state, action)]

    def computeValueFromQValues(self, state):
        """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0
    """
        "*** YOUR CODE HERE ***"
        Q = []
        Legal = self.getLegalActions(state)
        for action in Legal:
            Q.append(self.getQValue(state, action))
        if len(Legal) == 0:
            return 0.0
        else:
            return max(Q)
    """
    I found this section of code online and reference it here from googledocs. 
    Our original getAction and getQValue got results much different from this.
    We were never able to win a match until we pushed for a maximum Q value based
    on the slides in class from 2 weeks ago.  That one used an example (see dropbox 
    on lecture date 10/13/17).
    """
    def computeActionFromQValues(self, state):
        """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
        "*** YOUR CODE HERE ***"
        bestAction = None
        maxQ = 0
        Legal = self.getLegalActions(state)

        for action in Legal:
            Q = self.getQValue(state, action)
            if Q > maxQ or bestAction is None:
                maxQ = Q
                bestAction = action
        return bestAction

    def getAction(self, state):
        """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        """
        See comments above regarding adding the new code for 
        getQValue and getAction and update
        update didn't really change (meaning we could have used the 
        previous one, but we needed to be consistent.
        """
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state)

        return action

    def update(self, state, action, nextState, reward):
        """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
        "*** YOUR CODE HERE ***"
        """
        This is straight from Roman's lecture (10/15/17) and the question asked by 
        the guy up front halfway during lecture.
        """
        nextLegal = self.getLegalActions(nextState)

        if len(nextLegal) == 0:
            sample = reward
        else:
            sample = reward + (self.discount * max([self.getQValue(nextState, nextAction) for nextAction in nextLegal]))
        self.q_vals[(state, action)] = ((1 - self.alpha) * self.getQValue(state, action) + self.alpha * sample)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
        "*** YOUR CODE HERE ***"
        Q = 0.0
        featureVector = self.featExtractor.getFeatures(state, action)

        for feature in featureVector:
            Q += featureVector[feature] * self.weights[feature]
        return Q

    def update(self, state, action, nextState, reward):
        """
       Should update your weights based on transition
    """
        "*** YOUR CODE HERE ***"

        feat = self.featExtractor.getFeatures(state, action)
        nextLegal = self.getLegalActions(nextState)

        for feature in feat:
            diff = 0
            if len(nextLegal) == 0:
                diff = reward - self.getQValue(state, action)
            else:
                diff = (reward + self.discount * max(
                    [self.getQValue(nextState, nextAction) for nextAction in nextLegal])) - self.getQValue(state,
                                                                                                           action)
            self.weights[feature] = self.weights[feature] + self.alpha * diff * feat[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            """
            TA said not to worry about this because this is only if we
            have questions about the weights.  He said if we did the 
            weight function correct, this would never come up.
            """
            pass