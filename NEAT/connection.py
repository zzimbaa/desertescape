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
    
    def mutate(self):
        rand = random.random()
        if rand < 0.1: #ändra vikten helt
            self.weight = random.uniform(-1, 1) 
        else: #Ändra lite
            self.weight += random.gauss(0,1)
        if self.weight > self.max_weight:
            self.weight = self.max_weight
        if self.weight < -self.max_weight:
            self.weight = -self.max_weight

    #Olika sätt att mutera vikterna
    #Användes inte
    # def normalMutation(self):
    #     randomfloat = round(random.uniform(0.5, 1.5),2 ) 
    #     value = self.weight * randomfloat
    #     return value
    # def signChange(self):
    #     value = self.weight * -1
    #     return value
    # def diffMutate(self):
    #     randomfloat = round(random.uniform(0, 1),2 )
    #     choices = [True, False]
    #     if random.choice(choices):
    #         value = self.weight + randomfloat
    #     else:
    #         value = self.weight - randomfloat
    #     return value
    # def completeChange(self):
    #     value = round(random.uniform(-1, 1),2 )
    #     return value