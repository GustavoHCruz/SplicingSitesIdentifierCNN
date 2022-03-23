import pickle   # Used for file operations

import sklearn_crfsuite # CRF model library
# ======================================================

# ================================================================================================
def predictResult(seq):
    intronComb = []
    auxGT = 0
    auxAG = 0

    intronComb = []
    auxGT = seq.find("GT")
    while(auxGT != -1):
        auxAG = seq.find("AG",auxGT+2)
        while(auxAG != -1):
            actualSeq = seq[auxGT:auxAG+2]
            if(["Intron"] == clf.predict_single([{"sequence":actualSeq}])):
                intronComb.append([actualSeq])

            auxAG = seq.find("AG",auxAG+1)

        auxGT = seq.find("GT",auxGT+1)

    for intron in intronComb:
        seq = seq.replace(intron[0],"")

    return seq
# ================================================================================================

# Input & output filenames (you can edit)
model_filename_input = "model_filename_input"
mod1_filename_input = "mod1_filename_input"

# Load the model to be tested
file = open("./results/"+model_filename_input+".sav", "rb")
clf = pickle.load(file)

# Load the data from module 1
file = open("./assets/mod1/"+mod1_filename_input+".mod1", "rb")
data = pickle.load(file)

total = 0
hits = 0

for seq in data:
    answer = predictResult(seq[0])
    total += 1
    aux = ""
    for exon in seq[2]:
        aux += exon[0]

    if(aux == answer):
        hits += 1

print("Hits:"+str(hits),"\nTotal:"+str(total))
print("Result:"+str((hits/total)*100))