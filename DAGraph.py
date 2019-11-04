import queue
import copy

'''
Author: Echo Gao
Last modified: 2019.10.31

[[ DAGraph ]]
[BlockDAG]
[BlockBackdoorDriver]

Graph Class:
Holds a Graph object that contains the DAG, and related methods

Methods:
- Constructor
    Graph(numNodes, edgeList, exposure, outcome)
    - edgeList can be initialized to []
    - numNodes is used to check legality of adding edges
        - this is a terrible error checking method i know
            but something's better than nothing
    - exposure and outcome needs to be pre-specified for pathfinding
- addEdge(edgeStart, edgeEnd)
    - error handling includes:
        - check no duplicate edges
        - check number of nodes is less than the pre-specified value
            in case of typo mostly
- printGraph()
    - pretty prints the graph
- connectEO(node)
    - this method finds the shortest paths towards exp and otc from node
        and connect them into a list that represents the path from e to o thru n
    - returns the list that contains the "path"
- blockNode(node)
    - this method blocks the node and adds association
- copyDAG()
    - deepcopys the DAG object

## Note:
- A* search algorithm is used to find the shortest path from the specified node
    to exposure and outcome nodes. This method should be both optimal and complete. 

'''

class Graph: 
   
    def __init__(self, n, DAG, e, o): 
        self.numNodes = n #No. of vertices 
        self.graph = {}
        self.exposure = e
        self.outcome = o
        for edge in DAG:
            self.addEdge(edge[0], edge[1])
   
    # function to add an edge to graph 
    def addEdge(self, a, b):
        if (a not in self.graph):
            self.graph[a] = [b]
        else:
            if b not in self.graph[a]:
                self.graph[a].append(b)
                
        if len(self.graph) >= self.numNodes:
            self.printGraph()
            raise Exception("Number of nodes exceeds specification!")


    def printGraph(self):
        for k in self.graph:
            print(k)
            print(self.graph[k])


    def aStar(self, start, end):
        g = self.graph
        frontier = queue.PriorityQueue()
        frontier.put((0,start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        reached = False

        while not frontier.empty():
            current = frontier.get()
            currentNode = current[1]
            
            if currentNode == end:
                reached = True
                break
            if currentNode == self.exposure and end != self.exposure:
                reached = False
                continue      
            if currentNode == self.outcome and end != self.outcome:
                reached = False
                continue

            if (currentNode in self.graph):
                for nextN in g[currentNode]:
                    new_cost = cost_so_far[currentNode] + 1
                    if nextN not in cost_so_far or new_cost < cost_so_far[nextN]:
                        cost_so_far[nextN] = new_cost
                        priority = new_cost + 1
                        frontier.put((priority, nextN))
                        came_from[nextN] = currentNode
                        
        if reached:
            path, steps = self.makePath(came_from, start, end)
        else:
            path = []
            steps = 0
        return path, reached, steps


    def makePath(self,came_from, start, goal):
        current = goal
        path = [current]
        while current != start and came_from[current] != start:
            current = came_from[current]
            path.insert(0,current)
        path.insert(0,start)
        steps = len(path)-1
        return path, steps


    def connectEO(self, node):
        exp = self.exposure
        otc = self.outcome
        routeToE, toEYes, stepToE = self.aStar(node, exp)
        routeToO, toOYes, stepToO = self.aStar(node, otc)
        
        if toEYes and toOYes:
            routeToE.reverse()
            p = routeToE + routeToO[1:]
            return p
        else:
            return []


    def blockNode(self, node):
        numIn = 0
        nodeIn = []
        for aVertex in self.graph:
            if node in self.graph[aVertex]:
                nodeIn.append(aVertex)
                numIn += 1

        if numIn > 1:
            self.addAssociation(nodeIn)

        self.graph.pop(node)
        return


    def addAssociation(self, nodeList):
        for aNode in nodeList:
            for anotherNode in nodeList:
                if aNode != anotherNode:
                    self.addEdge(aNode, anotherNode)
        return


    def copyDAG(self):
        newDAG = copy.deepcopy(self)
        return newDAG
        


#test
if __name__ == "__main__":
    DAG1 = [ ("A","E"),
             ("A","C"),
             ("B","C"),
             ("B","D"),
             ("C","E"),
             ("C","D"),
             ("E","D") ]
    dag1 = Graph(5, DAG1, "E", "D")
    newdag1 = dag1.copyDAG()

    print("test copy 1")
    newdag1.printGraph()

    for edge in DAG1:
        dag1.addEdge(edge[0], edge[1])
    dag1.printGraph()

    print()
    print("A->D,",dag1.aStar("A","D"))
    print("A->E,",dag1.aStar("A","E"))
    print("C->E,",dag1.aStar("C","E"))
    print("C->D,",dag1.aStar("C","D"))
    print("B->E,",dag1.aStar("B","E"))
    print("B->D,",dag1.aStar("B","D"))
    print("A->B,",dag1.aStar("A","B"))
    print()
    print(dag1.connectEO("A"))
    print(dag1.connectEO("B"))
    print(dag1.connectEO("C"))
    print()


    print("test copy 2")
    newdag1.blockNode("C")
    print("original")
    dag1.printGraph()
    print("altered")
    newdag1.printGraph()
