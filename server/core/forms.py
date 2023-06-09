from django import forms

# from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "name",
            "alt_name",
            "email",
            "alt_email",
            "phone_number",
            "alt_phone_number",
        )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "name",
            "alt_name",
            "email",
            "alt_email",
            "phone_number",
            "alt_phone_number",
            "is_superuser",
        )

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            "name",
            "alt_name",
            "email",
            "alt_email",
            "phone_number",
            "alt_phone_number",
            "is_superuser",
        )
