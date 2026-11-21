import numpy as np

from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing import image


# 1. CHARGER LE MODELE

m = load_model("../modele_fertilite_sol.h5")


# 2. CHARGER LA PHOTO

img = image.load_img(
    "test.jpg",
    target_size=(224, 224)
)


# 3. PREPARER L'IMAGE

x = np.expand_dims(
    image.img_to_array(img) / 255.0,
    axis=0
)


# 4. EFFECTUER LA PREDICTION

prediction = float(m.predict(x, verbose=0)[0][0])


# 5. AFFICHER LE RESULTAT

print("\n===== RESULTAT AGRISCAN =====")

print("Valeur prédite :", prediction)

if prediction < 0.5:

    print("Diagnostic : SOL FERTILE")

else:

    print("Diagnostic : SOL NON FERTILE")

print("============================")