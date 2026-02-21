from django import forms
from django.contrib.auth import get_user_model
from academics.models import Teacher

User = get_user_model()

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Teacher
        fields = []

    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.get('instance').user if kwargs.get('instance') else None
        super().__init__(*args, **kwargs)
        if self.instance_user:
            self.fields['first_name'].initial = self.instance_user.first_name
            self.fields['last_name'].initial = self.instance_user.last_name
            self.fields['email'].initial = self.instance_user.email

    def save(self, commit=True):
        teacher = super().save(commit=False)
        if self.instance_user:
            user = self.instance_user
        else:
            user = User()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            teacher.user = user
            teacher.save()
        return teacher