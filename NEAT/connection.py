import random
import numpy.random
#Anta att vikten ligger mellan -1 och 1
class connection():
    
    def __init__(self, input, output, innonr):
        self.max_weight = 30
        self.input = input
        self.output = output
        self.weight = random.uniform(-1,1)
        self.enabled = True
        self.innovationnumber = innonr
    #Testa det här https://stackoverflow.com/questions/31708478/how-to-evolve-weights-of-a-neural-network-in-neuroevolution
    #Frågan är hur man ska mutera vikterna
    #Vikterna ska vara mellan -1 och 1
    #https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice Random choice med sannolikhet
    '''def mutate(self): #Med detta system kommer varenda vikt i ett nätverk gå igenom denna funktion. Det betyder att 
        randomInt = random.randint(0, 10)
        if randomInt <= 9: # 90% av tiden 
            choices = [self.normalMutation(), self.signChange(), self.diffMutate(), self.completeChange(), self.weight]
            probability = [0.7, 0.05, 0.1, 0.1, 0.05]
            weight = numpy.random.choice(choices, p=probability)
            self.weight = weight
'''
    def normalMutation(self):
        randomfloat = round(random.uniform(0.5, 1.5),2 ) #Hur mycket ska man avrunda?
        value = self.weight * randomfloat
        return value
    def signChange(self):
        value = self.weight * -1
        return value
    def diffMutate(self):
        randomfloat = round(random.uniform(0, 1),2 )
        choices = [True, False]
        if random.choice(choices):
            value = self.weight + randomfloat
        else:
            value = self.weight - randomfloat
        return value
    def completeChange(self):
        value = round(random.uniform(-1, 1),2 )
        return value
    
    
    def mutate(self):
        rand = random.random()
        if rand < 0.1: #ändra vikten helt
            self.weight = random.uniform(-1, 1) 
        else:
            self.weight += random.gauss(0,1)
        if self.weight > self.max_weight:
            self.weight = self.max_weight
        if self.weight < -self.max_weight:
            self.weight = -self.max_weight
