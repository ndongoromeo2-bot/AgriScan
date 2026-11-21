import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing.image import ImageDataGenerator


# 1. CHARGEMENT DU MODELE

model = load_model("modele_fertilite_sol.h5")


# 2. CHARGEMENT DES IMAGES DE VALIDATION

val = ImageDataGenerator(
    rescale=1.0 / 255
).flow_from_directory(
    "entrainement/dataset/val",
    target_size=(224, 224),
    batch_size=32,
    class_mode="binary",
    shuffle=False
)


# 3. PREDICTIONS DU MODELE

proba = model.predict(val).ravel()

pred = (proba >= 0.5).astype(int)


# 4. NOMS DES CLASSES

noms = ["fertile", "non_fertile"]


# 5. RAPPORT DE CLASSIFICATION

print("\n===== RAPPORT DE CLASSIFICATION =====")

print(
    classification_report(
        val.classes,
        pred,
        target_names=noms
    )
)


# 6. MATRICE DE CONFUSION

cm = confusion_matrix(
    val.classes,
    pred
)

affichage = ConfusionMatrixDisplay(
    cm,
    display_labels=noms
)

affichage.plot()

plt.title("Matrice de confusion - AgriScan")

plt.savefig(
    "matrice_confusion.png",
    dpi=150,
    bbox_inches="tight"
)

print("\nMatrice de confusion enregistrée.")
