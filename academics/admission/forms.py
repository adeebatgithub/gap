from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import Admission

phone_validator = RegexValidator(
    regex=r'^(\+91|91)?[6-9]\d{9}$',
    message='Enter a valid Indian phone number.'
)

pincode_validator = RegexValidator(
    regex=r'^[1-9][0-9]{5}$',
    message='Enter a valid Indian PIN code.'
)


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if len(full_name.strip()) < 2:
            raise ValidationError("Full name must be at least 2 characters long.")

        return full_name.title()

    def clean_guardian_name(self):
        guardian_name = self.cleaned_data.get("guardian_name")
        if len(guardian_name.strip()) < 2:
            raise ValidationError("Guardian name must be at least 2 characters long.")

        return guardian_name.title()

    def clean_post(self):
        post = self.cleaned_data.get("post")
        return post.title()

    def clean_district(self):
        district = self.cleaned_data.get("district")
        return district.title()

    def clean_state(self):
        state = self.cleaned_data.get("state")
        return state.title()

    def clean_mother_tongue(self):
        mother_tongue = self.cleaned_data.get("mother_tongue")
        return mother_tongue.title()

    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob >= date.today():
            raise ValidationError("Date of birth must be in the past.")

        age = date.today().year - dob.year
        if age < 13:
            raise ValidationError("Age must be at least 13 years.")

        return dob

    def clean_pincode(self):
        pincode = self.cleaned_data.get("pincode")
        pincode_validator(pincode)
        return pincode

    def clean_phone_1(self):
        phone = self.cleaned_data.get("phone_1")
        phone_validator(phone)
        return phone

    def clean_phone_2(self):
        phone = self.cleaned_data.get("phone_2")
        if phone:
            phone_validator(phone)

        return phone

    def clean(self):
        cleaned_data = super().clean()

        phone_1 = cleaned_data.get("phone_1")
        phone_2 = cleaned_data.get("phone_2")

        if phone_1 and phone_2 and phone_1 == phone_2:
            self.add_error("phone_1",
                "Primary and secondary phone numbers cannot be the same."
            )

        return cleaned_data
