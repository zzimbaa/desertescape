import math
from . import genome
from matplotlib import pyplot as plt

def drawNetwork(genome):
    layers = genome.layers
    nodesInLayers = []
    mostNodesInOneLayer = 0 #Detta blir största X
    nodeCords = {}
    for layer in range(1,genome.layers + 1): 
        nodes = []
        for node in genome.nodes:
            if node.layer == layer:
                nodes.append(node.id)
        nodesInLayers.append(nodes)
        length = len(nodes)
        if length > mostNodesInOneLayer:
            mostNodesInOneLayer = length
    #plota alla nodes
    y = 0
    for layer in nodesInLayers:
        if len(layer) == mostNodesInOneLayer:
            X = 0
            for node in layer:
                nodeCords[str(node)] = [X, y]
                plt.plot(X, y, "ko")
                plt.annotate(node, (X, y))
                X += 1
        else:
            distans = (mostNodesInOneLayer - len(layer))/2
            X = distans
            for node in layer:
                nodeCords[str(node)] = [X, y]
                plt.plot(X, y, "ko")
                plt.annotate(node, (X, y))
                X += distans
        y += 1
    #plota connections
    for connection in genome.connections.values():
        #print(key)
        fromNodeId = str(connection.input)
        toNodeId = str(connection.output)
        X1 = nodeCords[fromNodeId][0]
        y1 = nodeCords[fromNodeId][1]
        X2 = nodeCords[toNodeId][0]
        y2 = nodeCords[toNodeId][1]
        if connection.enabled:
            plt.plot([X1, X2], [y1,y2], color="blue")
        else:
            plt.plot([X1, X2], [y1,y2], color="red")
    plt.grid(True)
    plt.show()



def printConnections(genome):
    for connection in genome.connections.values():
        print(connection.input, "to", connection.output)