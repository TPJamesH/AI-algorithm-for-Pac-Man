# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        # ^ > < v = pacman's mouth direction  | G = ghost | % = wall | . = food
        "*** YOUR CODE HERE ***"
        # print("Successor game state: " + str(successorGameState))
        # print("New position: "+  str(newPos))
        # print("New food: "+ str(newFood))
        # print("Ghost: "+ str(newGhostStates[0].getPosition())) #tuple 
        # print("New Scared times: " + str(newScaredTimes))
        # print("Score: "+ str(successorGameState.getScore()))

        foodSet = set() #initialized as empty sets to store food coordinates
        distanceFood = set() #initialized as empty sets  to store distance from pac-man to different food coordinates
        ghost_x =  newGhostStates[0].getPosition()[0] #get the current X-coordinate of ghost
        ghost_y =  newGhostStates[0].getPosition()[1] # get the current Y-coordinate of ghost
        distanceGhost = 0 #disance from pacman to ghost
        for i in range(newFood.width): # get all food coordinates in the grid
            for k in range(newFood.height):
                if newFood[i][k]:
                    foodSet.add((i,k))
        # print(foodSet)
      #---POSITION ANALYSIS---#
        for food in foodSet: #iterate over the set, and calculate the distance from pac-man to different food coordinates (manhattan heuristic)
                distanceFood.add(abs(newPos[0] - food[0]) + abs(newPos[1] - food[1]))

        #calculate the next move of the ghost        
        if newGhostStates[0].getDirection() == 'East':
            ghost_x +=1 
        
        if newGhostStates[0].getDirection() == 'West':
            ghost_x -= 1

        if newGhostStates[0].getDirection() == 'North':
            ghost_y += 1

        if newGhostStates[0].getDirection() == 'South':
            ghost_y -= 1

        #get the distance between the ghost and pacman (manhattan)
        distanceGhost = abs(newPos[0] - ghost_x) + abs(newPos[1] - ghost_y)
       # distanceGhost = abs(newPos[0] - newGhostStates.) + abs(newPos[1] - newGhostStates[1])

        #-----EVALUATION-----#
        foodWeight = 10 #mark the importance of food (primary goal) => higher weight= more aggresive food collecting
        ghostWeight = 2# mark the importance of ghost (secondary goal ) => lower weight = doesn't mind the ghost much, but not completely ignore
        if distanceFood: #if any food coordinate presented
                minDistanceFood = min(distanceFood) #get the closest coordinate relative to pacman's current position
                
                output = (successorGameState.getScore() + foodWeight/minDistanceFood -  ghostWeight/max(distanceGhost,0.1))  #score adjust based on minimum distance to food and distance to ghost
        else:
                output = successorGameState.getScore() - ghostWeight/max(distanceGhost,0.1) #adjust based on distance to ghost
            
       # output = min(distance,distanceGhost,successorGameState.getScore()) * -1 
       # print("food distance: "+ str(distance))
       # print("ghost distance: "+ str(distanceGhost))
      #  print("output:" + str(output))
        return output

