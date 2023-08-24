from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import User, Platform, Account
from .forms import UserForm, AccountForm, PlatformForm
from  django.utils.html import format_html
from django.contrib import messages




# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =  ["id","first_name", "last_name","user_name", "email","delete_button"]
    search_fields = ["first_name__startswith", "last_name__startswith"]
    form = UserForm
    add_form_template = 'admin/add_form_u_p.html'
    
    def save_form(self, request, form, change):
        user = form.save(commit=False)  # Get the User object from the form without saving it yet.
        create_user = user.create_user(user.first_name.lower(),user.last_name.lower())
        user_name = create_user["user_name"]
        new_password = create_user["password"]
        email = create_user["email"]

        # Assign the generated values to the form fields
        form.instance.user_name = user_name
        form.instance.password = new_password
        form.instance.email = email

        return super().save_form(request, form, change)

    def delete_button(self, obj):
        return format_html('<center><a class="btn" href="/admin/passwordManager/user/{}/delete/">Delete</a></center>', obj.id)

class PlatformAdmin(admin.ModelAdmin):
    list_display =  ["id","platform_name", "platform_link","token","instance_url","api_login_username","api_login_password", "accounts_created_on_platform","delete_button"]
    search_fields = ["platform_name__startswith"]
    form = PlatformForm
    add_form_template = 'admin/add_form_u_p.html'
    

    def accounts_created_on_platform(self,platform_id):
        return Account.objects.filter(platform=platform_id).count()
    
    accounts_created_on_platform.short_description = "accounts created on"

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/platform/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/platform/{}/delete/">Delete</a>', obj.id)


class AccountAdmin(admin.ModelAdmin):
    list_display =  ["id","platform", "user","user_id_on_platform","status"]
    list_filter = ["platform","status"]
    
    form = AccountForm
    add_form_template = 'admin/account/add_form.html'
    change_form_template ='admin/account/change_form.html'
    change_list_template = 'admin/account/change_list.html'

    def change_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/account/{}/change/">Change</a>', obj.id)

    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/passwordManager/account/{}/delete/">Delete</a>', obj.id)
    
    def save_form(self, request: Any, form: Any, change: Any) -> Any:  
        platforms = form.cleaned_data['platforms']
        user = form.cleaned_data['user']

        for p in platforms[:len(platforms)-1]: # negative indexing isn't supported so changing to [:-1] won't work
            account_on_platform = Account.create_account(platform=p, user=user)
            if account_on_platform is not False:
                Account.objects.create( platform= p ,user= user, user_id_on_platform = Account.get_user_id(p, user))
            else :
                messages.error("account on {p} failed to be created")

        p = platforms[len(platforms)-1] 
        account_on_platform =  Account.create_account(platform=p, user=user)
        if  account_on_platform is not False:
            form.instance.platform = p
            form.instance.user_id_on_platform = Account.get_user_id(p , user)
        else :
            messages.error("account on {p} failed to be created")
        return super().save_form(request, form, change)
    
    def render_change_form(self, request: Any, context: Any, add: bool = ..., change: bool = ..., form_url: str = ..., obj: Any | None = ...) -> Any:
        context["platformCount"] = Platform.objects.all().count()
        context["current_account"] = obj
        if obj != None :
            context["user_id"]= obj.user.pk
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        if Account.deactivate_account(obj,obj.platform, obj.user) != False:
            obj.status = False
            obj.save()
            user = User.objects.get(pk = 23)
            platform = Platform.objects.get(pk = 18)
            obj = Account.objects.create(platform = platform, user = user)
        return super().delete_model(request, obj)

        
    
admin.site.register(User, UserAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.disable_action('delete_selected')
