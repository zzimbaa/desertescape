import numpy
import math
from .connection import connection
class Node():
    def __init__(self, id, layer):
        self.id = id
        self.layer = layer
        self.inputsum = 0 #Detta kanske ska vara None
        self.activationvalue = 0
        self.outconnections = []


    def sigmoid(self):
        #VIKTERNA BLIR SKIT HÖGA
        z = self.inputsum
        #print(z)
        #print(self.inputsum)
        #return 1/(1 + (math.exp(-self.inputsum)))
        z = max(-60.0, min(60.0, 5.0 * z))
        #print(z)
        return 1.0 / (1.0 + math.exp(-z))

    def sendvalue(self, genome): 
        if self.layer != 1:
            activationvalue = self.sigmoid()
        else:
            activationvalue = self.inputsum
        for connection in self.outconnections:  #Går igenom all utgående connections för denna noden och skicka ut activationvalue * vikt
            if connection.enabled: #Ifall den inte är enabled så skicka inte
                nodeid = connection.output
                weight = connection.weight
                #if weight > 5:
                    #print(weight)
                node = genome.getNodeFromId(nodeid)
                #print(weight * activationvalue )
                node.inputsum += weight * activationvalue 
#1,7310