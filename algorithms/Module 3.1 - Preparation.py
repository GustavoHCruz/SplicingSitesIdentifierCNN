toListDict = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'T':[0,0,0,1]}

def sequence_to_list(sequence):
  return 

import pickle

mod2_filename_input = "col_ac"
mod3_filename_output = "col_ac"
model_filename_output = "col_ac"

file = open("./assets/mod2/"+mod2_filename_input+".mod2", "rb")
data = pickle.load(file)

samples = data['samples']

labels = data['labels']

image_samples = []
for sample in samples:
  aux = []
  for char in sample:
    aux.append(toListDict[char])
  image_samples.append(aux)

file = open("./assets/mod3/"+mod3_filename_output+".mod3","wb")
pickle.dump({'samples':image_samples, 'labels':labels},file)