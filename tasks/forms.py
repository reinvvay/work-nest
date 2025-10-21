from django import forms
from django.utils import timezone

from tasks.models import Task


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "deadline": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "priority": forms.Select(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "task_type": forms.Select(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
            "assignees": forms.SelectMultiple(attrs={
                "class": "w-full p-3 rounded bg-gray-850 text-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-700"
            }),
        }

    def clean_deadline(self) -> str | None:
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.now():
                raise forms.ValidationError("The deadline cannot be in the past.")
        return deadline
