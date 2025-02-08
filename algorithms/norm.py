import pickle

import numpy as np
from PIL import Image
from tensorflow import keras

to_list_dict = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'T':[0,0,0,1]}

model_filename_input = "actin"
mod1_filename_input = "actin"

model = keras.models.load_model(f"./assets/models/{model_filename_input}.h5")

def convert_to_image(array):
  image = []
  for char in array:
    image.append(to_list_dict[char])
  
  image = np.array(image, np.uint8)

  image = Image.fromarray(image)
  
  resized = image.resize((4, 121))

  return np.array(resized)

def predict_sequence(seq):
  seq = seq.upper()

  intron_comb = []
  gt_pos = 0
  ag_pos = 0

  intron_comb = []
  gt_pos = seq.find("GT")
  while(gt_pos != -1):
    ag_pos = seq.find("AG", gt_pos+2)
    prediction = 1
    while(ag_pos != -1):
      current_seq = seq[gt_pos:ag_pos+2]

      image_to_predict = convert_to_image(current_seq)

      prediction = model.predict(np.array([image_to_predict]), verbose=0)
      prediction = round(prediction[0][0])

      if prediction == 0:
        intron_comb.append(current_seq)
        gt_pos = seq.find("GT", ag_pos+1)
        ag_pos = -1
      else:
        ag_pos = seq.find("AG", ag_pos+1)

    if prediction != 0:
      gt_pos = seq.find("GT", gt_pos+1)

  for intron in intron_comb:
    seq = seq.replace(intron, "")

  return seq

file = open("./assets/mod1/"+mod1_filename_input+".mod1", "rb")
processed_database = pickle.load(file)['test']

normalization_result = []
database_len = len(processed_database)

for sequence in processed_database:
  predicted_result = predict_sequence(sequence['complete_sequence'])
  comparation_result = sequence['response_sequence']

  hits = 0
  if predicted_result == comparation_result:
    hits += 1

  print(f"Progress: {hits}/{database_len}")
