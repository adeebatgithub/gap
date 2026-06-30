from django import forms

from .models import Assessment
from academics.subject.models import Subject, SubjectClass
from academics.schoolclass.models import SchoolClass


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['subject_class'].queryset = SubjectClass.objects.filter(
            teacher__user=user
        ).order_by('subject__name')


class AssessmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }