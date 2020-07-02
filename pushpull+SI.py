import networkx as nx
import random

#2
g=nx.read_edgelist('facebook_combined.txt',create_using=nx.Graph(),nodetype=int)
allList = dict(g.nodes()) #sum of sus+infected nodes
susNodeList = list(g.nodes())
infectedList = list()

#make all values zeros
allList = dict.fromkeys(allList,0)

#set val 1
val=1

#3
randomNode = random.choice(list(allList.keys()))

#4
neighbor_list=list(g.neighbors(randomNode))
allList[randomNode] = val

#susceptibleNodeList.remove(randomNode)
susNodeList.remove(randomNode)

#infectedNodeList.add(randomNode)
infectedList.append(randomNode)

print (infectedList)
#5
number_of_rounds = 0
round_of_for=0
#6
infected_node_count = 1

print (len(dict(g.nodes())))

while len(allList) != infected_node_count:
    for key in allList.keys():
        neighborNode=random.choice(list(g.neighbors(key)))
        if ((allList[key]==val) & (allList[neighborNode] == 0)):
            #g.neighbors(key)=neighborNode
            allList[neighborNode] = val #neighbor.val=node.val
            susNodeList.remove(neighborNode)
            infectedList.append(neighborNode)
            infected_node_count = infected_node_count + 1
           
        elif ((allList[key] == 0) & (allList[neighborNode] == val)): 
            allList[key] = allList[neighborNode]
            susNodeList.remove(key)
            infectedList.append(key)
            infected_node_count = infected_node_count + 1
        round_of_for = round_of_for + 1
    number_of_rounds = number_of_rounds + 1
