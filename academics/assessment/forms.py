from django import forms

from .models import Assessment
from academics.subject.models import Subject
from academics.schoolclass.models import SchoolClass


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['subject', 'school_class', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.order_by('name')
        self.fields['school_class'].queryset = SchoolClass.objects.order_by('name')


class AssessmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['subject', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.order_by('name')