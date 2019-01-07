#############################################################
#                    Authors:                               #
#               Christopher Edgley  75258                   #
#               Inês Lourenço       75637                   #
#############################################################

from copy import deepcopy

goalCask    = []
goalCWeight = []
goalStack   = []
goalStIndex = []
crossings   = []

# Reads the input file and creates the structures of
# crossings and casks, and return the first state space
def processFile(filename):

    state_space = []
    casks=[]
    global crossings
    
    for x in open(filename):
        line = x.split()

        if (line == []):
            continue

        elif (line[0][0] == 'S'):
            state_space.append([line[0], int(line[1]), []])
            if (len(line) > 2):
                for i in range(len(line)-2):
                    state_space[-1][-1].append(line[i+2])

        elif line[0][0] == 'E': # line = ['E','S4','N0,4','0.89']
            flagA = 0 # Indicates when the crossing in the first position has been placed
            flagB = 0 # Indicates when the crossing in the second position has been placed

            if crossings == []:
                crossings.append([line[1], [line[2], float(line[3])]])
                crossings.append([line[2], [line[1], float(line[3])]])
            else: # Since the crossings structure isn't empty, it must be searched for inserting existing crossings
                for c in crossings:
                    if line[1] == c[0]:
                        c.append([line[2], float(line[3])])
                        flagA = 1
                    if line[2] == c[0]:
                        c.append([line[1], float(line[3])])
                        flagB = 1
                if flagA != 1:
                    crossings.append([line[1], [line[2], float(line[3])]])
                if flagB != 1:
                    crossings.append([line[2], [line[1], float(line[3])]])
                    
        elif (line[0][0] == 'C'): # All casks are accumulated in a list for posterior processing
            line = [line[0], int(line[1]), float(line[2])]
            casks.append(line)    
    
    processCasks(state_space, casks)

    # Initial conditions
    cts = ['Empty' , 'EXIT']
    state_space.insert(0, cts)

    return state_space


# Stores the information of each cask in its corresponding stack
def processCasks(state_space, casks):
    while casks != []:
        cas = casks.pop(0)
        for ss in state_space:
            for c_id in range(len(ss[2])):
                if (cas[0] == ss[2][c_id]):
                    ss[2][c_id] = cas # List of cask info ['C5', '1', '0.124236'] replaces its placeholder name


# Attempts to load or unload. If so, returns cost of action, otherwise returns empty list []
def loadUnload (state_space): 
    if state_space[0][1][0] != 'S': # It is impossible to load or unload if the cts is not in a stack
        return []                   # No operation

    newStateSpace = deepcopy(state_space) # A deep copy must be performed to save and later modify all generated state spaces
    for ss in newStateSpace:
        if ss[0] != newStateSpace[0][1]:
            continue
        # Está unloaded, vai fazer o LOAD
        if newStateSpace[0][0] == 'Empty': # If it is empty, the cts can perform a load action
           if ss[2] == []: # A load action cannot be performed on an empty stack
               return []
           cask = ss[2].pop()
           newStateSpace[0][0] = cask # Updates the cts with the newly loaded cask
           action = 'load'
                
        else: # When loaded, the cts can perform an unload action
            cask = newStateSpace[0][0]
            totalLength = 0
            for casksId in ss[2]:
                totalLength = totalLength + casksId[1]

            if newStateSpace[0][0][1] + totalLength > ss[1]: # An unload action cannot be performed if the cask doesn't fit in the stack's remaining space
                return []

            ss[2].append(newStateSpace[0][0])
            newStateSpace[0][0] = 'Empty'
            action = 'unload'

        caskWeightCost = cask[2] + 1
        return [[newStateSpace, [action] + [cask[0]] + [newStateSpace[0][1]] + [caskWeightCost]]]


# Retuns all possible move actions from a given state space
def moveCTS(state_space):
    
    place = state_space[0][1]
    DescendentsSS = []
    
    for cross in crossings: # Find the starting location
         if place != cross[0]:
             continue
         for adj in cross[1:]: # For each adjacent node, create a new state space
            newStateSpace = deepcopy(state_space)                    
            newStateSpace[0][1] = adj[0]
            
            if newStateSpace[0][0] != 'Empty' :
                cost = (1 + newStateSpace[0][0][2]) * adj[1]
            else:
                cost = adj[1]
            
            opText = ['move'] + [place] + [newStateSpace[0][1]] + [cost]
            DescendentsSS.append([newStateSpace, opText])  
                        
    return DescendentsSS
    
# Calls the functions which generates lists of state spaces for possible actions
def exploreSS(state_space):
    return loadUnload(state_space) + moveCTS(state_space)

# Checks if the goal state was reached, i.e. reaching the EXIT with the goal cask loaded
def checkGoalState(state_space):
    if state_space[0][0][0] == goalCask and state_space[0][1] == 'EXIT':
        return 1
    return 0

# Sets the global variables related to the parameters of the goal cask
def setGoal(cask, fss):
    global goalCask
    global goalCWeight
    global goalStack
    global goalStIndex

    goalCask = cask
    for st in fss[1:]: #st represent cada stack no statespace
        for c in st[2]:
            if c[0] == goalCask:
                goalStack = st[0]
                goalStIndex = fss.index(st)
                goalCWeight = c[2]
                return
    else:
        return -1

# Calculation of heuristic for cask loading/unloading component of the problem
def heurLoad(stSpace):
    cumSum = 0
    if stSpace[0][0] != 'Empty':
        if stSpace[0][0][0] != goalCask:
            cumSum = stSpace[0][0][2]

    for c in stSpace[goalStIndex][2][::-1]:
        cumSum += 2 * c[2]
        if c[0] == goalCask:
            cumSum -= c[2]
            break
    else:
        cumSum = 0
    return cumSum
    
# Calculation of heuristic for movement component of the problem
def heurMove(stSpace):
    if stSpace[0][0][0] == goalCask:
        pathCost = (1 + goalCWeight)*dijkstra(stSpace[0][1], 'EXIT')
    else:
        pathCost = dijkstra(stSpace[0][1], goalStack) + (1 + goalCWeight)*dijkstra(goalStack, 'EXIT')
    return pathCost

# Dijkstra graph search algorithm
def dijkstra(initial, goal):
    
    dist  = []
    prev  = []
    nodes = []
    for i, cross in list(enumerate(crossings)):
        nodes.append(tuple([cross[0], i]))
    Q = dict(nodes) # Dictionary which allows reverse search of indexes from names of places (crossings, stacks or exit)
    
    initial = Q[initial]
    goal = Q[goal]

    for i in Q:
        dist.append(float('inf'))
        prev.append(-1)

    dist[initial] = 0

    visited = []
    unvisited = list(range(len(Q)))
    
    while unvisited != []:
        
        selnode = unvisited[0]
        for i in unvisited:
            if dist[i] < dist[selnode]:
                selnode = i

        for adj in crossings[selnode][1:]:
            adjIndex = Q[adj[0]]
            if  dist[adjIndex] > dist[selnode] + adj[1]:
                dist[adjIndex] = dist[selnode] + adj[1]
                prev[selnode]  = adjIndex
                
        if selnode == goal:
            return dist[goal]

        visited.append(selnode)
        unvisited.pop(unvisited.index(selnode))