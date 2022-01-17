#En class som heter typ innovation och sen bara gå igenom alla objekten.
class connectionhistory():
    def __init__(self):
        self.innovations = [] #Innovativa connections Anledningen till nollan är så att innovation numbers inte börjar på index 0 och så kan man returna 0 eventuellt
    
    def isNew(self, input, output):
        for innoNr,connection in enumerate(self.innovations):
            if connection[0] == input and connection[1] == output: #Ifall detta är true finns det redan en sån connection i historian, Connection[0] är input etc
                return innoNr #get vilket innovation number
        self.innovations.append([input, output])
        return len(self.innovations) - 1 #Detta borde ge det innovation nummret som den nya connectionen får?
    
    def historyExist(self,input, output):
        for innoNr,connection in enumerate(self.innovations):
            if connection[0] == input and connection[1] == output: #Ifall detta är true finns det redan en sån connection i historian, Connection[0] är input etc
                return True #get vilket innovation number
        return False
