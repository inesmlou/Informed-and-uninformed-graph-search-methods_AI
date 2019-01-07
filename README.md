# Informed-and-uninformed-graph-search-methods_AI
Find the set of operations (move, load, unload) necessary for a vehicle to transport a box (called cask, each with a certain weight) from a place in an environment to the exit point.
Project fo the course Artificial Intelligence and Decision Systems.

We model an environment given from an input file as a graph.
There are:
- Nodes: that correspond to physical location in the environment, and can be of three kinds: 
    Stacks - where the casks can be stored
    Crossings - Where the vehicle can move with the cask but not unload it
    Exit point - Where the vehicle should bring the goal cask to
    
- Indirect edges: connection between two nodes, with a certain length (cost)

From the initial position of all casks in multiple stacks, the vehicle has to do the necessary movements to let the desired cask be free (without any other cask on its way), so that it can load it and transport it into the exit point.
The solution should be optimal, which means that the sum of the costs in the sequence of actionst should be minimized.
These costs come from the actions of loading and loading casks, as well as moving along the edges, both deppending on the weight of the cask being used.
