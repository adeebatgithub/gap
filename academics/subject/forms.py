from django import forms
from academics.subject.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name', 'code')