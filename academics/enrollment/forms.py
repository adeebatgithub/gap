from django import forms

from academics.models import Student, SchoolClass, Enrollment


class EnrollmentForm(forms.ModelForm):
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all())

    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
        }
