from tensorflow import keras
from keras.layers import Conv2D, MaxPool2D
from keras.layers.core import Dense, Flatten
from keras.models import Sequential
import pickle
import numpy as np

mod3_filename_input = "col_ac"
model_filename_output = "col_ac"

file = open("./assets/mod3/"+mod3_filename_input+".mod3", "rb")
data = pickle.load(file)

width = 58
height = 4
channels = 1
input_shape = (width, height, channels)

train_samples = data['train_samples']
train_labels = data['train_labels']
test_samples = data['test_samples']
test_labels = data['test_labels']

train_samples_resized = []
for i in range(0, len(train_samples)):
  resized_sample = train_samples[i].resize((height, width))
  train_samples_resized.append(np.array(resized_sample))

test_samples_resized = []
for i in range(0, len(test_samples)):
  resized_sample = test_samples[i].resize((height, width))
  test_samples_resized.append(np.array(resized_sample))

train_samples = np.array(train_samples_resized, dtype='float32')
train_labels = np.array(train_labels, dtype='float32')
test_samples = np.array(test_samples_resized, dtype='float32')
test_labels = np.array(test_labels, dtype='float32')

model = Sequential()
model.add(Conv2D(filters=width, kernel_size=(2, 2), activation='relu', input_shape=input_shape))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(2, activation='softmax'))

# model.summary()

model.compile(optimizer='adam', loss=keras.losses.CategoricalCrossentropy(), metrics=['accuracy'])

history = model.fit(train_samples, keras.utils.to_categorical(train_labels), epochs=10, validation_data=(test_samples, keras.utils.to_categorical(test_labels)))

# Saving Training History

model.save('assets/models/'+model_filename_output)