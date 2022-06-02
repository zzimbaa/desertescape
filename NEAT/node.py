import numpy
import math
from .connection import connection
class Node():
    def __init__(self, id, layer):
        self.id = id
        self.layer = layer
        self.inputsum = 0 
        self.activationvalue = 0
        self.outconnections = []

    #Aktiveringsfunktionen som används
    def sigmoid(self):
        z = self.inputsum
        z = max(-60.0, min(60.0, 5.0 * z))
        return 1.0 / (1.0 + math.exp(-z))

    #Skickar sitt aktiveringsvärde
    #till alla utgående anslutningar
    def sendvalue(self, genome): 
        #Datan in i input_layer ska inte
        #gå igenom sigmoid funktionen
        if self.layer != 1:
            activationvalue = self.sigmoid()
        else:
            activationvalue = self.inputsum

        #Går igenom all utgående anslutningar skickar ut activationvalue * vikt
        for connection in self.outconnections:  
            if connection.enabled: #Ifall den inte är aktiverad,skicka inte
                nodeid = connection.output
                weight = connection.weight
                node = genome.getNodeFromId(nodeid)
                node.inputsum += weight * activationvalue 
