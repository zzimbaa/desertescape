#Databasen som har koll på alla innovationIds
class connectionhistory():
    def __init__(self):
        self.innovations = [] 
    
    #Dumt namnt
    #ger ID på anslutingen som mattas in
    #Ifall anslutningen redan finns i databasen får det ID:et
    #Annars sätts anslutningen in i databasen och tillges ett ID
    def isNew(self, input, output):
        for innoNr,connection in enumerate(self.innovations):
            if connection[0] == input and connection[1] == output: #Ifall detta är true finns det redan en sån connection i historian, Connection[0] är input etc
                return innoNr #get vilket innovation number
        self.innovations.append([input, output])
        return len(self.innovations) - 1 #Detta borde ge det innovation nummret som den nya connectionen får?

    #Oväsentlig funktion    
    # def historyExist(self,input, output):
    #     for innoNr,connection in enumerate(self.innovations):
    #         if connection[0] == input and connection[1] == output: #Ifall detta är true finns det redan en sån connection i historian, Connection[0] är input etc
    #             return True #get vilket innovation number
    #     return False
