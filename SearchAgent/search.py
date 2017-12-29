# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    fringe = Stack()

    # result is a list of actions to reach the goal state
    prev_action = []
    prev_cost = []
    successors = set()     # the empty set

    # getSuccessor returns (successor, action, cost) tuple
    # fringe = (state, action, cost) tuple
    #           (x,y) position tuple

    fringe.push((problem.getStartState(), prev_action, prev_cost))
    while True:
        if fringe.isEmpty():
            return null
        (popped_state, popped_action, popped_cost) = fringe.pop()
        if problem.isGoalState(popped_state):
            # return list of actions, i.e. second value in tuple
            return popped_action

        # part of EXPAND
        if popped_state not in successors:
            successors.add(popped_state)
            for successor, action, cost in problem.getSuccessors(popped_state):
                popped_action_list = list(popped_action)
                popped_action_list.append(action)
                # list(popped_action).append(action)
                fringe.push((successor, popped_action_list, popped_cost))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    from util import Queue

    fringe = Queue()

    # result is a list of actions to reach the goal state
    prev_action = []
    prev_cost = []
    successors = set()     # the empty set

    # getSuccessor returns (successor, action, cost) tuple
    # fringe = (state, action, cost) tuple
    #           (x,y) position tuple

    fringe.push((problem.getStartState(), prev_action, prev_cost))
    while True:
        if fringe.isEmpty():
            return null
        (popped_state, popped_action, popped_cost) = fringe.pop()
        if problem.isGoalState(popped_state):
            # return list of actions, i.e. second value in tuple
            return popped_action

        # part of EXPAND
        if popped_state not in successors:
            successors.add(popped_state)
            for successor, action, cost in problem.getSuccessors(popped_state):
                popped_action_list = list(popped_action)
                popped_action_list.append(action)
                # list(popped_action).append(action)
                fringe.push((successor, popped_action_list, popped_cost))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue

    fringe = PriorityQueue()

    # result is a list of actions to reach the goal state
    actions_to_goal = []
    prev_cost = []
    successors = set()     # the empty set

    # getSuccessor returns (successor, action, cost) tuple
    # fringe = (state, action, cost) tuple - cost not stored, just used to sort
    # state - (x,y) position tuple

    fringe.push((problem.getStartState(), actions_to_goal), problem.getCostOfActions(actions_to_goal))

    while True:
        if fringe.isEmpty():
            return None

        # cost not stored in PriorityQueue, so only state and action would be popped off the fringe
        (popped_state, popped_action) = fringe.pop()

        if problem.isGoalState(popped_state):
            # return list of actions, i.e. second value in tuple
            return popped_action

        # part of EXPAND
        if popped_state not in successors:
            successors.add(popped_state)
            for successor, action, cost in problem.getSuccessors(popped_state):
                popped_action_list = list(popped_action)
                popped_action_list.append(action)
                fringe.push((successor, popped_action_list), problem.getCostOfActions(popped_action_list))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue
    from util import manhattanDistance

    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    # print problem

    fringe = PriorityQueue()
    visited = dict()  # see class Counter in util.py

    # get the current state
    cur_state = problem.getStartState()

    # copy the contents of the current (root?) node in problem
    item = {}

    # initial settings
    item["parent"] = None
    item["action"] = None
    item["state"] = cur_state
    item["cost"] = 0
    item["heuristic"] = heuristic(cur_state, problem)

    # Expand: have to create such that f = g + h
    fringe.push(item
                , item["cost"] + item["heuristic"])

    # Just like DFS but with priority queue and
    while not fringe.isEmpty():
        item = fringe.pop()
        state = item["state"]
        cost = item["cost"]
        v = item["heuristic"]
        # print state

        if visited.has_key(state):
            continue

        visited[state] = True
        if problem.isGoalState(state) == True:
            break

        for child in problem.getSuccessors(state):
            if not visited.has_key(child[0]):
                next_item = {}
                next_item["parent"] = item
                next_item["state"] = child[0]
                next_item["action"] = child[1]
                next_item["cost"] = child[2] + cost
                next_item["heuristic"] = heuristic(next_item["state"], problem)
                fringe.push(next_item, next_item["cost"] + item["heuristic"])

    actions = []
    while item["action"] != None:
        actions.insert(0, item["action"])
        item = item["parent"]

    return actions

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
