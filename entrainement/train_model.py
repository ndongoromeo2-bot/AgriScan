import os
from tensorflow.keras.models import load_model
import tensorflow as tf

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models


# PARAMETRES
IMG = (224, 224)
BATCH = 32
EPOCHS = 15


# 1. PREPARATION DES IMAGES D'ENTRAINEMENT

train_gen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=(0.8, 1.2)
)


# 2. PREPARATION DES IMAGES DE VALIDATION

val_gen = ImageDataGenerator(
    rescale=1.0 / 255
)


# 3. CHARGEMENT DES DATASETS

train = train_gen.flow_from_directory(
    "dataset/train",
    target_size=IMG,
    batch_size=BATCH,
    class_mode="binary"
)

val = val_gen.flow_from_directory(
    "dataset/val",
    target_size=IMG,
    batch_size=BATCH,
    class_mode="binary"
)


# 4. VERIFICATION DES CLASSES

print("Classes :", train.class_indices)

assert train.class_indices == {
    "fertile": 0,
    "non_fertile": 1
}, "Ordre des classes incorrect"


# 5. CHARGEMENT DE MOBILENETV2

base = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base.trainable = False


# 6. CONSTRUCTION DU MODELE

model = models.Sequential([
    base,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(1, activation="sigmoid")
])


# 7. COMPILATION

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()


# 8. ARRET AUTOMATIQUE

arret = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True
)


# 9. ENTRAINEMENT

history = model.fit(
    train,
    validation_data=val,
    epochs=EPOCHS,
    callbacks=[arret]
)


# 10. SAUVEGARDE DU MODELE

model.save("../modele_fertilite_sol.h5")

print("Modèle sauvegardé : modele_fertilite_sol.h5")


# 11. GENERATION DES COURBES

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)

plt.plot(history.history["accuracy"], label="entraînement")
plt.plot(history.history["val_accuracy"], label="validation")

plt.title("Précision")
plt.legend()


plt.subplot(1, 2, 2)

plt.plot(history.history["loss"], label="entraînement")
plt.plot(history.history["val_loss"], label="validation")

plt.title("Perte")
plt.legend()


plt.savefig(
    "courbes_entrainement.png",
    dpi=150,
    bbox_inches="tight"
)

print("Courbes d'entraînement enregistrées.")