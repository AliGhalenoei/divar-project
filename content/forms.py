from django import forms
from accounts.models import UserProfile



class SearchAdvertisementForm(forms.Form):
    search = forms.CharField(label='search')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)


