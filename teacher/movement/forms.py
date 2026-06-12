from django import forms

from teacher.teacher.models import Teacher
from .models import Movement


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ["date", "teacher", "start_time", "end_time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["teacher"].queryset = (
            Teacher.objects.select_related("user")
        )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "End time must be greater than start time."
            )

        return cleaned_data