def scoreEvaluationFunction(currentGameState: GameState): 
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState:GameState,depth): #pacman is MAX player
            if gameState.isWin() or gameState.isLose() or depth == self.depth: #essentially "game.IS-TERMINAL(STATE) then return game.UTILITY(state,player)" in the textbook
                return self.evaluationFunction(gameState)
            v = float('-inf') # equivalent of "v,move <- negative infinity"
            for action in gameState.getLegalActions(0): #for some reason, getLegalPacmanActions doesn't work, so getLegalPacmanActions will sufficed
                pacmanSuccessor = gameState.generateSuccessor(0,action) # same for successor generation
                v = max(v,minValue(pacmanSuccessor,1,depth))  #get the maximum value from all the possible responses from the ghosts   
            return v
        ##########################################
        def minValue(gameState:GameState,ghostIndex,depth): #ghosts are MIN player
             if gameState.isWin() or gameState.isLose() or depth == self.depth:  #essentially "game.IS-TERMINAL(STATE) then return game.UTILITY(state,player)" in the textbook
                return self.evaluationFunction(gameState)
             v = float('inf') # equivalent of "v,move <- positive infinity"
             for action in gameState.getLegalActions(ghostIndex): #get possible moves of the ghost based on current game state of the pac-man
                ghostSuccessor = gameState.generateSuccessor(ghostIndex,action)
                if ghostIndex == gameState.getNumAgents() - 1: # final ghost
                    v = min(v,maxValue(ghostSuccessor,depth + 1)) # pac-man's turn
                else: #according to Berkeley AI project -> minimax tree will have multiple min layers (one for each ghost) for every max layer
                    v = min(v, minValue(ghostSuccessor,ghostIndex + 1,depth)) #next ghost's turn
                    

             return v
        ###############################
        #Pacman is always agent 0, and the agents move in order of increasing agent index (pacman then ghosts)
        pacmanActions = gameState.getLegalActions(0) #parameter = agent index 
        best_value = float('-inf') #intialize variable to hold best value
        best_action = None #intialize variable to hold best actions

        for action in pacmanActions: # note: this loop is actually an un-encapsulated, simplified version of the function for MAX player. It serves as the starter of the recursive loop
            pacmanSuccessor = gameState.generateSuccessor(0,action)
            value = minValue(pacmanSuccessor,1,0) #Pass the  game state of pacman in, along with the first ghost (to get the game state of that ghost later), and initial depth
            if(value > best_value): # in terms of the pseudocode in the textbook, this is "value, move <- MAX-VALUE (game,state)"
                best_value = value
                best_action = action

        return best_action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """Note: both maxValue and minValue functions integrated the pseudocode obtained from question 3 of Berkeley AI assignment"""
        def maxValue(gameState:GameState,alpha,beta,depth): #pacman is MAX player
            if gameState.isWin() or gameState.isLose() or depth == self.depth: #essentially "game.IS-TERMINAL(STATE) then return game.UTILITY(state,player)" in the textbook
                return self.evaluationFunction(gameState)

            v = float('-inf') # equivalent of "v,move <- negative infinity"
            for action in gameState.getLegalActions(0): #for some reason, getLegalPacmanActions doesn't work, so getLegalPacmanActions will sufficed
                pacmanSuccessor = gameState.generateSuccessor(0,action) # same for successor generation
                v = max(v,minValue(pacmanSuccessor,alpha,beta,1,depth))  #get the maximum value from all the possible responses from the ghosts   
                
                if v > beta: return v
                alpha = max(alpha,v)

            return v
        ##########################################
        def minValue(gameState:GameState,alpha,beta,ghostIndex,depth): #ghosts are MIN player
             if gameState.isWin() or gameState.isLose() or depth == self.depth:  #essentially "game.IS-TERMINAL(STATE) then return game.UTILITY(state,player)" in the textbook
                return self.evaluationFunction(gameState)
            
            
             v = float('inf') # equivalent of "v,move <- positive infinity"
             for action in gameState.getLegalActions(ghostIndex): #get possible moves of the ghost based on current game state of the pac-man
                ghostSuccessor = gameState.generateSuccessor(ghostIndex,action)
                    
                if ghostIndex == gameState.getNumAgents() - 1: # final ghost
                    v = min(v, maxValue(ghostSuccessor,alpha,beta,depth + 1)) # pac-man's turn   
                else: #according to Berkeley AI project -> minimax tree will have multiple min layers (one for each ghost) for every max layer
                    
                    v = min(v, minValue(ghostSuccessor,alpha,beta,ghostIndex + 1,depth) ) #next ghost's turn
                    
                if v < alpha: return v
                beta = min(beta,v) 
        
             return v
        ###############################
        #Pacman is always agent 0, and the agents move in order of increasing agent index (pacman then ghosts)
        pacmanActions = gameState.getLegalActions(0) #parameter = agent index 
        best_value = float('-inf') #intialize variable to hold best value
        best_action = None #intialize variable to hold best actions
        alpha =float('-inf')
        beta =float('inf')
    

        for action in pacmanActions: # note: this loop is actually an un-encapsulated, simplified version of the function for MAX player. It serves as the starter of the recursive loop
            pacmanSuccessor = gameState.generateSuccessor(0,action)
            value = minValue(pacmanSuccessor,alpha,beta,1,0) #Pass the  game state of pacman in, along with the first ghost (to get the game state of that ghost later), and initial depth
           
            if(value > best_value): # in terms of the pseudocode in the textbook, this is "value, move <- MAX-VALUE (game,state)"
                best_value = value
                best_action = action
            alpha= max(alpha,best_value) #save the latest alpha value 

        return best_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState:GameState,depth): #pacman is MAX player
            if gameState.isWin() or gameState.isLose() or depth == self.depth: #essentially "game.IS-TERMINAL(STATE) then return game.UTILITY(state,player)" in the textbook
                return self.evaluationFunction(gameState)
            v = float('-inf') # equivalent of "v,move <- negative infinity"
            for action in gameState.getLegalActions(0): #for some reason, getLegalPacmanActions doesn't work, so getLegalPacmanActions will sufficed
                pacmanSuccessor = gameState.generateSuccessor(0,action) # same for successor generation
                v = max(v,chanceValue(pacmanSuccessor,1,depth))  #get the maximum value from all the possible responses from the ghosts   
            return v
        ##########################################
         #ghosts are chance/expecti player
        def chanceValue(gameState:GameState,ghostIndex,depth):
             if gameState.isWin() or gameState.isLose() or depth == self.depth:  #essentially "game.IS-TERMINAL(STATE) then return game.UTILITY(state,player)" in the textbook
                return self.evaluationFunction(gameState)
             v = 0 # equivalent of "v,move <- positive infinity"
             for action in gameState.getLegalActions(ghostIndex): #get possible moves of the ghost based on current game state of the pac-man
                ghostSuccessor = gameState.generateSuccessor(ghostIndex,action)
                if ghostIndex == gameState.getNumAgents() - 1: # final ghost
                    v = (maxValue(ghostSuccessor,depth + 1) + v)  # pac-man's turn
                else: #according to Berkeley AI project -> minimax tree will have multiple min layers (one for each ghost) for every max layer
                    #v = min(v, chanceValue(ghostSuccessor,ghostIndex + 1,depth)) #next ghost's turn
                    v = (chanceValue(ghostSuccessor,ghostIndex + 1,depth) + v) / ghostIndex + 1
                    

             return v
        ###############################
        #Pacman is always agent 0, and the agents move in order of increasing agent index (pacman then ghosts)
        pacmanActions = gameState.getLegalActions(0) #parameter = agent index 
        best_value = float('-inf') #intialize variable to hold best value
        best_action = None #intialize variable to hold best actions

        for action in pacmanActions: # note: this loop is actually an un-encapsulated, simplified version of the function for MAX player. It serves as the starter of the recursive loop
            pacmanSuccessor = gameState.generateSuccessor(0,action)
            value = chanceValue(pacmanSuccessor,1,0) #Pass the  game state of pacman in, along with the first ghost (to get the game state of that ghost later), and initial depth
            if(value > best_value): # in terms of the pseudocode in the textbook, this is "value, move <- MAX-VALUE (game,state)"
                best_value = value
                best_action = action

        return best_action
        util.raiseNotDefined()
