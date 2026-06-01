from django import forms
from front.models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('title', 'content', 'file')