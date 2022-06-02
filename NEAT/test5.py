from genome import genome 
from connection import connection
import math
ply = genome()

ply.connections["0"] = connection(0,3,0)
ply.connections["0"].weight = 3.1


ply.connections["1"] = connection(1,3,1)
ply.connections["1"].weight = 7.9

ply.connections["2"] = connection(2,3,2)
ply.connections["2"].weight = 1.9

ply.initalizeNetwork()
ply.makeReady()

input = {}
input["1"] = 0.3
input["2"] = 1.0
output1 = ply.useNetwork(input)[0]

print(output1)


print(1 / (1 + math.e ** -1.7))