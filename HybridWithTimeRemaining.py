import facebook
import time
import numpy
import random

start = time.time()

#ignorant aware PI NI removed
# load the network
facebook.load_network()

number_of_for = 0
number_of_rounds = 0
ctr=500
thresholdValue=30  #interest threshold state degisimi icin
timeToRemove=10  #bilgi noda geldiginden itibaren ne zaman removed'a gecis yapacak
compareThreshold = 30 #bilgi noda geldiğinde nodun yeni mesaja olan tavrı -> >x ise interest= x + eski interest; <x ise interest= eski interest -x

interest = dict(facebook.network.nodes())
interest = dict.fromkeys(interest,0)

#her bir nod mesajı hangi yönde yayiyor 1-pozitif 2-negatif 0-yayılım yok
directionOfMsg = dict(facebook.network.nodes())
directionOfMsg = dict.fromkeys(directionOfMsg,0)

#her bir noda rumor kac kere gelmis
rumorCount = dict(facebook.network.nodes())
rumorCount = dict.fromkeys(rumorCount,0)

#start end times for countdown
startcd = dict(facebook.network.nodes())
startcd = dict.fromkeys(startcd,0)
endcd = dict(facebook.network.nodes())
endcd = dict.fromkeys(endcd,0)

#nodeların stateleri value olarak tutuluyor 0-ignorant 1-aware 2-PI 3-NI 4-removed
allList = dict(facebook.network.nodes())
allList = dict.fromkeys(allList,0)

ignorantNodeList = list(facebook.network.nodes())
awareNodeList = []
totalAwareNumber=0
piNodeList = []
totalPINumber=0
niNodeList = []
totalNINumber=0
removedNodeList = []
totalRemovedNumber=0

#random choosing of first node
randomNode = random.choice(list(allList.keys()))
totalAwareNumber = totalAwareNumber + 1
totalPINumber = totalPINumber + 1
ignorantNodeList.remove(randomNode)
piNodeList.append(randomNode)
allList[randomNode] = 2
directionOfMsg[randomNode] = 1
interest[randomNode]=20

#creating a message
msg= numpy.tile(0,len(facebook.network.nodes[4]['features']))
msgfeat = random.randint(0, len(facebook.network.nodes[4]['features']))
msg[msgfeat] = 2

def decisionFromAware(nodeId):
    
    if((interest[nodeId] >= thresholdValue) & (rumorCount[nodeId]>5)):
        allList[nodeId] = 2 #positive Infected
        global totalPINumber
        totalPINumber = totalPINumber + 1
        directionOfMsg[nodeId] == 1
        awareNodeList.remove(nodeId)
        piNodeList.append(nodeId)
        
    elif((interest[nodeId] < thresholdValue) and (interest[nodeId] > -thresholdValue)):
        allList[nodeId] = 1 #stay in aware state
        rumorCount[nodeId] = rumorCount[nodeId] + 1
    
    elif((interest[nodeId] <= -thresholdValue) & (rumorCount[nodeId]>5)):
        allList[nodeId] = 3 #NegativeInfected
        global totalNINumber
        totalNINumber = totalNINumber + 1
        directionOfMsg[nodeId] == 2
        awareNodeList.remove(nodeId)
        niNodeList.append(nodeId)
       
        
def updateInterest(nodeId, totalInterest):
    
    currentInterest = interest[nodeId] + totalInterest
    interest[nodeId] = currentInterest
    return currentInterest


def decisionFromPI(nodeId):
    
    if((interest[nodeId]>=thresholdValue)):
        allList[nodeId] = 2 #positive Infected
        directionOfMsg[nodeId] == 2
        
    elif((interest[nodeId]<thresholdValue) and (interest[nodeId] > -thresholdValue)):
        allList[nodeId] = 4 #removed
        global totalRemovedNumber
        totalRemovedNumber = totalRemovedNumber + 1
        directionOfMsg[nodeId] == 0
        piNodeList.remove(nodeId)
        removedNodeList.append(nodeId)
    
    elif((interest[nodeId]<=-thresholdValue)):
        allList[nodeId] = 4 #NegativeInfected
        global totalNINumber
        totalNINumber = totalNINumber + 1
        directionOfMsg[nodeId] == 2
        piNodeList.remove(nodeId)
        niNodeList.append(nodeId)
       
   
def decisionFromNI(nodeId):
    
    if((interest[nodeId]>=thresholdValue)):
        allList[nodeId] = 2 #positive Infected
        global totalPINumber
        totalPINumber = totalPINumber + 1
        directionOfMsg[nodeId] == 1
        niNodeList.remove(nodeId)
        piNodeList.append(nodeId)
        
    elif((interest[nodeId]<thresholdValue) and (interest[nodeId] > -thresholdValue)):
        allList[nodeId] = 4 #removed
        global totalRemovedNumber
        totalRemovedNumber = totalRemovedNumber + 1
        directionOfMsg[nodeId] == 0
        niNodeList.remove(nodeId)
        removedNodeList.append(nodeId)
    
    elif((interest[nodeId]<=-thresholdValue)):
        allList[nodeId] = 3 #NegativeInfected
        directionOfMsg[nodeId] == 2
       
