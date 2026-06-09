from django import forms

from teacher.attendance.models import Session, SubjectClass
from academics.subject.models import Subject
from academics.schoolclass.models import SchoolClass


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('date', 'period', 'subject_class')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['subject_class'].queryset = SubjectClass.objects.filter(
            teacher__user=user
        ).order_by('subject__name')

    def clean_period(self):
        period = self.cleaned_data['period']
        if period and period > 10:
            raise forms.ValidationError("invalid option")
        return period


class SessionUpdateForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('date', 'period', 'subject_class')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['subject_class'].queryset = SubjectClass.objects.filter(
            teacher__user=user
        ).order_by('subject__name')
