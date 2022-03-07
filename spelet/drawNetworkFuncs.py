import pygame

def getRects(network, width, height):
    sWidth, eWitdh = width #Width = (startwidth, endwith)
    sHeight, eHeight = height
    
    width = eWitdh - sWidth #Totala längden
    height = eHeight - sHeight #Height systemet går från att toppen är y koordinat 0 
    
    layers = network.layers #Hur många layers
    neurons = network.nodes #Nodsen
    neuronlist = neuronList(network)
    rect_widths = width/layers #Hur mycket plats varje layer får ta upp
    current_left = sWidth #Vart någonstans vi börjar lägga upp rektanglarna
    circles = []
    for layer in range(1, layers + 1): #För varje layer
        left = current_left 
        right = left + rect_widths
        current_left = right        
        amount_neurons = neuronlist[layer - 1] #Hur många neuroner i den layern
        rect_heigts = round(height/amount_neurons) #Hur mycket plats i höjd varje delrektangel får ta upp
        current_top = sHeight
        current_layer = []
        #Beräkna vart varje delrektangels top och bot
        for nr in range(amount_neurons):
            #börja från toppen
            top = current_top
            bottom = current_top + rect_heigts
            current_top = bottom
            centerx = round((left + right)/2) #beräknar mitten koordinaten för X eftersom vi senare kommer lägga en cirkel på mittpunkten
            centery = round((top + bottom)/2)
            circles.append((centerx,centery))
    return circles

def assign_circle_to_node(circles,nodes): #Ger varje cirkel vi skapade ett id som representerar en node via en dict
    circleDict = {}
    sorted_nodes = sorted(nodes, key=lambda x: x.layer) #Ger en lista där neuroner är sorterade där de som är i layer 1 kommer först

    for key, node in enumerate(sorted_nodes):
        circleDict[str(node.id)] = circles[key]
    
    #Hacky fix till att nodsen hamnar på olika stället
    #Eftersom vi vet antalet input och output nodes kan vi sortera efteråt
    for i in range(0, 3 + 1): #+1 för bias 3 är antalet inputnodes
        circleDict[i] = circles[i]
    for i in range(1,3 + 1): #3 är antalet output nodes
        circleDict[i + 3 + 1] = circles[-i] # 3 är inputnodes
    return circleDict



def neuronList(network):
    neuronlist = []
    for i in range(network.layers):
        neuronlist.append(0)
    for node in network.nodes:
        layer = node.layer
        neuronlist[layer-1] += 1
    return neuronlist

def drawCircles(circles,screen):
    for key in circles:
        #x,y = circles[key]
        pygame.draw.circle(screen, pygame.Color(0,191,255), circles[key], 7)

def drawLines(network,circles,screen):
    connections = network.connections
    for conn in connections:
        conn = connections[conn]
        fromid = str(conn.input)
        toid = str(conn.output)
        color = None
        if conn.enabled:
            color = pygame.Color(0,0,255)
        else:
            color = pygame.Color(255,0,0)
        width = round(max(min(30, 2*abs(conn.weight)), 5)) #ändra den här så det är mer normalfördelat
        pygame.draw.line(screen, color, circles[fromid],circles[toid], width)

