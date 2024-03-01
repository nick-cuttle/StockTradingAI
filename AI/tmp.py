#from cnn import create_cnn_model, load_and_preprocess_image
model_weights_path = "./weights.h5"
import pygame
import sys
import random
import os
from PIL import Image
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
exit()
dirs = ["UP", "DOWN", "NEUTRAL"]
num_unique_labels = 1
def create_cnn_model():
    num_out = len(dirs) + (num_unique_labels - 1)
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
    return model

def load_and_preprocess_image(file_path):
    img = Image.open(file_path)
    img = img.convert("RGB")
    img = img.resize((64, 64))  # Resize images to a consistent size
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    return img_array

model = create_cnn_model()
model.load_weights(model_weights_path)
batch_size = 32

#test_img_path = "../DataCollector/test_imgs/" + random.choice(os.listdir("../DataCollector/test_imgs"))
test_img_path = "../DataCollector/test_imgs/DOWN50001.png"
print(test_img_path)

test_images = np.array([load_and_preprocess_image(test_img_path)])

# Make predictions on the test set
predictions = model.predict(test_images, batch_size=batch_size, verbose=2)
#Apply a threshold to convert probabilities to binary predictions
threshold = 0.5
binary_predictions = (predictions > threshold).astype(int)
print(binary_predictions)
sys.exit()


# Initialize pygame
pygame.init()

# Set the dimensions of the window
width, height = 800, 600

# Create a window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Image Example")

# Load an image
image = pygame.image.load("path/to/your/image.png")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the image onto the screen
    screen.blit(image, (0, 0))

    # Update the display
    pygame.display.flip()


