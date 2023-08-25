from django.db import models
from django import forms
from .loggers import *


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, unique=True) # might change this to platform table instead
    email = models.EmailField(max_length=255, blank=True, default="None")
    password = models.CharField(max_length=255) 

    def __str__(self) -> str:
        return "{} {} (id={})".format(self.first_name, self.last_name, self.pk)

    def generate_password(self): 
        return "Agadir414$"

    def create_user(self, first_name, last_name):
        new_password = self.generate_password()
        user_name = first_name + "." + last_name
        email = user_name + "@infodat.ma"
        return {"password":new_password, "user_name":user_name, "email":email}
    
    def clean(self) -> None:
        if not self.first_name.isalpha():
            raise forms.ValidationError("First name must only have letters!")
        
        if not self.last_name.isalpha():
            raise forms.ValidationError("Last name must only have letters!")
        
        username = self.first_name + "." + self.last_name
        if User.objects.filter(user_name__iexact=username).exists():
            raise forms.ValidationError("user name already exists") 
        
        return super().clean()
    
    

    

class Platform(models.Model):
    platform_name = models.CharField(max_length=255)
    platform_link = models.URLField(max_length=200)
    instance_url = models.URLField(max_length=200, default = None, blank=True )
    token = models.CharField(max_length=250, default=None, blank=True)
    api_login_username = models.CharField(max_length=250, blank=True, default="None")
    api_login_password = models.CharField(max_length=250, blank=True, default="None")

    def __str__(self) -> str:
        return "{}".format(self.platform_name)
    
    def clean(self) -> None: #cleans and check if the input is properly formated before saving the form
        if (self.instance_url != "") :
            if (self.instance_url[-1]=="/"):
                self.instance_url = self.instance_url[:-1]

        self.platform_name = self.platform_name.lower().strip()

        if Platform.objects.filter(platform_name__iexact=self.platform_name, platform_link__iexact=self.platform_link).exists():
            raise forms.ValidationError("platform already exists") 

        return super().clean()


class Account(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.BooleanField(default=True) #active or deactivated
    user_id_on_platform = models.CharField(max_length=250, default=None, blank=True)

    def account_already_exists(self, user, platform):
        return Account.objects.filter(user=user, platform=platform).exists()
    
    def create_account(platform ,user): # calls the right logger to create the account on the platform
        if platform.platform_name == 'gitlab':
            logger = GitlabLogger(url=platform.instance_url, token = platform.token, id="", password="")
        elif platform.platform_name == 'mattermost':
            logger = MatterMostLogger(url=platform.instance_url, token = platform.token,id="", password="")
        elif platform.platform_name == 'harbor':
            logger = HarborLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        elif platform.platform_name == 'minio':
            logger = MinioLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        else :
            raise forms.ValidationError("the platfrom", platform.platform_name ,"selected has no configured logger")
        
        try :
            return logger.create_user(email=user.email, user_name=user.user_name, name=user.first_name +" "+user.last_name, password=user.password)
        except :
            return False
        
    def deactivate_account(account,platform, user):
        if platform.platform_name == 'gitlab':
            logger = GitlabLogger(url=platform.instance_url, token = platform.token, id="", password="")
        elif platform.platform_name == 'mattermost':
            logger = MatterMostLogger(url=platform.instance_url, token = platform.token,id="", password="")
        elif platform.platform_name == 'harbor':
            logger = HarborLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        elif platform.platform_name == 'minio':
            logger = MinioLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        else :
            raise forms.ValidationError("the platfrom", platform.platform_name ,"selected has no configured logger")
        
        try :
            return logger.block_user(id=account.user_id_on_platform, user_name=user.user_name)
        except :
            return False
    
    def activate_account(account,platform, user):
        if platform.platform_name == 'gitlab':
            logger = GitlabLogger(url=platform.instance_url, token = platform.token, id="", password="")
        elif platform.platform_name == 'mattermost':
            logger = MatterMostLogger(url=platform.instance_url, token = platform.token,id="", password="")
        elif platform.platform_name == 'harbor': # action imposible on harbor
            logger = HarborLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        elif platform.platform_name == 'minio':
            logger = MinioLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        else :
            raise forms.ValidationError("the platfrom", platform.platform_name ,"selected has no configured logger")
        
        try :
            return logger.unblock_user(id=account.user_id_on_platform, user_name=user.user_name)
        except :
            return False
    
    def get_all_users(platform):
        if platform.platform_name == 'gitlab':
            logger = GitlabLogger(url=platform.instance_url, token = platform.token, id="", password="")
        elif platform.platform_name == 'mattermost':
            logger = MatterMostLogger(url=platform.instance_url, token = platform.token,id="", password="")
        elif platform.platform_name == 'harbor':
            logger = HarborLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        elif platform.platform_name == 'minio':
            logger = MinioLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        else :
            raise forms.ValidationError("the platfrom", platform.platform_name ,"selected has no configured logger")
        
        try :
            return logger.get_users()
        except :
            return False
        
    def get_user_id(platform ,user): # calls the right logger to create the account on the platform
        if platform.platform_name == 'gitlab':
            logger = GitlabLogger(url=platform.instance_url, token = platform.token, id="", password="")
        elif platform.platform_name == 'mattermost':
            logger = MatterMostLogger(url=platform.instance_url, token = platform.token,id="", password="")
        elif platform.platform_name == 'harbor':
            logger = HarborLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        elif platform.platform_name == 'minio':
            logger = MinioLogger(url=platform.instance_url, token = "", id = platform.api_login_username, password = platform.api_login_password)
        else :
            raise forms.ValidationError("the platfrom", platform.platform_name ,"selected has no configured logger")
        
        try :
            return logger.get_user_id(user_name=user.user_name)
        except :
            return None
