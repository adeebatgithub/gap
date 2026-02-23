from django import forms

from academics.models import SubjectClass, Teacher, SchoolClass, Subject


class SubjectClassForm(forms.ModelForm):
    class Meta:
        model = SubjectClass
        fields = ('teacher', 'school_class', 'subject')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.select_related('user').order_by('user__first_name')
        self.fields['school_class'].queryset = SchoolClass.objects.order_by('name')
        self.fields['subject'].queryset = Subject.objects.order_by('name')
