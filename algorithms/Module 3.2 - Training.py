import pickle

import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Conv2D, Dense, Flatten, MaxPool2D
from keras.metrics import Accuracy, Precision, Recall
from keras.models import Sequential
from tensorflow import keras

mod3_filename_input = "col_ac"
model_filename_output = "col_ac"

file = open("./assets/mod3/"+mod3_filename_input+".mod3", "rb")
data = pickle.load(file)

train_samples = data['train_samples']
train_labels = data['train_labels']
test_samples = data['test_samples']
test_labels = data['test_labels']

avg = 0
for sample in train_samples:
    avg += sample.size[1]
avg /= len(train_samples)

width = int(avg)
height = 4
channels = 1
input_shape = (width, height, channels)

train_samples_resized = []
for i in range(0, len(train_samples)):
  resized_sample = train_samples[i].resize((height, width))
  train_samples_resized.append(np.array(resized_sample))

test_samples_resized = []
for i in range(0, len(test_samples)):
  resized_sample = test_samples[i].resize((height, width))
  test_samples_resized.append(np.array(resized_sample))

train_samples_resized = np.array(train_samples_resized, dtype='float32')
train_labels = np.array(train_labels, dtype='float32')
test_samples_resized = np.array(test_samples_resized, dtype='float32')
test_labels = np.array(test_labels, dtype='float32')

model = Sequential()
model.add(Conv2D(filters=width, kernel_size=(2, 2), activation='relu', input_shape=input_shape))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(2, activation='softmax'))

# model.summary()

model.compile(optimizer='adam', loss=keras.losses.CategoricalCrossentropy(), metrics=[Accuracy(), Precision(), Recall()])

history = model.fit(train_samples_resized, keras.utils.to_categorical(train_labels), epochs=1000)

# Saving Training History

model.save('assets/models/'+model_filename_output)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.2, 1])
plt.legend(loc='lower right')
plt.show()

test_loss = model.evaluate(test_samples_resized,  keras.utils.to_categorical(test_labels), verbose=2)