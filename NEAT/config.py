

genomes = dict(
    mutateNodeProb = 0.01, #chans att mutera en ny nod
    mutateConnection = 0.05, #Chans att mutera ny connection
    mutateWeightsProb = 0.7, #Chans att mutera vikterna
    inputNodes = 1, #Antal input nodes
    outputNodes = 3, #Antal output nodes
)

specie = dict(
    compThreshold = 3, #Gränsen för att combatilbily funktionen
    disJointCo = 1, #Koeffcienten för disjoint och excess genes i comp funktionen
    weightDiffCoefficent = 0.4 #Koeffcienten för vikterna i comp funktionen
)

populations = dict(
    size = 10, #Antal individer per generation
    stale = 30 #Hur många generationer kan en art gå igenom utan någon fitnessökning innan den dör
)

connections = dict(
    maxWeight = 30 #Max weight for connections (It minimum is the same but a negative sign)
)