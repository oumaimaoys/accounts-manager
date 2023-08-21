from .models import User, Account, Platform
from django import forms
from django.forms import ModelForm

# model Forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields= ["first_name", "last_name"]
        widgets = {'user_name': forms.HiddenInput(), 'password':forms.HiddenInput(), 'email':forms.HiddenInput()}

class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class AccountForm(ModelForm):
    platforms = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Platform.objects.all())
    class Meta:
        model = Account
        fields = ["user","platforms"]
        widgets = {'platform' : forms.HiddenInput(), 'status' : forms.HiddenInput()}
