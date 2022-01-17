#De som implementerar verkar bara låta lagret på en ny node vara = fromnode.layer + 1
from typing import NewType
from .history import connectionhistory
from .node import Node
from .connection import connection
import random
#import miscFuncs
from . import config
class genome():
    def __init__(self):
        self.nextnode = 1
        #Kanske borde använad en dictonary för nodsen, även för connections?
        self.nodes = [] #Biasnoden ska ha sitt värde = 0, Detta är i ordningen nodesen har kommit in i nätverket
        self.connections = {} #Alla connections som det nuvarande nätverket har i sina gener, Detta är i ordningen connections har kommit in i nätverket
        self.inputnodes = config.genomes["inputNodes"]
        self.outputnodes = config.genomes["outputNodes"]
        self.layers = 2
    
    def getOutputconnections(self, nodeId): #Ger alla enabled connections som en node ska skicka till
        connections = [] #Connections funktionen ska returna
        for connection in self.connections.values(): #Går igenom nätverkets connections
            input = connection.input
            if input == nodeId and connection.enabled:
                connections.append(connection)
        return connections #Kanske ska göra något om den är tom

    def initInputNodes(self):
        for i in range(1, self.inputnodes + 1): #Sätter i som värdet på varje input node och skapar nya nodes med layer = 1 eftersom det är input layer
            node = Node(self.nextnode, 1) #Skapar Node med nextnode som Id och lagret = 1
            self.nodes.append(node)
            self.nextnode += 1

    def initBiasNode(self): #Biasnode har värde = 0
        bias = Node(0, 1)
        bias.inputsum = 1
        self.nodes.append(bias)
    
    def initOutputNodes(self): #Känns som man borde kunna göra det här efter man har init gömda nodsen för att spara på prestanda, Körs egentligne
        for i in range(1, self.outputnodes + 1): #Sätter nextnode som värdet på varje output node och skapar nya nodes med layer = 2 eftersom det är output layer
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
    
    def connectNodes(self): # Går igenom alla connections som genome har och ger de relevanta connectionsarna till nodsen.
        for connection in self.connections.values():
            if connection.enabled: #Ge bara om connectionen faktiskt är igång
                fromNode = connection.input
                fromNode = self.getNodeFromId(fromNode)
                fromNode.outconnections.append(connection)

    def clearNetwork(self): #Gör detta snabbare om det går
        for node in self.nodes:
            if node.id == 0: #Inte om bias node
                node.outconnections = [] #Fixa så biasnoden har activationvalue och inputsum som konstanter
                continue 
            node.activationvalue = None
            node.inputsum = 0 #Kanske ska vara None
            node.outconnections = []
    
    def fullyConnected(self): #Behövs inte längre
        self.connectNodes() #Anledningen till detta är för jag tror att när en funktionen körs så är networket clearat såååå
        for node in self.nodes:#Går igenom varje node
            layer = node.layer
            antalConnections = len(node.outconnections) #Får antalet connections den noden har just nu
            nodesEfter = 0
            for searchNode in self.nodes: #tar fram alla nodes efter noden, maximalet antal connections är antalet nodes efter den
                if searchNode.layer > layer:
                    nodesEfter += 1
            if antalConnections != nodesEfter: #Ifall dessa två nummer inte är desamma betyder det att nätverket inte är fullt
                self.clearNetwork()
                return False
        self.clearNetwork()
        return True
        #KOLLA UPP LIST COMPREHENSIONS OCH LAMBDA
            
    def connectionExists(self, fromNodeId, toNodeId):
        for i in self.connections.values():
            if i.input == fromNodeId and i.output == toNodeId:
                return True
        return False

    def makeReady(self):
        self.clearNetwork()
        self.connectNodes()

    def useNetwork(self, dict): #dictionaryn innehåller input till input nodsen
        #Gå ingenom alla inputnodes och ändra deras inputsum
        for i in range(1,self.inputnodes + 1): #Börja inte på bias
            noden = self.getNodeFromId(i)
            value = dict[str(i)]
            noden.inputsum += value
        #Går igenom varje node i varje lager (börjar från input lager) och lägger på sin (activation value * weight) på alla outgoing connections i out nodens inputsum
        outputNodesValue = []
        for layer in range(1,self.layers + 1): #Detta går också igenom output layer?
            if layer == self.layers: #Ifall vi är på sista lagret alla output nodes
                for node in self.nodes:
                    if node.layer == layer:
                        outputNodesValue.append(self.getNodeFromId(node.id).sigmoid())
            else:
                for node in self.nodes:
                    if node.layer == layer:
                        node.sendvalue(self)
        #Få outputNodsens values

        #Clearar nodsen så funtkionen kan köras ien
        for node in self.nodes:
            if node.id == 0: #Inte om bias node
                continue 
            node.activationvalue = None
            node.inputsum = 0 #Kanske ska vara None
        return outputNodesValue


    def twoNodesToConnect(self): #Vad ifall det är en node med full connection. Det kanske finns ett sätt att använda det här än getNodeWithConnections
        randomNode = None
        layer = randomNode.layer
        possibleNodes = []
        for searchNode in self.nodes: #Går igenom alla nodesen
            if layer < searchNode.layer: #Om layer är lägre än search.layer är randomNode = fromNode vilket betyder att den får id1 för connectionExistsfunktionen
                id1 = randomNode.id
                id2 = searchNode.id
            elif layer < searchNode.layer: #Vice versa
                id1 = searchNode.id
                id2 = randomNode.id
            else: #Om de är i samma lager så gå bara till nästa node
                continue
            if not (self.connectionExists(id1, id2)): #Om connectionen inte existerar så lägg till NodeId i possible nodes
                possibleNodes.append(searchNode.id)
        
    def getNodeWithConnections(self):
        connectionDict = {}
        for node in self.nodes:#Går igenom varje node
            #Kolla om det är output layer
            layer = node.layer
            for searchNode in self.nodes: #tar fram alla nodes efter noden, maximalet antal connections är antalet nodes efter den
                if searchNode.layer > layer and not self.connectionExists(node.id, searchNode.id): #Kommer bli dubbelt för det kommer bli ex 1 2 och 2 1
                    #Om det här är True = nodsen är inte connectade med varandra
                    #Kan man ens appenda en dictionary?
                    try:
                        connectionDict[str(node.id)].append(searchNode.id)
                    except:
                        connectionDict[str(node.id)] = [searchNode.id]
        return connectionDict

    def mutateNode(self,history):
        #Du måste få index för connectionen
        self.clearNetwork() #DET HÄR BEHVÖS EGENTLIGEN INTE GÖRAS TYP MEN JAG GÖR DET ÄNDÅ FIXA DET SENARELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
        length = len(self.connections) #GÅR INTE ATT MUTERA EN NODE MELLAN TVÅ NODES SOM INTE HAR CONNECTIONS
        if length == 0: #Betyder att det inte går att mutera
            return
        tempList = list(self.connections.items()) #Långasmt? ska det ens vara list?
        innonr, randomConnection = random.choice(tempList) #Detta kanske går långsamt? du får en index
        self.connections[innonr].enabled = False #Måste den vara på från början för att det ska hända?
        weight = self.connections[innonr].weight
        fromNode = self.getNodeFromId(randomConnection.input)
        toNode = self.getNodeFromId(randomConnection.output)
        layer = fromNode.layer + 1
        
        if fromNode.layer + 1 == toNode.layer:
            self.layers += 1
            for node in self.nodes:
                if node.layer > fromNode.layer:
                    node.layer += 1
        newNode = Node(self.nextnode, layer)
        self.nextnode += 1
        self.nodes.append(newNode)
        #Skapa de två nya connectionsarna
        innonr = history.isNew(newNode.id, toNode.id)
        firstConnection = connection(newNode.id, toNode.id, innonr)
        firstConnection.weight = 1
        self.connections[str(innonr)] = firstConnection
        innonr = history.isNew(fromNode.id, newNode.id)
        secondConnection = connection(fromNode.id, newNode.id, innonr)
        #The new connectionleading into the new node receives a weight of 1, and the new connection leading out receives the same weight as the old connection
        secondConnection.weight = weight
        self.connections[str(innonr)] = secondConnection

    def mutateConnection(self, history): #Detta är inte effektivt.
        #Hur kollar man så att det faktiskt går att göra en ny connection
        #Pick random from node and to node
        nodeDict = self.getNodeWithConnections() #En dictonary med Nodeid som index där value är ett table med alla möjliga connections den noden kan ha
        if len(nodeDict) == 0: #Betyder att nätverket är fullt
            return
        fromNode = random.choice(list(nodeDict))
        toNode = random.choice(nodeDict[fromNode])
        fromNode = self.getNodeFromId(int(fromNode))
        toNode = self.getNodeFromId(toNode)
        if fromNode.layer > toNode.layer: #DETTA BETYDER ATT DET INTE FINNS RECURSIONS 
            temporary = fromNode
            fromNode = toNode #Ifall fromnode kommer i ett lager efter toNode så blir fromNode = toNode
            toNode = temporary
        if self.connectionExists(fromNode.id, toNode.id): #Det betyder att en connection redan finns (TA BORT?)
            return
        innovationnumber = history.isNew(fromNode.id, toNode.id)
        newconnection = connection(fromNode.id, toNode.id, innovationnumber) # Du måste sätta en random vikt på connectionen också
        self.connections[str(innovationnumber)] = newconnection

    def mutateRemoveNode(self): #Tar bort en node och alla connections som har med den noden att göra
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
        print(type(self.connections))
        self.connections = {key:val for key, val in self.connections.items() if (val.input != id and val.output != id)}
    
    def mutate(self,history):

        if random.random() < config.genomes["mutateWeightsProb"]: #Mutera vikterna 80% av tiden
            for connection in self.connections.values():
                connection.mutate()
        
        if random.random() < config.genomes["mutateConnection"] or len(self.connections) == 0: #Mutera ny connection 5% av tiden
            self.mutateConnection(history)
        
        if random.random() < config.genomes["mutateNodeProb"]: #Mutera ny node 1% av tiden
            #if len(self.nodes) < 6:
            self.mutateNode(history)

        

