def verify_seq(positions_seq, current_seq, seq_type):
	for i in positions_seq:
		if(i == current_seq):
			return seq_type
	return "Neither"

import pickle
import random as rd

mod1_filename_input = "col_ac"
mod2_filename_output = "col_ac"

file = open("./assets/mod1/"+mod1_filename_input+".mod1", "rb")

data = pickle.load(file)

flag = True
combinations = []
intron_comb = []
exon_comb = []
gt_pos = 0
ag_pos = 0
aux_extern_comb = []

counter = 0
for i in data:
	counter += 1
	aux_extern_comb = []
	gt_pos = i[0].find("GT")
	while gt_pos != -1:
		ag_pos = i[0].find("AG", gt_pos+2)
		while ag_pos != -1:
			current_seq = i[0][gt_pos:ag_pos+2]
			current_seq_position = [gt_pos, ag_pos+1]
			aux_extern_comb.append([current_seq,current_seq_position, verify_seq(i[3], current_seq_position, "Intron")])
			ag_pos = i[0].find("AG", ag_pos+1)

		gt_pos = i[0].find("GT", gt_pos+1)

	intron_comb.append(aux_extern_comb)

counter = 0
for i in data:
	counter += 1
	aux_extern_comb = []    
	ag_pos = 0
	flag = True
	while flag:
		gt_pos = i[0].find("GT", ag_pos+2)
		while gt_pos != -1:
			current_seq = i[0][ag_pos:gt_pos]
			current_seq_position = [ag_pos, gt_pos-1]
			aux_extern_comb.append([current_seq, current_seq_position, verify_seq(i[1], current_seq_position, "Exon")])
			gt_pos = i[0].find("GT", gt_pos+1)
		current_seq = i[0][ag_pos:]
		current_seq_position = [ag_pos, len(i[0])-1]
		aux_extern_comb.append([current_seq, current_seq_position, verify_seq(i[1], current_seq_position, "Exon")])
		ag_pos = i[0].find("AG", ag_pos)
		if ag_pos == -1:
			flag = False
		else:
			ag_pos += 2
	exon_comb.append(aux_extern_comb)

samples = []

labels = []

aux = []

exons_counter = 0

introns_counter = 0

for i in range(0, len(exon_comb)):
	for seq in exon_comb[i]:
		if(seq[-1] != "Neither"):
			samples.append(seq[0])
			labels.append(seq[-1])
			exons_counter += 1
		else:
			aux.append([seq[0]])

	for seq in intron_comb[i]:
		if(seq[-1] != "Neither"):
			samples.append(seq[0])
			labels.append(seq[-1])
			introns_counter += 1
		else:
			aux.append(seq[0])

average = int((exons_counter + introns_counter)/2)

for i in range(0, average):
    random_number = rd.randint(0, len(aux)-1)
    samples.append(aux[random_number][0])
    labels.append("Neither")
    aux.pop(random_number)

file = open("./assets/mod2/"+mod2_filename_output+".mod2","wb")
pickle.dump({'samples':samples, 'labels':labels},file)