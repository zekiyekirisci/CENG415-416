import facebook
import time
import numpy
import random

start = time.time()

totalAware=0
totalPI=0
totalNI=0
totalRemoved=0
#ignorant aware PI NI removed
# load the network
facebook.load_network()

interest = dict(facebook.network.nodes())
interest = dict.fromkeys(interest,0)

#her bir nod mesajı hangi yönde yayiyor 1-pozitif 2-negatif 0-yayılım yok
directionOfMsg = dict(facebook.network.nodes())
directionOfMsg = dict.fromkeys(directionOfMsg,0)

#her bir noda rumor kac kere gelmis
rumorCount = dict(facebook.network.nodes())
rumorCount = dict.fromkeys(rumorCount,0)

#nodeların stateleri value olarak tutuluyor 0-ignorant 1-aware 2-PI 3-removed 4-NI
allList = dict(facebook.network.nodes())
allList = dict.fromkeys(allList,0)

ignorantNodeList = list(facebook.network.nodes())

awareNodeList = []

piNodeList = []

niNodeList = []

removedNodeList = []

#random choosing of first node
randomNode = random.choice(list(allList.keys()))
ignorantNodeList.remove(randomNode)
piNodeList.append(randomNode)
totalAware = totalAware+1
totalPI = totalPI+1
allList[randomNode] = 2
directionOfMsg[randomNode] = 1
interest[randomNode]=20

number_of_for = 0
number_of_rounds = 0
ctr=4039
thresholdValue=100
compareThreshold=30 #between 2 nodes and msg
#creating a message
msg= numpy.tile(0,len(facebook.network.nodes[4]['features']))
msgfeat = random.randint(0, len(facebook.network.nodes[4]['features']))
msg[msgfeat] = 2
print(type(msg))
print (msg)


def decisionFromAware(nodeId):
    
    if((interest[nodeId] >= thresholdValue) & (rumorCount[nodeId]>5)):
        allList[nodeId] = 2 #positive Infected
        global totalPI
        totalPI = totalPI + 1
        directionOfMsg[nodeId] = 1
        awareNodeList.remove(nodeId)
        piNodeList.append(nodeId)
        
    elif((interest[nodeId] < thresholdValue) and (interest[nodeId] > -thresholdValue)):
        allList[nodeId] = 1 #stay in aware state
        rumorCount[nodeId] = rumorCount[nodeId] + 1
    
    elif((interest[nodeId] <= -thresholdValue) & (rumorCount[nodeId]>5)):
        allList[nodeId] = 4 #NegativeInfected
        global totalNI
        totalNI = totalNI + 1
        directionOfMsg[nodeId] = 2
        awareNodeList.remove(nodeId)
        niNodeList.append(nodeId)
       
        
def updateInterest(nodeId, totalInterest):
    
    currentInterest = interest[nodeId] + totalInterest
    interest[nodeId] = currentInterest
    return currentInterest


def decisionFromPI(nodeId):
    
    if((interest[nodeId]>=thresholdValue)):
        allList[nodeId] = 2 #positive Infected

    elif((interest[nodeId]<thresholdValue) and (interest[nodeId] > -thresholdValue)):
        allList[nodeId] = 3 #removed
        global totalRemoved
        totalRemoved = totalRemoved + 1
        directionOfMsg[nodeId] = 0
        piNodeList.remove(nodeId)
        removedNodeList.append(nodeId)
    
    elif((interest[nodeId]<=-thresholdValue)):
        allList[nodeId] = 4 #NegativeInfected
        global totalNI
        totalNI = totalNI + 1
        directionOfMsg[nodeId] = 2
        piNodeList.remove(nodeId)
        niNodeList.append(nodeId)
       
   
def decisionFromNI(nodeId):
    
    if((interest[nodeId]>=thresholdValue)):
        allList[nodeId] = 2 #positive Infected
        global totalPI
        totalPI = totalPI + 1
        directionOfMsg[nodeId] = 1
        niNodeList.remove(nodeId)
        piNodeList.append(nodeId)
        
    elif((interest[nodeId]<thresholdValue) and (interest[nodeId] > -thresholdValue)):
        allList[nodeId] = 3 #removed
        global totalRemoved
        totalRemoved = totalRemoved + 1
        directionOfMsg[nodeId] = 0
        niNodeList.remove(nodeId)
        removedNodeList.append(nodeId)
    
    elif((interest[nodeId]<=-thresholdValue)):
        allList[nodeId] = 4 #NegativeInfected
       
   
    
    
