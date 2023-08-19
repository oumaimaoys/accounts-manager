from django.db import models



# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255) # might change this to platform table instead
    # email 
    password = models.CharField(max_length=255) 

    def __str__(self) -> str:
        return "{} {} (id={})".format(self.first_name, self.last_name, self.pk)

    def generate_password(self): 
        return "Agadir414$"

    def create_user(self, first_name, last_name):
        new_password = self.generate_password()
        user_name = first_name + "." + last_name
        return {"password":new_password, "user_name":user_name}
    
    def validate_credentials(self):
        pass
    

class Platform(models.Model):
    platform_name = models.CharField(max_length=255)
    platform_link = models.URLField(max_length=200)
    instance_url = models.URLField(max_length=200, default = None, blank=True )
    token = models.CharField(max_length=250, default=None, blank=True)
    #api_login_username = models.CharField(max_length=250, default=None, blank=True)
    #api_login_password = models.CharField(max_length=250, default="None")

    def __str__(self) -> str:
        return "{}".format(self.platform_name)


class Account(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.BooleanField(default=True) #active or deactivated
    # id of user on that plattform

    def account_already_exists(self, u, p):
        return Account.objects.filter(user=u, platform=p).exists()
    


    