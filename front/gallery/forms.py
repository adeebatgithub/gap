# forms.py
from django import forms
from front.models import Gallery


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["image", "position"]

    def clean_position(self):
        position = self.cleaned_data["position"]
        if position == Gallery.IN_HOME_PAGE and Gallery.objects.filter(position=Gallery.IN_HOME_PAGE).count() == 5:
            self.add_error("position", forms.ValidationError("only 5 images are allowed in home page"))
        return position