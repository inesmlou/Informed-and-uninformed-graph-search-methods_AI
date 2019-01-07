#############################################################
#                    Authors:                               #
#               Christopher Edgley  75258                   #
#               Inês Lourenço       75637                   #
#############################################################

import domain

class Node:
    def __init__(self, parent = None, stSpace = None,
                       opText = None, totCost = None, heuCost = None):
        self.parent  = parent  # Index of parent, referenced to nodeInsts
        self.stSpace = stSpace # Contains the entirety of this node's state space
        self.opText  = opText  # Contains operation text ['move', 'N3,9', 'EXIT', '1.124236']
        self.totCost = totCost # Represents total cost function, g(n)
        self.heuCost = heuCost # Represents heuristic function, h(n)
        
    def expandNode(self, nId):
        newNodes = []
        stChanges = domain.exploreSS(self.stSpace) # stChanges is a list of all possible state changes which the children will represent [s0, s1, ...]
        for s in stChanges:  # s = [stateSpace, opText] where opText = ['move', 'N0,0', 'N0,1', '8.72']
            stateSpace    = s[0]
            operationText = s[1] # opText = ['load', 'Cb', 'S1', '2.5'] for example
            totalCost     = s[1][3] + self.totCost
            heurCost      = 0 # Heuristic will only be calculated after comparison with existing nodes
            node = Node(nId, stateSpace, operationText, totalCost, heurCost)
            newNodes.append(node)
        return newNodes
    
    def checkGoal(self, nInsts, clList, filename):
        if (domain.checkGoalState(self.stSpace)):
            path = solveSeq(nInsts, clList, self.parent)
            path.append(self.opText)
            path.append([self.totCost])
            for i in path:
                print(' '.join(map(str, i)))
            return 1
        return 0
            
    def updateHeuristic(self, nodeInsts, existNode):
        if existNode == 0: # For a new node, the heuristic must be calculated
            heuCost = domain.heurLoad(self.stSpace) + domain.heurMove(self.stSpace)
        else:
            heuCost = existNode.heuCost # In this case, the heuristic is the same, since the state space is the same
        self.heuCost = heuCost

# Recursive function which produces a list of the sequence of actions to output
def solveSeq(nodeInsts, closedList, goalPathNId):
    parent = None
    parent = nodeInsts[goalPathNId].parent
    if parent == None:
        return []
    
    path = solveSeq(nodeInsts, closedList, parent)
    path.extend([nodeInsts[goalPathNId].opText])
    return path

# Initial function calls the function which reads the input file,
# and generates the crossings as well as the first node with the initial state space
def initStSpace(arg):
    if len(arg) != 3:
        return None

    firstStateSpace = domain.processFile(arg[1])

    if domain.setGoal(arg[2], firstStateSpace) == -1:
        return None

    return Node(stSpace = firstStateSpace, totCost = 0)


# Runs through all previously expanded nodes to find if child was already seen
def compareNodes(child, openList, closedList, nodeInsts):
    for ind in openList:
        if child.stSpace == nodeInsts[ind].stSpace: # Child found repeated in open list
            return nodeInsts[ind]
    for ind in closedList:
        if child.stSpace == nodeInsts[ind].stSpace: # Child found repeated in closed list
            return 1 #Encontrou um node na closedList
    return 0 # No repetition found, child's state space is new
    
# Compares the evaluation function, f=g+h, with h=0 for uninformed search
def lessThanCost(node1, node2):
    if node1.totCost + node1.heuCost < node2.totCost + node2.heuCost:
        return 1
    else:
        return 0