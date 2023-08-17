from typing import Any, Optional
from django.contrib import admin
from django.forms.fields import TypedChoiceField
from .models import User, Platform, Account
from .forms import UserForm, AccountForm
from  django.utils.html import format_html
from django.db.models  import Subquery


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =  ["id","first_name", "last_name","user_name", "change_button","delete_button"]
    search_fields = ["first_name__startswith", "last_name__startswith"]
    form = UserForm
    
    def save_form(self, request, form, change):
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
    list_display =  ["id","platform_name", "platform_link", "accounts_created_on_platform","token","instance_url","change_button","delete_button"]
    search_fields = ["platform_name__startswith"]

    def accounts_created_on_platform(self,platform_id):
        return Account.objects.filter(platform=platform_id).count()
    
    accounts_created_on_platform.short_description = "accounts"

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/platform/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/platform/{}/delete/">Delete</a>', obj.id)
            

class AccountAdmin(admin.ModelAdmin):
    list_display =  ["id","platform", "user","status","delete_button"]
    form = AccountForm
    add_form_template = 'admin/account/add_form.html'

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/account/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/account/{}/delete/">Delete</a>', obj.id)
    
    def save_form(self, request: Any, form: Any, change: Any) -> Any:  
        platforms = form.cleaned_data['platforms']
        user = form.cleaned_data['user']
        if platforms:
            for p in platforms[:len(platforms)-1]:
                Account.objects.create( platform= p ,user= user)
            form.instance.platform = platforms[len(platforms)-1]  
        return super().save_form(request, form, change)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs) -> TypedChoiceField:
        if db_field.name == 'user':  
            Platform_count = Platform.objects.all().count()
            existing_user_ids = Account.objects.values_list('user')
            if existing_user_ids.count() == Platform_count:
                kwargs['queryset'] = User.objects.exclude(pk__in=Subquery(existing_user_ids))
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def render_change_form(self, request: Any, context: Any, add: bool = ..., change: bool = ..., form_url: str = ..., obj: Any | None = ...) -> Any:
        context["platformCount"] = Platform.objects.all().count()
        return super().render_change_form(request, context, add, change, form_url, obj)

    
    
admin.site.register(User, UserAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Account, AccountAdmin)