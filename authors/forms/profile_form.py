from django import forms
from authors.models import Profile
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')

        if len(bio) < 6:
            raise ValidationError(
                'A bio deve ter no minímo 5 caracteres',
                code='invalid'
            )
        
        return bio