def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: 
    The evaluation function use AlphaBeta agent to 
    determine the optimal successor game state for evaluation, 
    if the current game state is terminal, then it will be 
    evaluated instead.

    The features (e.g., ghost's position, scared ghost's position,
    pacman's position, food's position, and pellet's position ) 
    of the chosen game state (successor/current) will be extracted 
    to calculate the distance between pacman's position to foods,pellets, 
    and ghost coordinates,respectively.

    The evaluation process will utilize variables called 
    food weight, ghost weight, pellet weight, 
    and scared ghost weight. They are responsible for pacman's
    prioritization on the consumables and obstacles.
    Addtionally, they can be dynamically adjusted based on
    the calculated distance of the function's current iteration

    The evaluation first check the ghost promoxity 
    (how close the ghost is to Pacman) and
    whether there's any pellets on the map.
    If the condition is true, then the current score will be added 
    with pelletWeight / farthest pellet from pacman's position

    If the above condition failed, then the evaluation check if there's any
    food on the map, then the food proximity
    (how close the ghost is to Pacman) to get the closest food and pellet proximity
    to get the farthest pellet (if there's any).
    If the condition is true, then the current score will be added 
    with pelletWeight / farthest pellet from pacman's position, foodWeight / closest food fom pacman's position,
    and subtracted by ghostWeight / distance from pacman to ghost and added again by scared ghost's weight

    If all conditions mentioned above failed (e.g., pacman's
    line of sight to foods is blocked by walls), then the pacman shift its attention
    to the ghost and try to avoid it at all cost, which would leads to chase scenarios,
    at some point it would guide the pacman to the remaining foods, and the above conditions 
    will become true in the next function iteration.

    Note on pellets: maximum distance to pellets was used instead of minimum to ensure the
    safety of pacman and reposition itself to a better situation (e.g., set it self up to be near the farthest pellet,
    and wait for the ghost to come, the pacman then consume the pellet and then the ghost for optimal score)

    Note on scared ghost: since scared ghost greatly boost pacman's score when consumed, 
    this evaluation function encourage pacman to consume the ghost through
    'scaredGhostWeight'.
    """
    "*** YOUR CODE HERE ***"

    #--------EXTRACTING FEATURES-------------###
    output = 0
    agent = AlphaBetaAgent() # it is inefficient to check the entire map (consume computational power), so AlphaBeta is used to enhance the calculation speed and choose the most optimal successor (in terms of depth, and best-worse case handler)
    #generate the successor for the current game state if possible. 
    try:
        successorGameState = currentGameState.generatePacmanSuccessor(agent.getAction(currentGameState))
    except: #If the terminal state is reached, then the current game state will be used
         successorGameState = currentGameState
         
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
     # ^ > < v = pacman's mouth direction  | G = ghost | % = wall | . = food
        

    foodSet = set() #initialized as empty sets to store food coordinates
    distanceFood = set() #initialized as empty sets  to store distance from pac-man to different food coordinates
    distancePellet = set()
    pelletList = successorGameState.getCapsules()
    ghost_x =  newGhostStates[0].getPosition()[0] #get the current X-coordinate of ghost
    ghost_y =  newGhostStates[0].getPosition()[1] # get the current Y-coordinate of ghost
   

    distanceGhost = 0 #distance from pacman to ghost

   #---POSITION ANALYSIS---#
    for i in range(newFood.width): # get all food coordinates in the grid
            for k in range(newFood.height):
                if newFood[i][k]:
                    foodSet.add((i,k))
    

    for pellet in pelletList:
         distancePellet.add(abs(newPos[0] - pellet[0]) + abs(newPos[1] - pellet[1]))

    for food in foodSet: #iterate over the set, and calculate the distance from pac-man to different food coordinates (manhattan heuristic)
                distanceFood.add(abs(newPos[0] - food[0]) + abs(newPos[1] - food[1]))

        #calculate the next move of the ghost        
    if newGhostStates[0].getDirection() == 'East':
            ghost_x +=1 
        
    if newGhostStates[0].getDirection() == 'West':
            ghost_x -= 1

    if newGhostStates[0].getDirection() == 'North':
            ghost_y += 1

    if newGhostStates[0].getDirection() == 'South':
            ghost_y -= 1

        #get the distance between the ghost and pacman (manhattan)
    distanceGhost = abs(newPos[0] - ghost_x) + abs(newPos[1] - ghost_y)
       # distanceGhost = abs(newPos[0] - newGhostStates.) + abs(newPos[1] - newGhostStates[1])
    scareGhostDistance = distanceGhost if newScaredTimes[0] > 0 else 0
    
   #-----EVALUATION-----#
    scaredGhostWeight = 0
    ghostWeight = 0
    foodWeight = 5 if distanceGhost < 5 else 8 #mark the importance of food (primary goal) => larger weight= more aggresive food collecting

    if(newScaredTimes[0] >0):
        ghostWeight = 5 # mark the importance of ghost (secondary goal ) => lower weight = doesn't mind the ghost much, but not completely ignore
        scaredGhostWeight = 300 / max(scareGhostDistance,1)
        #reminder, larger weight => more aggresive in consuming, and scared ghost is also a type of food
    else:
        ghostWeight = 15 if distanceGhost < 5 else 3

    pelletWeight = 20 if distanceGhost < 5 else 10
    
    if len(pelletList) < 2: #if any pellets are still on the map
        pelletWeight += 10

    if distanceGhost < 5 and distancePellet: #if ghost is close and there are pellet
         output =  successorGameState.getScore() + pelletWeight/ max(distancePellet,default=float('inf'))
  
    elif distanceFood: #if any food coordinate presented
        minDistanceFood = min(distanceFood, default = float('inf')) #get the closest coordinate relative to pacman's current position
        maxDistancePellet = max(distancePellet,default=float('inf'))
                
        output = successorGameState.getScore() + (foodWeight/minDistanceFood +  pelletWeight/maxDistancePellet)  -  ghostWeight/max(distanceGhost,0.1) + scaredGhostWeight #score adjust based on minimum distance to food and distance to ghost
    else: #default case
         output = successorGameState.getScore() - ghostWeight/max(distanceGhost,0.1) + scaredGhostWeight #adjust based on distance to ghost
            
    
    return output
   
   
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

