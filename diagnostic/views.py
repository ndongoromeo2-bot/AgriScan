import os

import numpy as np
import tensorflow as tf

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from tensorflow.keras.preprocessing import image

from .forms import ImageSolForm


# Chargement du modèle d'intelligence artificielle
CHEMIN_MODELE = os.path.join(
    settings.BASE_DIR,
    "modele_fertilite_sol.h5"
)

model = tf.keras.models.load_model(CHEMIN_MODELE)

# Seuil indicatif pour signaler un résultat incertain
SEUIL_FIABLE = 70

# Conseils affichés selon la classe prédite
CONSEIL_FERTILE = (
    "Ce sol présente des caractéristiques visuelles associées "
    "à un sol fertile. Vérifiez néanmoins son pH et ses nutriments "
    "(azote, phosphore et potassium) par une analyse en laboratoire."
)

CONSEIL_PAUVRE = (
    "Ce sol présente des caractéristiques visuelles associées "
    "à un sol potentiellement pauvre. Un apport de compost ou de fumier "
    "peut être envisagé. Faites confirmer le diagnostic par une analyse "
    "en laboratoire."
)


def analyser_sol(request):

    contexte = {
        "form": ImageSolForm()
    }

    if request.method == "POST":

        form = ImageSolForm(request.POST, request.FILES)
        contexte["form"] = form

        if form.is_valid():

            photo = form.cleaned_data["image"]

            fs = FileSystemStorage()

            nom_fichier = fs.save(photo.name, photo)

            chemin_complet = fs.path(nom_fichier)

            try:
                # Charger et redimensionner la photo
                img = image.load_img(
                    chemin_complet,
                    target_size=(224, 224)
                )

                # Normaliser les pixels et ajouter la dimension du lot
                img_array = np.expand_dims(
                    image.img_to_array(img) / 255.0,
                    axis=0
                )

                # Effectuer la prédiction
                prediction = float(
                    model.predict(img_array, verbose=0)[0][0]
                )

            except Exception:
                fs.delete(nom_fichier)

                form.add_error(
                    "image",
                    "L'image n'a pas pu être lue. Essayez une autre photo."
                )

            else:

                # Classe 0 = fertile ; classe 1 = non fertile
                est_fertile = prediction < 0.5

                score_indicatif = round(
                    (1 - prediction if est_fertile else prediction) * 100,
                    1
                )

                contexte.update({
                    "resultat": True,
                    "est_fertile": est_fertile,
                    "statut": (
                        "Sol Fertile"
                        if est_fertile
                        else "Sol Non Fertile"
                    ),
                    "confiance": score_indicatif,
                    "largeur": int(round(score_indicatif)),
                    "fiable": score_indicatif >= SEUIL_FIABLE,
                    "conseil": (
                        CONSEIL_FERTILE
                        if est_fertile
                        else CONSEIL_PAUVRE
                    ),
                    "image_url": fs.url(nom_fichier),
                })

    return render(
        request,
        "diagnostic/index.html",
        contexte
    )