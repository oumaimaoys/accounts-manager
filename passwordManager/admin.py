from typing import Any
from django.contrib import admin
from .models import User, Platform, Account, UserForm, AccountForm
from  django.utils.html import format_html


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =  ["id","first_name", "last_name","user_name", "password", "change_button","delete_button"]
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
    
    def change_button(self, obj):
        return format_html('<center><a class="btn" href="/admin/passwordManager/user/{}/change/">Change</a></center>', obj.id)

    def delete_button(self, obj):
        return format_html('<center><a class="btn" href="/admin/passwordManager/user/{}/delete/">Delete</a></center>', obj.id)


class PlatformAdmin(admin.ModelAdmin):
    list_display =  ["id","platform_name", "platform_link", "accounts_created_on_platform","change_button","delete_button"]
    search_fields = ["platform_name__startswith"]
    def accounts_created_on_platform(self,platform_id):
        return Account.objects.filter(platform=platform_id).count()
    
    accounts_created_on_platform.short_description = "accounts"

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/platform/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/platform/{}/delete/">Delete</a>', obj.id)
    

         

class AccountAdmin(admin.ModelAdmin):
    list_display =  ["id","platform", "user","change_button","delete_button"]
    form = AccountForm

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/account/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/account/{}/delete/">Delete</a>', obj.id)
    
    def save_form(self, request: Any, form: Any, change: Any) -> Any:
        for p in form.cleaned_data["platforms"]:
            account = form.save(commit=False)
            form.instance.platform =  p

        
admin.site.register(User, UserAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Account, AccountAdmin)