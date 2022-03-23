def verifySeq(PositionsSeq, ActualSeq, seqType):
    for i in PositionsSeq:
        if(i == ActualSeq):
            return seqType
    return "Neither"

import pickle
import random

mod1_filename_input = "col_ac"
mod2_filename_output = "col_ac"

file = open("./assets/mod1/"+mod1_filename_input+".mod1", "rb")

data = pickle.load(file)

flag = True
combinations = []
intronComb = []
exonComb = []
auxGT = 0
auxAG = 0
auxExternComb = []

contador = 0
for i in data:
    contador += 1
    auxExternComb = []
    auxGT = i[0].find("GT")
    while(auxGT != -1):
        auxAG = i[0].find("AG",auxGT+2)
        while(auxAG != -1):
            actualSeq = i[0][auxGT:auxAG+2]
            actualPositionSeq = [auxGT,auxAG+1]
            auxExternComb.append([actualSeq,actualPositionSeq,verifySeq(i[3],actualPositionSeq,"Intron")])
            auxAG = i[0].find("AG",auxAG+1)

        auxGT = i[0].find("GT",auxGT+1)

    intronComb.append(auxExternComb)

contador = 0
for i in data:
    contador += 1
    auxExternComb = []    
    auxAG = 0
    flag = True
    while(flag):
        auxGT = i[0].find("GT",auxAG+2)
        while(auxGT != -1):
            actualSeq = i[0][auxAG:auxGT]
            actualPositionSeq = [auxAG,auxGT-1]
            auxExternComb.append([actualSeq,actualPositionSeq,verifySeq(i[1],actualPositionSeq,"Exon")])
            auxGT = i[0].find("GT",auxGT+1)
        actualSeq = i[0][auxAG:]
        actualPositionSeq = [auxAG,len(i[0])-1]
        auxExternComb.append([actualSeq,actualPositionSeq,verifySeq(i[1],actualPositionSeq,"Exon")])
        auxAG = i[0].find("AG",auxAG)
        if(auxAG == -1):
            flag = False
        else:
            auxAG += 2
    exonComb.append(auxExternComb)

samples = []

labels = []

aux = []

exonsCount = 0

intronsCount = 0

i=0
while(i < len(exonComb)):
    for seq in exonComb[i]:
        if(seq[-1] != "Neither"):
            samples.append(seq[0])
            labels.append(seq[-1])
            exonsCount += 1
        else:
            aux.append([seq[0]])

    for seq in intronComb[i]:
        if(seq[-1] != "Neither"):
            samples.append(seq[0])
            labels.append(seq[-1])
            intronsCount += 1
        else:
            aux.append(seq[0])
    i+=1

average = (exonsCount + intronsCount)/2

for i in range(0,int(average)):
    randomNumber = random.randint(0,len(aux)-1)
    samples.append(aux[randomNumber][0])
    labels.append("Neither")
    aux.pop(randomNumber)

file = open("./assets/mod2/"+mod2_filename_output+".mod2","wb")
pickle.dump({'samples':samples, 'labels':labels},file)