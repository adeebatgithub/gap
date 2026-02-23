from django import forms

from academics.models import Session, SchoolClass, Subject


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('date', 'school_class', 'subject')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school_class'].queryset = SchoolClass.objects.order_by('name')
        self.fields['subject'].queryset = Subject.objects.order_by('name')

class SessionUpdateForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('date', 'subject')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.order_by('name')



