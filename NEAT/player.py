class player():
    def __init__(self, brain):
        self.brain = brain
        #För att undvika divide by 0 error
        self.fitness = 1