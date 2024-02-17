import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import os
from PIL import Image
import numpy as np

# Load and preprocess your data
image_dir = "./DataCollector/images/"
label_dir = "./DataCollector/labels/"

# Function to load and preprocess an individual image
def load_and_preprocess_image(file_path):
    img = Image.open(file_path)
    img = img.resize((32, 32))  # Resize images to a consistent size
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

# Split data into training and testing sets
train_filenames, test_filenames, train_labels, test_labels = train_test_split(
    all_filenames, all_labels, test_size=0.2, random_state=42
)

# Load and preprocess images
train_images = np.array([load_and_preprocess_image(path) for path in train_filenames])
test_images = np.array([load_and_preprocess_image(path) for path in test_filenames])

# Define the model
model = keras.models.Sequential()
model.add(layers.Conv2D(32, (3, 3), strides=(1, 1), padding="valid", activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, 3, activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(num_unique_labels, activation='sigmoid'))  # Multi-label classification: Output layer with sigmoid activation activation='sigmoid')

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Convert labels to a multi-hot encoded format
train_labels_multi_hot = np.zeros((len(train_labels), num_unique_labels))
test_labels_multi_hot = np.zeros((len(test_labels), num_unique_labels))

dirs = ["Up", "Down", "Neutral"]

for i, labels in enumerate(train_labels):

    for j, label in enumerate(labels):

        if label.startswith('DIRECTION:'):
            dir_vec = np.zeros(len(dirs)) 
            direction_value = label.split(':')[1].strip().upper()

            if direction_value in dirs:
                label_idx = dirs.index(direction_value)
                # Set the corresponding entry to 1 for the specific direction value
                dir_vec[label_idx] = 1
                
                train_labels_multi_hot[i, j] = dir_vec
        
        else:
            train_labels_multi_hot[i, j] = 0


for i, labels in enumerate(test_labels):

    for j, label in enumerate(labels):
        if label.startswith('DIRECTION:'):
            dir_vec = np.zeros(len(dirs)) 
            direction_value = label.split(':')[1].strip().upper()

            if direction_value in dirs:
                label_idx = dirs.index(direction_value)
                # Set the corresponding entry to 1 for the specific direction value
                dir_vec[label_idx] = 1
                test_labels_multi_hot[i, j] = dir_vec
        else:
            a = 1
            test_labels_multi_hot[i, j] = 0

# Train the model iteratively
# batch_size = 32
# epochs_per_iteration = 40
# total_iterations = 5  # Set the total number of iterations

# for iteration in range(total_iterations):
#     print(f"Iteration {iteration + 1}/{total_iterations}")

#     # Train the model
#     model.fit(train_images, train_labels_multi_hot, epochs=epochs_per_iteration, batch_size=batch_size, verbose=2)

#     # Evaluate the model on the test set
#     evaluation_result = model.evaluate(test_images, test_labels_multi_hot, batch_size=batch_size, verbose=2)

#     # Print the evaluation result
#     print("Evaluation result:", evaluation_result)
# Train the model
batch_size = 32
epochs = 40

model.fit(train_images, train_labels_multi_hot, epochs=epochs, batch_size=batch_size, verbose=2)

# Evaluate the model
model.evaluate(test_images, test_labels_multi_hot, batch_size=batch_size, verbose=2)
