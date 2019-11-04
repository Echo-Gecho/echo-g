import DAGraph
import random

'''
Author: Echo Gao
Last modified: 2019.10.31

[DAGraph]
[[ BlockDAG ]]
[BlockBackdoorDriver]

This module contains methods that are used to place blocks on the DAG
There's also an experiment module at the end mostly for debugging purposes.

- closeBackDoors(DAG)
    - This is the only public method in the module
    - It calls a bunch of other methods to block the least number of nodes
        such that there's no more node that has an unblocked path
        to both the exposure and outcome nodes
    - loops until no more backdoors

## Note:
- Heuristics reparir with min-conflict is adapted and used here in order to
    produce hopefully optimal result. In each iteration, all nodes that are
    not exposure or outcome nodes are tried and blocked, the resulted new
    number of backdoors are compared. The node to be actually blocked is
    randomly selected from a list of nodes that produces the least number
    of backdoors if blocked.
    - Note the this is local search, so, like, no guarantee it will reach
        the global minimum.

'''


## Globals used for the experiment
DAG1 = [ ("A","E"),
         ("A","C"),
         ("B","C"),
         ("B","D"),
         ("C","E"),
         ("C","D"),
         ("E","D") ]

'''
Start and Goal:
S = Vitamins
G = Birth defects

Other nodes:
PNC = prenatal care
SES = Maternal SES
DC = Difficulty conceiving
GN = Genetics
'''
DAG2 = [ ("S","G"),
         ("PNC","S"),
         ("PNC","G"),
         ("SES","S"),
         ("SES","PNC"),
         ("DC","PNC"),
         ("GN","DC"),
         ("GN","G") ]

'''
s = start = childhoodSES
g = goal = mortality

A = adultSES
U = unknown
'''
DAG3 = [ ("S","A"),
         ("S","G"),
         ("A","G"),
         ("U","A"),
         ("U","G") ]
## end globals

def closeBackDoors(DAG):
    blocked = []
    backdoors = findBackdoors(DAG)

    while len(backdoors) != 0:
        node_Backdoors = tryBlockDoors(DAG)
        minBackdoor = min(node_Backdoors.values())
        nodes = [k for k,v in node_Backdoors.items() if v == minBackdoor]
        chosenIdx = random.randint(0, len(nodes)-1)
        chosenNode = nodes[chosenIdx]
        blocked.append(chosenNode)
        DAG.blockNode(chosenNode)
        backdoors = findBackdoors(DAG)
    return blocked
    
    

def tryBlockDoors(DAG):
    # for each node in the graph, try block them,
    # and count how many backdoors are present after blocking them
    initialBackdoors = len(findBackdoors(DAG))
    
    # this records the number of backdoors in the graph resulted by
    # blocking the node
    nodeBackdoors = {}
    for aNode in DAG.graph:
        if aNode != DAG.exposure and aNode != DAG.outcome:
            testDAG = DAG.copyDAG()
            testDAG.blockNode(aNode)
            newBackdoors = len(findBackdoors(testDAG))
            nodeBackdoors[aNode] = newBackdoors

    return nodeBackdoors


def findBackdoors(DAG):
    backdoors = []
    shortestIdx = 0
    shortestStep = 999
    for aNode in DAG.graph:
        if aNode != DAG.exposure and aNode != DAG.outcome:
            b = DAG.connectEO(aNode)
            if len(b) > 0:
                backdoors.append(b)
    return backdoors


def experiment():
    print("Experiment!")
    print()
    print("closing for dag1")
    for i in range(10):
        print()
        dag1 = DAGraph.Graph(5,DAG1, "E", "D")
        blocked = closeBackDoors(dag1)
        print(blocked)

    print()
    print("closing for dag2")
    for j in range(10):
        print()
        dag2 = DAGraph.Graph(6,DAG2, "S", "G")
        blocked = closeBackDoors(dag2)
        print(blocked)

    print()
    print("closing for dag3")
    for k in range(10):
        print()
        dag3 = DAGraph.Graph(4,DAG3, "S", "G")
        blocked = closeBackDoors(dag3)
        print(blocked)

    print("\nDone")
    return 0


if __name__ == "__main__":
    experiment()
