from .models import User, Account, Platform
from django import forms
from django.forms import ModelForm

# model Forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields= ["first_name", "last_name"]
        widgets = {'user_name': forms.HiddenInput(), 'password':forms.HiddenInput()}


class AccountForm(ModelForm):
    platforms = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Platform.objects.all())
    #select_all_checkbox = forms.BooleanField(required = False,label = 'Select all platforms')

    class Meta:
        model = Account
        fields = '__all__'
        exclude = ["status"]
        widgets = {'platform' : forms.HiddenInput()}

    def select_all_platforms(): # this might get done in js instead
        pass

    def clean_all_platforms():
        pass