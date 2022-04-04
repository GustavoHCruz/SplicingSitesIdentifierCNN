import tensorflow as tf
from tensorflow import keras
from keras import datasets, layers, models
import pickle
import numpy as np

mod3_filename_input = "col_ac"
model_filename_output = "col_ac"

file = open("./assets/mod3/"+mod3_filename_input+".mod3", "rb")
data = pickle.load(file)

all_samples = data['samples']

all_labels = data['labels']

avg = 0
for sample in all_samples:
  avg += len(sample)
avg = avg/len(all_samples)

input_shape = (int(avg), 4, 1)
activation = 'relu'

model = models.Sequential()
model.add(layers.Conv2D(filters=58, kernel_size=(2, 2), activation=activation, input_shape=input_shape, padding='same'))
model.add(layers.AvgPool2D(pool_size=(2, 2), padding='same'))
model.add(layers.Conv2D(filters=116, kernel_size=(2, 2), activation=activation, padding='same'))
model.add(layers.AvgPool2D(pool_size=(2, 2), padding='same'))
model.add(layers.Conv2D(filters=116, kernel_size=(2, 2), activation=activation, padding='same'))
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(3))

# model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Create Samples Test and Train Set

all_samples = np.array(all_samples, dtype=object)

for i in range(0, len(all_samples)):
  if (len(all_samples[i]) == 0):
    all_samples[i] = [[0,0,0,0]]
  
  image = tf.image.convert_image_dtype(all_samples[i], 'float32')
  image = image[..., tf.newaxis]

  image = tf.image.resize(image, (58, 4))

  all_samples[i] = image

all_samples = np.array([np.asarray(sample).astype('float32') for sample in all_samples])

for i in range(0, len(all_labels)):
  if all_labels[i] == 'Exon':
    all_labels[i] = 0
  elif all_labels[i] == 'Intron':
    all_labels[i] = 1
  else:
    all_labels[i] = 2

all_labels = np.array(all_labels, dtype='float32')

# =================================

# trained_model = model.fit(all_samples, all_labels, epochs=10,
#                    validation_data=(samples, labels))

trained_model = model.fit(all_samples, all_labels, epochs=10)

# Trained Model Save

pickle.dump(trained_model, open("./assets/models/"+model_filename_output+".sav", "wb"))
