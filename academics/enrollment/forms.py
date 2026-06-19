from django import forms

from academics.enrollment.models import Student
from academics.schoolclass.models import SchoolClass


class EnrollmentForm(forms.ModelForm):
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all())

    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
        }


class StudentImportForm(forms.Form):
    file = forms.FileField(
        label="Excel File",
        help_text="Upload .xlsx file with student data.",
        widget=forms.FileInput(attrs={"accept": ".xlsx"}),
    )

    def clean_file(self):
        file = self.cleaned_data["file"]
        if not file.name.endswith(".xlsx"):
            raise forms.ValidationError("Only .xlsx files are supported.")
        if file.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("File too large (max 5MB).")
        return file
