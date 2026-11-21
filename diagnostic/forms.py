from django import forms


class ImageSolForm(forms.Form):

    image = forms.ImageField(
        label="Photo du sol",
        error_messages={
            "required": "Veuillez sélectionner une image.",
            "invalid": "Le fichier sélectionné n'est pas une image valide."
        }
    )

    def clean_image(self):
        image = self.cleaned_data.get("image")

        # Vérifier la taille : maximum 8 Mo
        if image.size > 8 * 1024 * 1024:
            raise forms.ValidationError(
                "La taille de l'image ne doit pas dépasser 8 Mo."
            )

        # Vérifier le format
        formats_autorises = ["JPEG", "PNG"]

        if image.image.format not in formats_autorises:
            raise forms.ValidationError(
                "Format non autorisé. Utilisez une image JPG ou PNG."
            )

        return image