from django.db import models
from django import forms
from django.forms import ModelForm

import random
import string
import bcrypt

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255) # might change this to platform table instead
    # email 
    password = models.CharField(max_length=255) # hashed password

    def __str__(self) -> str:
        return "{} {} (id={})".format(self.first_name, self.last_name, self.pk)

    def generate_password(self, password_length): #autogenerates credentials
        password = []
        character_list_alpha = string.ascii_letters
        character_list_num = string.digits
        character_list_punc = string.punctuation

        while(len(password) != password_length):
            if random.random() < 1/4 :
                password.append(random.choice(character_list_num))
            if random.random() < 1/4:
                password.append(random.choice(character_list_punc))
            if random.random() < 1/2 :
                password.append(random.choice(character_list_alpha))

        return ''.join(password)
    
    def hash_pasword(self, password):
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed_password
    
    def authenticate_password(self, input_password, hashed_password):
        password = input_password.encode('utf-8')
        if bcrypt.checkpw(password, hashed_password):
            return True
        else :
            raise ValueError("You entered the wrong password")

    def create_user(self, first_name, last_name):
        new_password = self.generate_password(20)
        hashed_password  = self.hash_pasword(new_password)
        user_name = first_name + "." + last_name
        return {"password":hashed_password, "user_name":user_name}
    


class UserForm(ModelForm):
   
    platforms = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=User.objects.all())
    fieldsets = [
        ( "persoanl info", {'fields':["first_name", "last_name"]}),
        ("platfroms", {'fields':["platforms"]})
    ]
    
    your_checkbox = forms.BooleanField(required = False,label = 'your_checkbox')
    class Meta:
        model = User
        fields= '__all__'
        widgets = {'user_name': forms.HiddenInput(), 'password':forms.HiddenInput()}

   
         
       

class Platform(models.Model):
    platform_name = models.CharField(max_length=255)
    platform_link = models.CharField(max_length=255)

    def __str__(self) -> str:
        return "{}".format(self.platform_name)


class Account(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)



"""class Admins(models.Model):
    pass"""