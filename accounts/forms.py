from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    ValidationError
)

from tasks.models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "email")

    def clean_email(self) -> str | None:
        email = self.cleaned_data.get("email")
        if Worker.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


class WorkerAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Worker
        fields = ("username", "password")


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "username", "email", "position"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "username": forms.TextInput(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "position": forms.Select(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
        }
