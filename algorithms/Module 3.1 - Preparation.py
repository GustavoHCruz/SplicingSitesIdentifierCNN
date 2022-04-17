to_list_dict = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'T':[0,0,0,1]}
separation_rate = 0.2

import pickle
import numpy as np
import random as rd
from PIL import Image as im

mod2_filename_input = "col_ac"
mod3_filename_output = "col_ac"

file = open("./assets/mod2/"+mod2_filename_input+".mod2", "rb")
data = pickle.load(file)

all_samples = data['samples']

all_labels = data['labels']

# Creating a list of all the samples already in the format of a list of images
train_samples = []
for sample in all_samples:
    aux = []
    for char in sample:
      aux.append(to_list_dict[char])
    
    aux = np.array(aux, np.uint8)

    aux = im.fromarray(aux)

    train_samples.append(aux)

# Creating a list of all the labels already in the format of a list of labels
train_labels = []
for i in range(0, len(all_labels)):
  if all_labels[i] == 'Intron':
    train_labels.append(0)
  else:
    train_labels.append(1)

train_labels = np.array(train_labels, dtype='float32')

# Unifing the samples and labels into a single list

samples_labels_set = []

for i in range(0, len(train_samples)):
  samples_labels_set.append([train_samples[i], train_labels[i]])

# Shuffling the set

rd.shuffle(samples_labels_set)

# Spreading the samples and labels into a training and validation set

introns = []
not_introns = []

for sample_label in samples_labels_set:
  if sample_label[1] == 0:
    introns.append(sample_label)
  else:
    not_introns.append(sample_label)

# Introns sets

introns_test = introns[0:int(len(introns)*separation_rate)]

introns = introns[int(len(introns)*separation_rate):]

# Not Introns sets

not_introns = not_introns[0:int(len(not_introns)/2)]

not_introns_test = not_introns[0:int(len(not_introns)*separation_rate)]

not_introns = not_introns[int(len(not_introns)*separation_rate):]

# Creating the training and testing sets

train_set = introns + not_introns
test_set = introns_test + not_introns_test

rd.shuffle(train_set)
rd.shuffle(test_set)

train_samples = []
train_labels = []
test_samples = []
test_labels = []

for i in range (0, len(train_set)):
  train_samples.append(train_set[i][0])
  train_labels.append(train_set[i][1])

for i in range (0, len(test_set)):
  test_samples.append(test_set[i][0])
  test_labels.append(test_set[i][1])

file = open("./assets/mod3/"+mod3_filename_output+".mod3","wb")
pickle.dump({'train_samples':train_samples, 'train_labels':train_labels, 'test_samples':test_samples, 'test_labels':test_labels}, file)