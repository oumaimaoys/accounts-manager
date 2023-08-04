from django.contrib import admin
from .models import User, Platform, Account, UserForm
from django.shortcuts import get_object_or_404



# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =  ["id","first_name", "last_name","user_name", "password"]
    search_fields = ["first_name__startswith", "last_name__startswith"]
    form = UserForm

    def save_form(self, request, form, change):
        # Do some custom logic before saving the form.
        user = form.save(commit=False)  # Get the User object from the form without saving it yet.
        create_user = user.create_user(user.first_name.lower(),user.last_name.lower())
        user_name = create_user["user_name"]
        new_password = create_user["password"]

        # Assign the generated values to the form fields
        form.instance.user_name = user_name
        form.instance.password = new_password

        return super().save_form(request, form, change)
    


class PlatformAdmin(admin.ModelAdmin):
    list_display =  ["id","platform_name", "platform_link", "accounts_created_on_platform"]
    search_fields = ["platform_name__startswith"]
    def accounts_created_on_platform(self,platform_id):
        return Account.objects.filter(platform=platform_id).count()
    
    accounts_created_on_platform.short_description = "accounts"
         

class AccountAdmin(admin.ModelAdmin):
    list_display =  ["id","platform", "user"]



admin.site.register(User, UserAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Account, AccountAdmin)