from game import Agent
from game import Directions
from game import Actions
import distanceCalculator
from util import nearestPoint
from baselineTeam import ReflexCaptureAgent
from captureAgents import CaptureAgent
import random
import util

def createTeam(firstIndex, secondIndex, isRed,
               first = 'ContestOffensiveReflexAgent', second = 'ContestDefensiveReflexAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """
    return [eval(first)(firstIndex), eval(second)(secondIndex)]



class ContestOffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def getFeatures(self, gameState, action):
        features = util.Counter()
        previousFood = self.getFood(gameState).asList()
        previousCapsules = self.getCapsules(gameState)

        successor = self.getSuccessor(gameState, action)
        # features['successorScore'] = self.getScore(successor)
        myPos = successor.getAgentState(self.index).getPosition()
        ghosts =[successor.getAgentState(i) for i in self.getOpponents(successor) if successor.getAgentState(i).getPosition() != None]
        if action == Directions.STOP:
            features["stop"] = 1

        minScaredDistance = float("inf")
        minNormalDistance = float("inf")
        for ghost in ghosts:
            if not ghost.isPacman:
                if ghost.scaredTimer > 0:
                    if self.getMazeDistance(myPos, ghost.getPosition()) <= 2:
                        features["scared1away"] += 1
                        features["eatFood"] += 2
                    # minScaredDistance =  min(self.getMazeDistance(myPos, ghost.getPosition()), minScaredDistance)
                else:
                    if self.getMazeDistance(myPos, ghost.getPosition()) <= 1:
                        minNormalDistance = min(self.getMazeDistance(myPos, ghost.getPosition()), minNormalDistance)
                        features["normal1away"] += 1

        if minNormalDistance == float("inf"):
            features["normalDistance"] = 0
        else:
            features["normalDistance"] = minNormalDistance

        # if minScaredDistance == float("inf"):
        #     features["scaredDistance"] = 0
        # else:
        #     features["scaredDistance"] = minScaredDistance


        foodList = self.getFood(successor).asList()
        capsulesList = self.getCapsules(successor)
        if len(foodList) > 0:
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
        if len(capsulesList) > 0:
            minDistance = min([self.getMazeDistance(myPos, capsule)] for capsule in capsulesList)
            features['distanceToCapsule'] = minDistance[0]
        if len(foodList) < len(previousFood):
            features["eatFood"] += 1
            features["distanceToFood"] = 0

        if len(capsulesList) < len(previousCapsules):
            features["eatCapsules"] += 1
            features["distanceToCapsule"] = 0



        print features
        return features

    def getWeights(self, gameState, action):
        return {'distanceToFood': -1, 'normal1Away': -20, 'scared1Away':1, "distanceToCapsule" : -1, "stop" : -10,
                'eatFood': 1, 'eatCapsule':10, "normalDistance":-4}

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        print action, features*weights
        return features * weights

class ContestDefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        previousInvaders = invaders

        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if len(invaders) < len(previousInvaders):
            features["eatInvader"] += 1
            features["distanceToInvader"] = 0

        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {'numInvaders': -1000, 'onDefense': 50, 'invaderDistance': -10, 'stop': -100, 'reverse': -2, 'eatInvader': 50} #onDefense = 100 initially
