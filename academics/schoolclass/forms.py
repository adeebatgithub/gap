from django import forms
from academics.models import SchoolClass


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }