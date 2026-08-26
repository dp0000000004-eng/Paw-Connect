from django import forms
from .models import Students, FeedBack

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = [
            'description'
        ]

