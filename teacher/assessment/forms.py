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

    def clean_mark(self):
        mark = self.cleaned_data['mark']
        if int(mark) <= 0:
            raise forms.ValidationError("Mark cannot be less than 0")
        return mark


class AssessmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }