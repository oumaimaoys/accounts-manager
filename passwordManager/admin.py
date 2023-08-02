from django.contrib import admin
from .models import User, Platform, Accounts
# Register your models here.

class ManageUser(admin.ModelAdmin):
    list_display =  ["id","first_name", "last_name","user_name", "password"]

class ManagePlatform(admin.ModelAdmin):
    list_display =  ["id","platform_name", "platform_link", "accounts_created_on_platform"]

    def accounts_created_on_platform(self,platform_id):
        return Accounts.objects.filter(platform=platform_id).count()
         


class ManagerAccount(admin.ModelAdmin):
    list_display =  ["id","platform", "user"]

    def format_user_name():
        pass

    def format_platform_name():
        pass


admin.site.register(User, ManageUser)
admin.site.register(Platform, ManagePlatform)
admin.site.register(Accounts, ManagerAccount)