def timeLeft(nodeId):
    if(endcd[nodeId] - startcd[nodeId] >= timeToRemove): #bilgi noda ilk kez geldiğinden bu yana geçen zaman 10 saniye ise
        allList[nodeId] = 4 #removed
        directionOfMsg[nodeId] == 0
        removedNodeList.append(nodeId)
        if nodeId in awareNodeList:
            awareNodeList.remove(nodeId)
        if nodeId in piNodeList:
            piNodeList.remove(nodeId)
        if nodeId in niNodeList:
            niNodeList.remove(nodeId)
            
#while (ctr > number_of_rounds):
while (totalRemovedNumber+totalAwareNumber<4039):
    for key in allList.keys():
        neighborlist = [item[1] for item in list(facebook.network.edges(key))]
        neighborNode=random.choice(neighborlist)
        if (((0 < allList[key] < 4) or (0 < allList[neighborNode] < 4)) and not(allList[neighborNode]==allList[key]==1)):
            
            #calculate for neighbor
            rumorCount[neighborNode] = rumorCount[neighborNode] + 1
            neighborInterest = facebook.totalInterest(facebook.network.nodes[key]['features'], facebook.network.nodes[neighborNode]['features'], key, msg)
            
            if(directionOfMsg[key] == 1):
                if(neighborInterest> compareThreshold):    #aradaki total relation
                    interest[neighborNode] = interest[neighborNode] + neighborInterest
                else:
                    interest[neighborNode] = interest[neighborNode] - neighborInterest
                    
                if(allList[neighborNode] == 0): #mesaj ilk kez geldi ignorant->aware
                    totalAwareNumber = totalAwareNumber + 1
                    startcd[neighborNode]= time.time()
                    allList[neighborNode] = 1
                    ignorantNodeList.remove(neighborNode)
                    awareNodeList.append(neighborNode)
                
                elif(allList[neighborNode]==1):
                    decisionFromAware(neighborNode)
                   
                elif(allList[neighborNode]==2):
                    decisionFromPI(neighborNode)
                    
                elif(allList[neighborNode]==3):
                    decisionFromNI(neighborNode)
                    
            if(directionOfMsg[key] == 2):
                if(neighborInterest>compareThreshold):
                    interest[neighborNode] = interest[neighborNode] - neighborInterest
                    
                else:
                    interest[neighborNode] = interest[neighborNode] + neighborInterest
           
                if(allList[neighborNode] == 0): #mesaj ilk kez geldi ignorant->aware
                    totalAwareNumber = totalAwareNumber + 1
                    startcd[neighborNode]= time.time()
                    allList[neighborNode] = 1
                    ignorantNodeList.remove(neighborNode)
                    awareNodeList.append(neighborNode)
                
                elif(allList[neighborNode]==1):
                    decisionFromAware(neighborNode)
                   
                elif(allList[neighborNode]==2):
                    decisionFromPI(neighborNode)
                    
                elif(allList[neighborNode]==3):
                    decisionFromNI(neighborNode)
                
            #calculate for source=key
            sourceInterest = facebook.totalInterest(facebook.network.nodes[neighborNode]['features'], facebook.network.nodes[key]['features'], neighborNode, msg)
    
            rumorCount[key] = rumorCount[key] + 1
        
            if(directionOfMsg[neighborNode] == 1):
                if(sourceInterest>compareThreshold):
                    interest[key] = interest[key] + sourceInterest
                else:
                    interest[key] = interest[key] - sourceInterest
                    
                if(allList[key]==0): #mesaj ilk kez geldi ignorant->aware
                    totalAwareNumber = totalAwareNumber + 1
                    startcd[key]= time.time()
                    allList[key] = 1
                    ignorantNodeList.remove(key)
                    awareNodeList.append(key)
                    
                if(allList[key]==1):
                    decisionFromAware(key)
                    
                if(allList[key]==2):
                    decisionFromPI(key)
                    
                elif(allList[key]==3):
                    decisionFromNI(key)                
            
            
            if(directionOfMsg[neighborNode] == 2):
                if(sourceInterest>compareThreshold):
                    interest[key] = interest[key] - sourceInterest
                else:
                    interest[key] = interest[key] + sourceInterest
           
                if(allList[key]==0): #mesaj ilk kez geldi ignorant->aware
                    totalAwareNumber = totalAwareNumber + 1
                    startcd[key]= time.time()
                    allList[key] = 1
                    ignorantNodeList.remove(key)
                    awareNodeList.append(key)
                    
                if(allList[key]==1):
                    decisionFromAware(key)
                    
                if(allList[key]==2):
                    decisionFromPI(key)
                    
                elif(allList[key]==3):
                    decisionFromNI(key)
             
            number_of_for = number_of_for + 1
        
        for i in startcd:
            if ((startcd[i] > 0) and not( i in removedNodeList)):
                endcd[i] = time.time()  
                if timeLeft(i):
                    totalRemovedNumber = totalRemovedNumber + 1
        
    number_of_rounds = number_of_rounds + 1
            
        
    end = time.time()
    totalTime= end - start
    print(totalTime)
            






