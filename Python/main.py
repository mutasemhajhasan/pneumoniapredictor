import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import os

# Constants
MODEL_PATH = 'pneumonia_model.h5'
BASE_DIR = 'chest_xray'
TRAIN_DIR = os.path.join(BASE_DIR, 'train')
VAL_DIR = os.path.join(BASE_DIR, 'val')
TEST_DIR = os.path.join(BASE_DIR, 'test')
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def create_data_generators():
    """Create and configure data generators"""
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    test_val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    val_generator = test_val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    test_generator = test_val_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )

    return train_generator, val_generator, test_generator

def build_model():
    """Build and compile the DenseNet121 model"""
    base_model = DenseNet121(
        weights='imagenet',
        include_top=False,
        input_shape=(*IMG_SIZE, 3)
    )
    base_model.trainable = False

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )

    return model

def train_and_save_model():
    """Train the model and save to file"""
    train_gen, val_gen, _ = create_data_generators()
    model = build_model()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss'),
        tf.keras.callbacks.ModelCheckpoint(MODEL_PATH, save_best_only=True)
    ]

    history = model.fit(
        train_gen,
        steps_per_epoch=len(train_gen),
        epochs=5,
        validation_data=val_gen,
        validation_steps=len(val_gen),
        callbacks=callbacks
    )

    return history

def load_saved_model():
    """Load the pre-trained model"""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    return load_model(MODEL_PATH)

def evaluate_model(model):
    """Evaluate model on test set"""
    _, _, test_gen = create_data_generators()
    test_loss, test_acc, test_auc = model.evaluate(test_gen)
    print(f"\nTest Accuracy: {test_acc*100:.2f}%")
    print(f"Test AUC: {test_auc:.3f}")

def predict_image(model, image_path):
    """Make prediction on a single image"""
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=IMG_SIZE)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    
    prediction = model.predict(img_array)
    result = {
        'prediction': 'Pneumonia' if prediction[0][0] > 0.5 else 'Normal',
        'confidence': float(prediction[0][0] if prediction[0][0] > 0.5 else 1 - prediction[0][0]),
        'probability': float(prediction[0][0])
    }
    
    plt.imshow(img)
    plt.title(f"{result['prediction']} ({result['confidence']*100:.2f}%)")
    plt.axis('off')
    plt.show()
    
    return result

def main():
    # Check if model exists
    if os.path.exists(MODEL_PATH):
        print("Loading pre-trained model...")
        model = load_saved_model()
    else:
        print("Training new model (this may take a while)...")
        train_and_save_model()
        model = load_saved_model()
    
    # Evaluate model
    evaluate_model(model)
    
    # Example prediction
    sample_image = os.path.join(TEST_DIR, 'PNEUMONIA/person1_virus_11.jpeg')
    print("\nMaking prediction on sample image...")
    prediction = predict_image(model, sample_image)
    print(f"Prediction: {prediction['prediction']}")
    print(f"Confidence: {prediction['confidence']*100:.2f}%")
    print(f"Raw probability: {prediction['probability']:.4f}")

if __name__ == "__main__":
    main()
