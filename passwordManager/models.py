from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def create_new_user(self): #autogenerates credentials
        pass




class Platform(models.Model):
    platform_name = models.CharField(max_length=255)
    platform_link = models.CharField(max_length=255)


class Accounts(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


"""class Admins(models.Model):
    pass"""