from django import forms
from academics.admission.models import Admission


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"