while (ctr >= number_of_rounds):
    for key in allList.keys():
        neighborlist = [item[1] for item in list(facebook.network.edges(key))]
        neighborNode=random.choice(neighborlist)
        if (((0 < allList[key] < 4) or (0 < allList[neighborNode] < 4)) and not(allList[neighborNode]==allList[key]==1)):
            rumorCount[neighborNode] = rumorCount[neighborNode] + 1
            #calculate for neighbor
            neighborInterest = facebook.totalInterest(facebook.network.nodes[key]['features'], facebook.network.nodes[neighborNode]['features'], key, msg)
            
            if(directionOfMsg[key] == 1):
                if(neighborInterest>compareThreshold):    #aradaki total relation
                    interest[neighborNode] = interest[neighborNode] + neighborInterest
                else:
                    interest[neighborNode] = interest[neighborNode] - neighborInterest
                    
                if(allList[neighborNode] == 0): #mesaj ilk kez geldi ignorant->aware
                    totalAware = totalAware+1
                    allList[neighborNode] = 1
                    ignorantNodeList.remove(neighborNode)
                    awareNodeList.append(neighborNode)
                
                elif(allList[neighborNode]==1):
                    decisionFromAware(neighborNode)
                   
                elif(allList[neighborNode]==2):
                    decisionFromPI(neighborNode)
                    
                elif(allList[neighborNode]==4):
                    decisionFromNI(neighborNode)
                    
            elif(directionOfMsg[key] == 2):
                if(neighborInterest>compareThreshold):
                    interest[neighborNode] = interest[neighborNode] - neighborInterest
                    
                else:
                    interest[neighborNode] = interest[neighborNode] + neighborInterest
           
                if(allList[neighborNode] == 0): #mesaj ilk kez geldi ignorant->aware
                    allList[neighborNode] = 1
                    totalAware = totalAware+1
                    ignorantNodeList.remove(neighborNode)
                    awareNodeList.append(neighborNode)
                
                elif(allList[neighborNode]==1):
                    decisionFromAware(neighborNode)
                   
                elif(allList[neighborNode]==2):
                    decisionFromPI(neighborNode)
                    
                elif(allList[neighborNode]==4):
                    decisionFromNI(neighborNode)
                
            #calculate for source=key
            sourceInterest = facebook.totalInterest(facebook.network.nodes[neighborNode]['features'], facebook.network.nodes[key]['features'], neighborNode, msg)
    
            rumorCount[key] = rumorCount[key] + 1
        
            if(directionOfMsg[neighborNode] == 1):
                if(sourceInterest>compareThreshold):
                    interest[key] = interest[key] + sourceInterest
                else:
                    interest[key] = interest[key] - sourceInterest
                    
                if(allList[key]==0):
                    allList[key] = 1
                    totalAware = totalAware+1
                    ignorantNodeList.remove(key)
                    awareNodeList.append(key)
                    
                if(allList[key]==1):
                    decisionFromAware(key)
                    
                if(allList[key]==2):
                    decisionFromPI(key)
                    
                elif(allList[key]==4):
                    decisionFromNI(key)                
            
            
            elif(directionOfMsg[neighborNode] == 2):
                if(sourceInterest>compareThreshold):
                    interest[key] = interest[key] - sourceInterest
                else:
                    interest[key] = interest[key] + sourceInterest
           
                if(allList[key]==0):
                    allList[key] = 1
                    totalAware = totalAware+1
                    ignorantNodeList.remove(key)
                    awareNodeList.append(key)
                    
                if(allList[key]==1):
                    decisionFromAware(key)
                    
                if(allList[key]==2):
                    decisionFromPI(key)
                    
                elif(allList[key]==4):
                    decisionFromNI(key)
            
            number_of_for = number_of_for + 1
    number_of_rounds = number_of_rounds + 1
    print(number_of_rounds)
        
    end = time.time()
    print(end - start)
            






