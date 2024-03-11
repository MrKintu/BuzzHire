import os

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Flatten, Conv1D, MaxPooling1D
from tensorflow.keras import Sequential


# Function to preprocess data
def preprocess_data(raw_data):
    # Preprocess raw_data here
    # Example: Convert raw_data to numpy array and apply fuzzy logic
    preprocessed_data = np.random.rand(100, 100)  # Example preprocessed data
    return preprocessed_data


# Function to define the neural network model
def define_model():
    # Load previous model if available
    model_path = 'myers_briggs_model.h5'  # Path to save/load the model

    if os.path.exists(model_path):
        print("Loading previous model...")
        model = tf.keras.models.load_model(model_path)
    else:
        print("Creating new model...")
        # Example raw_data (Replace with your actual data)
        raw_data = np.random.rand(100, 100)  # Example raw data

        # Preprocess data
        preprocessed_data = preprocess_data(raw_data)
        labels = ['I/E', 'S/I', 'T/F', 'J/P']

        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(preprocessed_data,
                                                          labels, test_size=0.2, random_state=42)

        # Define input shape and number of classes
        input_shape = (100, 1)  # Example input shape
        num_classes = 16  # Example number of classes

        # Define the model architecture
        model = Sequential([
            Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=input_shape),
            Dense(64, activation='relu'),
            MaxPooling1D(pool_size=2),
            Conv1D(filters=64, kernel_size=3, activation='relu'),
            Dense(32, activation='relu'),
            Flatten(),
            Dense(num_classes, activation='softmax')
        ])

        # Compile model
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train model
        model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

        # Save model
        model.save(model_path)
        print(model.summary())

    return model
