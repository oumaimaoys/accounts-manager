from django.db import models
from django import forms
from django.forms import ModelForm


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255) # might change this to platform table instead
    # email 
    password = models.CharField(max_length=255) # hashed password

    def __str__(self) -> str:
        return "{} {} (id={})".format(self.first_name, self.last_name, self.pk)

    def generate_password(self): 
        return "Agadir414$"

    def create_user(self, first_name, last_name):
        new_password = self.generate_password(20)
        hashed_password  = self.hash_pasword(new_password)
        user_name = first_name + "." + last_name
        return {"password":hashed_password, "user_name":user_name}
    

class Platform(models.Model):
    platform_name = models.CharField(max_length=255)
    platform_link = models.URLField(max_length=200)
    instance_url = models.URLField(max_length=200, default = None, blank=True )
    token = models.CharField(max_length=250, default=None, blank=True)

    def __str__(self) -> str:
        return "{}".format(self.platform_name)


class Account(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    def account_already_exists(self, u, p):
        return Account.objects.filter(user=u, platform=p).exists()
    
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
        fields = ["user", "platforms"]
        widgets = {'platform' : forms.HiddenInput()}

    def select_all_platforms(): # this might get done in js instead
        pass

    def clean_all_platforms():
        pass

    