to_list_dict = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'T':[0,0,0,1]}

from tensorflow import keras
import pickle
import numpy as np
from PIL import Image as im

def convert_to_image(array):
  image = []
  for char in array:
    image.append(to_list_dict[char])
  
  image = np.array(image, np.uint8)

  image = im.fromarray(image)
  
  resized = image.resize((4, 63))

  return np.array(resized)

def predict_sequence(seq):
  intron_comb = []
  gt_pos = 0
  ag_pos = 0

  intron_comb = []
  gt_pos = seq.find("GT")
  while(gt_pos != -1):
    ag_pos = seq.find("AG", gt_pos+2)
    while(ag_pos != -1):
      current_seq = seq[gt_pos:ag_pos+2]

      image_to_predict = convert_to_image(current_seq)

      prediction = np.argmax(model.predict(np.array([image_to_predict])))
      if prediction == 0:
        intron_comb.append(current_seq)

      ag_pos = seq.find("AG", ag_pos+1)

    gt_pos = seq.find("GT", gt_pos+1)

  for intron in intron_comb:
    seq = seq.replace(intron, "")

  return seq
# ================================================================================================

# Input & output filenames
model_filename_input = "col_ac"
mod1_filename_input = "col_ac"

# Load the model to be tested
model = keras.models.load_model('./assets/models/'+model_filename_input)

# Load the data from module 1
file = open("./assets/mod1/"+mod1_filename_input+".mod1", "rb")
data = pickle.load(file)

total = 0
hits = 0

for sequence in data[0:1000]:
  answer = predict_sequence(sequence[0])
  total += 1
  aux = ""
  for exon in sequence[2]:
    aux += exon[0]

  if(aux == answer):
    hits += 1
  
  if (total % 100 == 0):
    print("Hits:"+str(hits),"\nTotal:"+str(total))
    print("Result:"+str((hits/total)*100))    


print("Hits:"+str(hits),"\nTotal:"+str(total))
print("Result:"+str((hits/total)*100))