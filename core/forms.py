from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'wage', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }
