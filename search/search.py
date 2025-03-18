# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
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
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(problem):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(problem, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(problem, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(problem, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited =  set() # Boolean set initializing
    direction = {}#init dummy direction dictionary
    parents = {}#init dummy parent dictionary
    stack.push(problem.getStartState()) # push start state
    goal = None
   # visited.add(problem.getStartState())
    try:
            while(not stack.isEmpty()):
                pop = stack.pop() #get current state 
              #  msg = str(pop) + " and its successor: " + str(problem.getSuccessors(pop)) #get current position and successor
               # print(msg)
                if(problem.isGoalState(pop)): #if reached the goal
                    goal = pop
                    #print("goal state reached")
                    break
                    #note: the more you call getSuccessor, the larger the node expansion will be, so avoid calling it multiple times
                for successor, dir,step_cost in problem.getSuccessors(pop):
                    if successor not in visited:
                       # print(str(pop) + " and successors:" + str(problem.getSuccessors(pop)[i])) #get position
                        stack.push(successor) #push the latest position to stack
                        visited.add(successor)
                        parents[successor] = pop
                        direction[successor] = dir
                visited.add(pop)
    finally:
        path = []
        current = goal
        while current != problem.getStartState():
            path.append(direction[current])
            current = parents[current]
        
        path.reverse()
       # print(path)
        return path
    util.raiseNotDefined() 
     
        


    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue()
    visited =  set() # Boolean list initializing
    direction = {}#init dummy direction dictionary
    parents = {}
    queue.push(problem.getStartState()) # push start state
    goal = None
   # visited.add(problem.getStartState())
    try:
            while(not queue.isEmpty()):
                pop = queue.pop() #get current state 
              #  msg = str(pop) + " and its successor: " + str(problem.getSuccessors(pop)) #get current position and successor
               # print(msg)
                if(problem.isGoalState(pop)): #if reached the goal
                    goal = pop
                   # print("goal state reached")
                    break
                    #note: the more you call getSuccessor, the larger the node expansion will be, so avoid calling it multiple times
                for successor, dir,step_cost in problem.getSuccessors(pop):
                    if successor not in visited:
                     
                        queue.push(successor) #push the latest position to stack
                        visited.add(successor) #mark the latest as visited
                        parents[successor] = pop # mark the parent
                        direction[successor] = dir#get the direction (by key-pairing the now visited node with its direction)
                visited.add(pop)
    finally: #reconstruct the path
        path = []
        current = goal
        while current != problem.getStartState():
            path.append(direction[current])
            current = parents[current]
        
        path.reverse()
        #print(path)
        return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
 

    queue = util.PriorityQueue()
    visited =  set() # Boolean list initializing
    direction = {}#init dummy direction dictionary
    parents = {}
    queue.push(problem.getStartState(),0) # push start state
    goal = None
   # visited.add(problem.getStartState())
    g_costs = {problem.getStartState(): 0}
    try:
            while(not queue.isEmpty()):
                pop = queue.pop() #get current state 
                # msg = str(pop) + " and its successor: " + str(problem.getSuccessors(pop)) #get current position and successor
                # print(msg)
                if(problem.isGoalState(pop)): #if reached the goal
                    goal = pop
                  #  print("goal state reached")
                    break
                visited.add(pop) #mark the latest as visited
                #note: the more you call getSuccessor, the larger the node expansion will be, so avoid calling it multiple times
                for successor, dir,step_cost in problem.getSuccessors(pop):
                         if not successor in visited:
                            temp_g_cost = g_costs[pop] + step_cost
                            if(successor not in g_costs or temp_g_cost < g_costs[successor]):
                                g_costs[successor] = temp_g_cost

                              
                                queue.push(successor,temp_g_cost) #push the latest position to queue
                                parents[successor] = pop
                                direction[successor] = dir
                visited.add(pop)        
    finally:
        path = []
        current = goal
        while current != problem.getStartState():
            path.append(direction[current])
            current = parents[current]
        
        path.reverse()
       # print(path)
        return path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    visited = set() # Boolean list initializing
    direction = {}#init dummy direction dictionary
    parents = {}
    queue.push(problem.getStartState(),0) # push start state
    goal = None
    g_costs = {problem.getStartState(): 0}
    try:
            while(not queue.isEmpty()):
                pop = queue.pop() #get current state 
              #  msg = str(pop) + " and its successor: " + str(problem.getSuccessors(pop)) #get current position and successor
               # print(msg)
                if(problem.isGoalState(pop)): #if reached the goal
                    goal = pop
                    print("goal state reached")
                    break
                visited.add(pop)
               #note: the more you call getSuccessor, the larger the node expansion will be, so avoid calling it multiple times
                for successor, dir,step_cost in problem.getSuccessors(pop):
                           if  successor not in visited:
                            temp_g_cost = g_costs[pop] + step_cost
                            if(successor not in g_costs or temp_g_cost < g_costs[successor]):
                                g_costs[successor] = temp_g_cost
                                f_costs = temp_g_cost + heuristic(successor,problem)
                             
                                queue.push(successor,f_costs) #push the latest position to queue
                                parents[successor] = pop
                                direction[successor] = dir
                visited.add(pop)

    finally:
        path = []
        current = goal
        while current != problem.getStartState():
            path.append(direction[current])
            current = parents[current]
        
        path.reverse()
       # print(path)
        return path
    util.raiseNotDefined()


#####################################################
# EXTENSIONS TO BASE PROJECT
#####################################################

# Extension Q1e
def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


#####################################################
# Abbreviations
#####################################################
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
