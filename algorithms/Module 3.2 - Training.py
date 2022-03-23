import tensorflow as tf
from tensorflow import keras
from keras import datasets, layers, models
import pickle

mod3_filename_input = "col_ac"
model_filename_output = "col_ac"

file = open("./assets/mod3/"+mod3_filename_input+".mod3", "rb")
data = pickle.load(file)

samples = data['samples']

labels = data['labels']

input_shape = (None, None, 1)
activation = 'relu'

model = models.Sequential()
model.add(layers.Conv2D(filters=32, kernel_size=(2, 2), activation=activation, input_shape=input_shape))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(filters=64, kernel_size=(2, 2), activation=activation))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(filters=64, kernel_size=(2, 2), activation=activation))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

trained_model = model.fit(samples, labels, epochs=10,
                    validation_data=(samples, labels))

# Trained Model Save

pickle.dump(trained_model, open("./models/"+model_filename_output+".sav", "wb"))

file = open("./assets/mod3/"+mod3_filename_output+".mod3","wb")
pickle.dump([samples,labels],file)
