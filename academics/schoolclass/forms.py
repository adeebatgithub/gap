from django import forms
from academics.schoolclass.models import SchoolClass


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ('name', 'class_teacher')
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }