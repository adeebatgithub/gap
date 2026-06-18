from django import forms
from academics.schoolclass.models import SchoolClass
from teacher.teacher.models import Teacher


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ('name', 'class_teacher', 'parent')
        widgets = {
            'name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_teacher'].queryset = Teacher.objects.all().select_related("user")
        self.fields['parent'].label = "under"