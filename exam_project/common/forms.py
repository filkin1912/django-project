from django import forms
from exam_project.common.models import BoughtGame


class BoughtGameForm(forms.ModelForm):
    class Meta:
        model = BoughtGame
        fields = '__all__'
