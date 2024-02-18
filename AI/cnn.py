import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os
from PIL import Image
import numpy as np
import random
from tensorflow.keras.callbacks import ModelCheckpoint

# Load and preprocess your data
image_dir = "../DataCollector/images/"
label_dir = "../DataCollector/labels/"
model_weights_path = "./weights.h5"
dirs = ["UP", "DOWN", "NEUTRAL"]

# Function to load and preprocess an individual image
def load_and_preprocess_image(file_path):
    img = Image.open(file_path)
    img = img.resize((64, 64))  # Resize images to a consistent size
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    return img_array

def load_and_flip_image(file_path):
    img = Image.open(file_path)
    img = img.resize((64, 64))  # Resize images to a consistent size
    flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    return img_array

# Load image paths and labels
image_paths = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir)]
label_paths = [os.path.join(label_dir, filename) for filename in os.listdir(label_dir)]
label_mapping = {}  # Map image filenames to their labels

# Assuming labels are stored in a text file, one per line
for path in label_paths:
    label_file = open(path, "r")
    filename = label_file.name
    filename = filename.replace("/labels/", "/images/")
    filename = filename.replace(".txt", ".png")
    label_mapping[filename] = []
    for line in label_file:
        label = line.strip()
        label_mapping[filename].append(label)

num_unique_labels = 2

# Create lists for training and testing data
all_filenames = list(label_mapping.keys())
all_labels = list(label_mapping.values())

num_iter = 20
mean_accuracy = 0

for iter in range(num_iter):
    # Split data into training and testing sets
    train_filenames, test_filenames, train_labels, test_labels = train_test_split(
        all_filenames, all_labels, test_size=0.1, random_state=None
    )

    num_out = len(dirs) + (num_unique_labels - 1)
    # Load and preprocess images
    train_images = np.array([load_and_preprocess_image(path) for path in train_filenames])
    test_images = np.array([load_and_preprocess_image(path) for path in test_filenames])

    # # Define the model
    # model = keras.models.Sequential()
    # model.add(layers.Conv2D(32, (3, 3), strides=(1, 1), padding="valid", activation='relu', input_shape=(32, 32, 3)))
    # model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(32, 3, activation='relu'))
    # model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Flatten())
    # model.add(layers.Dense(64, activation='relu'))
    # model.add(layers.Dense(num_out, activation='sigmoid'))  # Multi-label classification: Output layer with sigmoid activation activation='sigmoid')
    # Define the model
    model = keras.models.Sequential()
    model.add(layers.Conv2D(64, (3, 3), strides=(1, 1), padding="valid", activation='relu', input_shape=(64, 64, 3)))  # Increase filters
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, 3, activation='relu'))  # Increase filters
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, 3, activation='relu'))  # Add another convolutional layer
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))  # Increase dense layer size
    model.add(layers.Dropout(0.5))  # Add dropout for regularization
    model.add(layers.Dense(num_out, activation='sigmoid'))  # Multi-label classification: Output layer with sigmoid activation


    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    #train_labels_multi_hot = np.zeros((len(train_labels), num_unique_labels))
    train_labels_multi_hot = np.zeros((len(train_labels), num_out))
    test_labels_multi_hot = np.zeros((len(test_labels), num_out))


    # multihot label format is the following:

    # [0, 0, 0]

    for i, labels in enumerate(train_labels):
        # [0, 0]
        row = [0] * num_out

        label_idx = None
        for j, label in enumerate(labels):
            if label.startswith('DIRECTION:'):
                #dir_vec = np.zeros(len(dirs)) 

                direction_value = label.split(':')[1].strip().upper()

                if direction_value in dirs:
                    label_idx = dirs.index(direction_value)
                    #get offset and store
                    row[j + label_idx] = 1
            
            else:
                tmp_i = j + len(dirs) - 1
                row[tmp_i] = 0
        train_labels_multi_hot[i] = row


    for i, labels in enumerate(test_labels):
        row = [0] * num_out
        for j, label in enumerate(labels):
            if label.startswith('DIRECTION:'):
                #dir_vec = np.zeros(len(dirs)) 
                direction_value = label.split(':')[1].strip().upper()

                if direction_value in dirs:
                    label_idx = dirs.index(direction_value)
                    row[j + label_idx] = 1
                    # Set the corresponding entry to 1 for the specific direction value
                    #dir_vec[label_idx] = 1
                    #row[j] = dir_vec
            else:
                tmp_i = j + len(dirs) - 1
                row[j] = 0
        
        test_labels_multi_hot[i] = row

    # Create a callback for model checkpointing
    model_checkpoint = ModelCheckpoint(model_weights_path, save_best_only=True, save_weights_only=True, monitor='val_accuracy', mode='max', verbose=1)
    batch_size = 32

    # Check if the saved weights file exists
    if os.path.exists(model_weights_path):
        # Load the previously learned weights
        model.load_weights(model_weights_path)
    else:
        # Train the model if no saved weights are found
        epochs = 20



        history = model.fit(train_images, train_labels_multi_hot, epochs=epochs, batch_size=batch_size, validation_data=(test_images, test_labels_multi_hot), callbacks=[model_checkpoint], verbose=2)
        # Save the learned weights
        model.save_weights(model_weights_path)


    # Evaluate the model
    print("ITER: " + str(iter))
    evaluation_result = model.evaluate(test_images, test_labels_multi_hot, batch_size=batch_size, verbose=2)
    accuracy_value = evaluation_result[1]
    mean_accuracy += accuracy_value
    # Print the evaluation result
    #print("Evaluation result:", evaluation_result)

    # Make predictions on the test set
    #predictions = model.predict(test_images, batch_size=batch_size, verbose=2)
    # Apply a threshold to convert probabilities to binary predictions
    #threshold = 0.5
    #binary_predictions = (predictions > threshold).astype(int)
# Print or store the binary predictions as needed
#print("Binary Predictions:", binary_predictions)
    
mean_accuracy = mean_accuracy/ num_iter

print("MEAN ACCURACY: ", mean_accuracy)
