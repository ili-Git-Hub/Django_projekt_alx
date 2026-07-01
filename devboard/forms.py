from django import forms

from devboard.models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'priority',
            'due_date',
            'assignee',
            'project',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    # dodatkowa walidacja - zadanie o wysokim priorytecie musi miec określony termin wykonania
    # celowo to wywolujemy
    def clean(self):
        cleaned = super().clean()
        priority = cleaned.get('priority')
        due_date = cleaned.get('due_date')
        if priority == Task.Priority.HIGH and not due_date:
            raise forms.ValidationError("Zadanie o wysokim piorytecie musi miec określony termin wykonania!")
        return cleaned