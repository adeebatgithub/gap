from django import forms

from academics.models import Enrollment, Student, SchoolClass, AcademicYear


class EnrollmentForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Enrollment
        fields = ('school_class', )

    def __init__(self, *args, **kwargs):
        self.instance_student = kwargs.get('instance').student if kwargs.get('instance') else None
        super().__init__(*args, **kwargs)
        if self.instance_student:
            self.fields['name'].initial = self.instance_student.name

    def save(self, commit=True):
        enrollment = super().save(commit=False)
        if self.instance_student:
            student = self.instance_student
        else:
            student = Student()
        student.name = self.cleaned_data['name']
        if commit:
            student.save()
            enrollment.student = student
            enrollment.save()
        return enrollment
