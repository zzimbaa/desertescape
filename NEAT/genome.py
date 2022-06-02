from typing import NewType
from .history import connectionhistory
from .node import Node
from .connection import connection
import random
from . import config
class genome():
    def __init__(self):
        #används för att hålla reda på vilket ID en ny node ska få
        self.nextnode = 1 
        self.nodes = [] 
        self.connections = {}
        self.inputnodes = config.genomes["inputNodes"]
        self.outputnodes = config.genomes["outputNodes"]
        self.layers = 2
    
    def initInputNodes(self):
        #Sätter i som värdet på varje input node och skapar nya nodes med layer = 1 eftersom det är input layer
        for i in range(1, self.inputnodes + 1): 
            node = Node(self.nextnode, 1) 
            self.nodes.append(node)
            self.nextnode += 1

    def initBiasNode(self): 
        bias = Node(0, 1) #Biasnode har värde = 0
        bias.inputsum = 1 #Konstant
        self.nodes.append(bias)
    
    #skapar motoriska nodsen
    def initOutputNodes(self): 
        #Sätter nextnode som värdet på varje output node och skapar nya nodes med layer = 2 eftersom det är output layer
        for i in range(1, self.outputnodes + 1): 
            node = Node(self.nextnode, 2) #Skapar Node med nextnode som Id och lagret = 1
            self.nodes.append(node)
            self.nextnode += 1
    
    def initalizeNetwork(self): #Behövs bara köras första gången nätverket går igång
        self.initBiasNode()
        self.initInputNodes()
        self.initOutputNodes()
    
    def getNodeFromId(self, id): #Säger säg självt
        for node in self.nodes:
            if node.id == id:
                return node

    # Går igenom alla anslutningar som en genome har och ger de relevanta anslutningarna till neuronerna
    #Så neuronerna skickar sitt aktiveringsvärde vidare till rätt neuroner
    def connectNodes(self): 
        for connection in self.connections.values():
            if connection.enabled: #Ge bara om anslutningen faktiskt är igång
                fromNode = connection.input
                fromNode = self.getNodeFromId(fromNode)
                fromNode.outconnections.append(connection)

    #Tömmer neuroner inför nästa körning
    def clearNetwork(self): 
        for node in self.nodes:
            if node.id == 0: #Inte om bias node
                node.outconnections = []
                continue 
            node.activationvalue = None
            node.inputsum = 0 
            node.outconnections = []

    #Kollar om en anslutning existerar
    def connectionExists(self, fromNodeId, toNodeId):
        for i in self.connections.values():
            if i.input == fromNodeId and i.output == toNodeId:
                return True
        return False

    def makeReady(self):
        self.clearNetwork()
        self.connectNodes()

    def useNetwork(self, dict): 
        #Gå ingenom alla inputnodes och ändra deras inputsum
        for i in range(1,self.inputnodes + 1): #Börja inte på bias
            noden = self.getNodeFromId(i)
            value = dict[str(i)]
            noden.inputsum += value
        #Går igenom varje node i varje lager (börjar från input lager) och lägger på sin (activation value * weight) på alla outgoing connections i out nodens inputsum
        outputNodesValue = []
        for layer in range(1,self.layers + 1): 
            #Ifall vi är på sista lagret ta data ur neuroner
            if layer == self.layers: 
                for node in self.nodes:
                    if node.layer == layer:
                        outputNodesValue.append(self.getNodeFromId(node.id).sigmoid())
            #Annars skicka värdet till anslutande neuroner
            else:
                for node in self.nodes:
                    if node.layer == layer:
                        node.sendvalue(self)

        #Städar neuronerna så funktionen kan köras igen
        for node in self.nodes:
            if node.id == 0: #Inte om bias node
                continue 
            node.activationvalue = None
            node.inputsum = 0 #Kanske ska vara None
        return outputNodesValue

    #Hittar två neuroner som går att anslutas
    def twoNodesToConnect(self): 
        randomNode = None
        layer = randomNode.layer
        possibleNodes = []
        for searchNode in self.nodes: #Går igenom alla nodesen
            #Om layer är lägre än search.layer är randomNode = fromNode vilket betyder att den får id1 för connectionExists funktionen
            if layer < searchNode.layer: 
                id1 = randomNode.id
                id2 = searchNode.id
            elif layer < searchNode.layer: #Vice versa
                id1 = searchNode.id
                id2 = randomNode.id
            else: #Om de är i samma lager så gå bara till nästa node
                continue
            #Om anslutningen inte existerar lägg till NodeId i possible nodes
            if not (self.connectionExists(id1, id2)): 
                possibleNodes.append(searchNode.id)
    
    #Skapar en dict där varja neuron har en lista
    #med alla neuroner den kan anslutas till
    def getNodeWithConnections(self):
        connectionDict = {}
        for node in self.nodes:#Går igenom varje node
            layer = node.layer
            for searchNode in self.nodes: 
                if searchNode.layer > layer and not self.connectionExists(node.id, searchNode.id): 
                    try:
                        connectionDict[str(node.id)].append(searchNode.id)
                    except:
                        connectionDict[str(node.id)] = [searchNode.id]
        return connectionDict


    def mutateNode(self,history):
        self.clearNetwork() 
        length = len(self.connections) 
        if length == 0: #Betyder att det inte går att mutera
            return
        tempList = list(self.connections.items()) 
        #Tar en slumpmässig anslutning och sätter en neuron där
        innonr, randomConnection = random.choice(tempList) 
        #Enligt NEAT ska den valda anslutningen deaktiveras
        #efter ny neuron hamnar emellan
        self.connections[innonr].enabled = False 
        weight = self.connections[innonr].weight
        fromNode = self.getNodeFromId(randomConnection.input)
        toNode = self.getNodeFromId(randomConnection.output)
        layer = fromNode.layer + 1
        #Fixar så att ifall ett nytt lager måste skapas
        #korrigeras de befintliga neuronernas lager
        if fromNode.layer + 1 == toNode.layer:
            self.layers += 1
            for node in self.nodes:
                if node.layer > fromNode.layer:
                    node.layer += 1
        newNode = Node(self.nextnode, layer)
        self.nextnode += 1
        self.nodes.append(newNode)
        #Skapa de två nya anslutningarna
        #The new connection leading into the new node receives a weight of 1, 
        #and the new connection leading out receives the same weight as the old connection
        innonr = history.isNew(newNode.id, toNode.id)
        firstConnection = connection(newNode.id, toNode.id, innonr)
        firstConnection.weight = 1
        self.connections[str(innonr)] = firstConnection
        innonr = history.isNew(fromNode.id, newNode.id)
        secondConnection = connection(fromNode.id, newNode.id, innonr)
        secondConnection.weight = weight
        self.connections[str(innonr)] = secondConnection

    def mutateConnection(self, history): 
        #En dictonary med Nodeid som index där value är en lista med alla möjliga connections den neuronen kan ha
        nodeDict = self.getNodeWithConnections() 
        if len(nodeDict) == 0: #Betyder att nätverket är fullt
            return
        fromNode = random.choice(list(nodeDict))
        toNode = random.choice(nodeDict[fromNode])
        fromNode = self.getNodeFromId(int(fromNode))
        toNode = self.getNodeFromId(toNode)
        if fromNode.layer > toNode.layer: 
            temporary = fromNode
            fromNode = toNode #Ifall fromnode kommer i ett lager efter toNode så blir fromNode = toNode
            toNode = temporary
        #Om anslutningen redan finns 
        #körs funktionen igen för att hitta nya neuroner
        if self.connectionExists(fromNode.id, toNode.id): 
            self.mutateConnection(history)
            return
        #Skapar nya anslutningen
        innovationnumber = history.isNew(fromNode.id, toNode.id)
        newconnection = connection(fromNode.id, toNode.id, innovationnumber) 
        self.connections[str(innovationnumber)] = newconnection

    #Tar bort en node och alla connections som har med den noden att göra
    #Hann aldrig implementera denna funktion i algoritmen
    #Skulle också göra removeConnection
    def mutateRemoveNode(self):
        i = True
        randomNode = None
        while i:
            randomNode = random.choice(self.nodes)
            if randomNode.layer == 1 or randomNode.layer == self.layers: #Ifall det är output nodes eller inputnodes
                continue
            i = False
        id = randomNode.id
        self.nodes.remove(randomNode) #Tar bort den noden från node listan, tror att det funkar...
        #Tar bort alla connections som är kopplat till den noden
        self.connections = {key:val for key, val in self.connections.items() if (val.input != id and val.output != id)}
    
    def mutate(self,history):

        if random.random() < config.genomes["mutateWeightsProb"]: 
            for connection in self.connections.values():
                connection.mutate()
        
        if random.random() < config.genomes["mutateConnection"] or len(self.connections) == 0: 
            self.mutateConnection(history)
        
        if random.random() < config.genomes["mutateNodeProb"]: 
            self.mutateNode(history)

        

