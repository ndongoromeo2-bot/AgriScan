(function () {
    const entree = document.getElementById("id_image");
    const nom = document.getElementById("nom_fichier");
    const apercu = document.getElementById("apercu");
    const image = document.getElementById("apercu_img");
    const bouton = document.getElementById("btn_analyser");
    const formulaire = document.getElementById("formulaire");
    const message = document.getElementById("erreur_js");

    const TAILLE_MAX = 8 * 1024 * 1024; // 8 Mo

    // Vérifier que les éléments HTML existent
    if (!entree || !nom || !apercu || !image ||
        !bouton || !formulaire || !message) {
        console.error("Erreur : certains éléments AgriScan sont introuvables.");
        return;
    }

    function afficherErreur(texte) {
        message.textContent = texte;
        message.hidden = !texte;
    }

    function reinitialiser() {
        nom.textContent = "Aucune photo sélectionnée";
        apercu.classList.remove("visible");
        image.removeAttribute("src");
        bouton.disabled = true;
    }

    // Lorsqu'une photo est sélectionnée
    entree.addEventListener("change", function () {
        afficherErreur("");

        const fichier = entree.files[0];

        if (!fichier) {
            reinitialiser();
            return;
        }

        // Vérifier le format
        if (!["image/jpeg", "image/png"].includes(fichier.type)) {
            entree.value = "";
            reinitialiser();
            afficherErreur("Format invalide : choisissez une image JPG ou PNG.");
            return;
        }

        // Vérifier la taille
        if (fichier.size > TAILLE_MAX) {
            entree.value = "";
            reinitialiser();
            afficherErreur("Photo trop lourde : 8 Mo maximum.");
            return;
        }

        // Afficher le nom du fichier
        nom.textContent = "Fichier : " + fichier.name;

        // Afficher l'aperçu
        const ancienneImage = image.dataset.objectUrl;

        if (ancienneImage) {
            URL.revokeObjectURL(ancienneImage);
        }

        const url = URL.createObjectURL(fichier);
        image.src = url;
        image.dataset.objectUrl = url;

        apercu.classList.add("visible");

        // Activer le bouton
        bouton.disabled = false;
    });

    // Lors de l'envoi du formulaire
    formulaire.addEventListener("submit", function (e) {

        if (!entree.files.length) {
            e.preventDefault();

            afficherErreur(
                "Veuillez prendre ou choisir une photo avant d'analyser."
            );

            return;
        }

        bouton.disabled = true;
        bouton.classList.add("charge");

        bouton.querySelector(".texte").textContent =
            "Analyse en cours...";
    });

})();