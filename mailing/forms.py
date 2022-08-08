from django import forms
from mailing.models import UserProfile

class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user']