def make_exons_list(seq):
  seq = str(seq)
  seq = seq.split("{")
  seq = seq[-1]
  for char in "}][><)(+- ":
    seq = seq.replace(char, "")
  seq = seq.split(",")
  for i in range(0, len(seq)):
    seq[i] = seq[i].split(":")
    seq[i][0] = int(seq[i][0])
    seq[i][1] = int(seq[i][1])
    seq[i][1] = seq[i][1] - 1
  
  return seq

def make_introns_list(exons_list, length):
  i = 0
  seq = []
  if exons_list[i][0] != 0:
    seq.append([0, exons_list[i][0]-1])
  while i < len(exons_list) - 1:
    seq.append([exons_list[i][1]+1, exons_list[i+1][0]-1])
    i += 1
  if exons_list[-1][1] != length - 1:
    seq.append([exons_list[-1][1]+1, length-1])

  return seq

from Bio import SeqIO
import pickle
import re

genbank_filename_input = "colletotrichum_actin"
mod1_filename_output = "col_ac"

genbank_archive = open("./assets/gb/"+genbank_filename_input+".gb","r")

data = []

for register in SeqIO.parse(genbank_archive, "genbank"):
  if register.features[-1].type == "CDS" and register.features[0].strand == 1:
    correct = False

    seq = str(register.seq)
    if len(seq) <= 300 and re.match(r'^[ACGT]+$', seq):
      correct = True

      exons_list = make_exons_list(register.features[-1].location)

      introns_list = make_introns_list(exons_list, len(seq))

      introns, exons = [], []

      for x in exons_list:
          exons.append([seq[(x[0]):(x[1])+1]])
      for x in introns_list:
          introns.append([seq[(x[0]):(x[1])+1]])
        
    if correct:
      data.append([seq, exons_list, exons, introns_list, introns])

file = open("./assets/mod1/"+mod1_filename_output+".mod1","wb")
pickle.dump(data, file)