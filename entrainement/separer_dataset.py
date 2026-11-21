import os
import random
import shutil

SOURCE = "dataset_brut"
DEST = "dataset"

RATIO_VAL = 0.2

random.seed(42)

for classe in ("fertile", "non_fertile"):

    dossier = os.path.join(SOURCE, classe)

    fichiers = [
        f for f in os.listdir(dossier)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    random.shuffle(fichiers)

    n_val = int(len(fichiers) * RATIO_VAL)

    parts = {
        "val": fichiers[:n_val],
        "train": fichiers[n_val:]
    }

    for nom, liste in parts.items():

        cible = os.path.join(DEST, nom, classe)

        os.makedirs(cible, exist_ok=True)

        for f in liste:
            shutil.copy(
                os.path.join(dossier, f),
                os.path.join(cible, f)
            )

    print(
        classe,
        ":",
        len(fichiers),
        "images",
        "(validation :",
        n_val,
        ")"
    )

print("Séparation terminée !")