from django.contrib import admin
from django import forms
from .models import User, Platform, Account
from django.shortcuts import get_object_or_404

# Register your models here.
class UserForm():
    pass

class UserAdmin(admin.ModelAdmin):
    list_display =  ["id","first_name", "last_name","user_name", "password"]
    fields = ["first_name","last_name"]

    def get_form(self, request, obj=None, **kwargs):
        # Get the default form.
        form = super().get_form(request, obj, **kwargs)


        return form


class PlatformAdmin(admin.ModelAdmin):
    list_display =  ["id","platform_name", "platform_link", "accounts_created_on_platform"]

    def accounts_created_on_platform(self,platform_id):
        return Account.objects.filter(platform=platform_id).count()
         

class AccountAdmin(admin.ModelAdmin):
    list_display =  ["id","platform", "user"]

    def format_user_name(self):# shows first name - last name  (id) in user column
        
        first_name = get_object_or_404(User, pk = id)["first_name"]
        last_name = get_object_or_404(User, pk =id)["last_name"]
        return ("%s %s (%d)" % first_name % last_name % id)

    def format_platform_name(): # shows platformName (id) in platform column
        pass


admin.site.register(User, UserAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Account, AccountAdmin)