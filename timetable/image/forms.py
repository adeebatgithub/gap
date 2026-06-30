from django import forms
from timetable.models import TimetableImage


class TimetableImageForm(forms.ModelForm):
    class Meta:
        model = TimetableImage
        fields = ['day', 'image']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }