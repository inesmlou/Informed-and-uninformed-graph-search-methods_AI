#############################################################
#      ooooo       .o.        .oooooo..o oooooooooo.        #
#      '888'      .888.      d8P'    'Y8 '888'   'Y8b       #
#       888      .8"888.     Y88bo.       888      888      #
#       888     .8' '888.     '"Y8888o.   888      888      #
#       888    .88ooo8888.        '"Y88b  888      888      #
#       888   .8'     '888.  oo     .d8P  888     d88'      #
#      o888o o88o     o8888o 8""88888P'  o888bood8P'        #
#                                                           #
#                                                           #
#              Project 1 - ITER Logistics                   #
#                                                           #
#                    Authors:                               #
#               Christopher Edgley  75258                   #
#               Inês Lourenço       75637                   #
#                                                           #
#############################################################

import sys
import utilities

#Returns best node from priority queue
def UnifCostSel(openList):
    return openList.pop(0)

#Places node in openList as a priority queue
def UnifCostPlace(nextID, newNodesSize, openList):
    for k in range(newNodesSize):
        newID = nextID + k     #New ID must be unique, as to uniquely index a node in nodeInsts (node instances)
        for aux in openList:
            if utilities.lessThanCost(nodeInsts[newID], nodeInsts[aux]): #Compares evaluation function (f=g=cost function)
                openList.insert(openList.index(aux), newID)          #Finds correct index to insert node as to maintain priority order
                break
        else:
            openList.append(newID) #If a higher priority node isn't found, the new node is appended to the end of the queue (openList)

#Processes a possible node to determine if it should be kept or discarded
def UnifCostDecide(newNodes, child, existNode, nodeInsts, openList):
    if existNode == 0:   #0 means 'New Node', which is always kept
            newNodes.append(child)
    elif existNode == 1: #1 means 'Node already in closedList', therefore isn't appended (therefore discarded)
        return
    else:                #existNode returns the repeated node from the openList
        #If child's evaluation function is lower, it is kept and the old repetition removed from the openList
        if utilities.lessThanCost(child, existNode):
            newNodes.append(child)
            repNodeID  = nodeInsts.index(existNode)
            repNodePos = openList.index(repNodeID)
            openList.pop(repNodePos)

#Main
initNode = utilities.initStSpace(sys.argv) #Creates the first node, with initial state space

nodeInsts  = [initNode] #nodeInsts stores all node structures, which are then referenced by their index in the open and closed lists
openList   = [0]    #Frontier list, starting with an initial node (represented by its index in nodeInsts)
closedList = []     #Explored list
if initNode == None:
    openList = []

#General search algorithm
while 1:
    if openList == []:
        break
    nodeID = UnifCostSel(openList) #The node with least evaluation function (g+h) is selected
    node   = nodeInsts[nodeID]

    if node.checkGoal(nodeInsts, closedList, sys.argv[1]):
        break

    closedList.append(nodeID)

    possNodes = node.expandNode(nodeID) #All possible nodes are expanded

    newNodes = [] #List of all nodes to be appended to open list: a subset of all possible children nodes
    for child in possNodes:
        existNode = utilities.compareNodes(child, openList, closedList, nodeInsts) #0:'New Node' | 1:'Node already in closedList' | node :'Node already in openList'
        UnifCostDecide(newNodes, child, existNode, nodeInsts, openList) #Processes each possible node to determine if it should be kept or discarded


    latestID     = len(nodeInsts)
    newNodesSize = len(newNodes)
    nodeInsts.extend(newNodes)
    UnifCostPlace(latestID, newNodesSize, openList) #Places node in openList as a priority queue