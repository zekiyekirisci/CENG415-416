import networkx as nx
import random

#2
g=nx.read_edgelist('facebook_combined.txt',create_using=nx.Graph(),nodetype=int)
nodelist = dict(g.nodes())

#make all values zeros
nodelist = dict.fromkeys(nodelist,0)

#set val 1
val=1

#3
randomNode = random.choice(list(nodelist.keys()))

#4
neighbor_list=list(g.neighbors(randomNode))
nodelist[randomNode] = val

#5
number_of_rounds = 0

#6
infected_node_count = 1
while len(nodelist) != infected_node_count:
    for key in nodelist.keys():
        neighborNode=random.choice(list(g.neighbors(key)))
        if ((nodelist[key]==val) & (nodelist[neighborNode] == 0)): #g.neighbors(key)=neighborNode
            nodelist[neighborNode] = val #neighbor.val=node.val
            infected_node_count = infected_node_count + 1
           
        elif ((nodelist[key] == 0) & (nodelist[neighborNode] == val)): 
            nodelist[key] = nodelist[neighborNode]
            infected_node_count = infected_node_count + 1
            
    number_of_rounds = number_of_rounds + 1
