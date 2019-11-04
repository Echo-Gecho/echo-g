import DAGraph
import BlockDAG

'''
Author: Echo Gao
Last modified: 2019.10.31

[DAGraph]
[BlockDAG]
[[ BlockBackdoorDriver ]]

This is the driver module for this program
also contains I/O functions used by the autoDriver

manual mode - user manually input graph, output to console
automatic - read graphs from file, output to file

For each graph, produce N = 10 suggestions, because this program
utilizes local search and random. Hopefully it will reach its global
maxima by repeating the process. 

'''

FILEIN = "DAGSamples.txt"
FILEOUT = "DAGResults.txt"
N = 20    # Change N to produce more or less suggestions

def manualDriver():
    userInputA = 0
    numNodes = int(input("Enter the number of nodes in the DAG: "))
    exposure = input("Enter the exposure of interest: ")
    outcome = input("Enter the outcome of interest: ")
    dag = DAGraph.Graph(numNodes, [], exposure, outcome)
    dag.addEdge(exposure, outcome)
    
    print("Enter 'DONE' to stop enter edges.")
    while userInputA != "DONE":
        userInput = input("Input edge in format of 'start,finish': ")
        try:
            userInputA, userInputB = userInput.split(',')
            dag.addEdge(userInputA.upper().strip(), userInputB.upper().strip())
        except:
            if userInput.upper() == 'DONE':
                break
            else:
                print("invalid input, try again")
                continue
        
    print("Done creating DAG:")
    dag.printGraph()
    
    for i in range(10):
        dagcopy = dag.copyDAG()
        print("The nodes to be blocked:")
        blocked = BlockDAG.closeBackDoors(dagcopy)
        print(blocked)
    return 0


def autoDriver(fileIn, fileOut):
    graphs = readFile(fileIn)
    result = []
    for graph in graphs:
        numNode = countNode(graph)
        e = graph[0][0]
        o = graph[0][1]
        dag = DAGraph.Graph(numNode, graph,e,o)
        r = repeatExp(dag, N)
        result.append(r)
    writeToFile(result, FILEOUT)
    return 0


def repeatExp(DAG, times):
    result = []
    for i in range(times):
        testDag = DAG.copyDAG()
        blocked = BlockDAG.closeBackDoors(testDag)
        result.append(blocked)
    return result


def countNode(DAG):
    nodeSet = []
    for edge in DAG:
        if edge[0] not in nodeSet:
            nodeSet.append(edge[0])
        if edge[1] not in nodeSet:
            nodeSet.append(edge[1])
    print(len(nodeSet))
    return len(nodeSet)

# I/O functions start here
def readFile(name):
    inFile = open(name, 'r')
    fileContent = inFile.read().splitlines()
    graphs = separateGraphs(fileContent)
    inFile.close()
    return graphs

def writeToFile(result, outName):
    file = open(outName, 'w')
    counter = 1
    for experiment in result:
        file.write("Result for DAG "+ str(counter)+ " \n")
        for i in range(len(experiment)):
            file.write(str(experiment[i])+'\n')
        file.write('\n')
        counter += 1
    file.close()

def separateGraphs(content):
    graphs = []
    aDag = []
    e = ""
    o = ""
    for line in content:
        if line != '':
            if line[0] == '-':
                e,o = line[1:].split(',')
                aDag.insert(0,(e,o))
            else:
                aDag.append(tuple(line.split(',')))
        else:
            graphs.append(aDag)
            aDag = []
    graphs.append(aDag)
    return graphs

# I/O functions ends
        

if __name__ == "__main__": 
    fin = readFile(FILEIN)
    print(fin)
    autoDriver(FILEIN, FILEOUT)
    #manualDriver()

