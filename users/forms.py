from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    terms_accepted = forms.BooleanField(required=True, label="I accept the Terms and Conditions")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        terms = cleaned_data.get("terms_accepted")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if not terms:
            raise forms.ValidationError("You must accept the terms and conditions.")

        return cleaned_data
