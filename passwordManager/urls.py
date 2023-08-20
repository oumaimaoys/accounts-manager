from django.urls import path, include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('admin/passwordManager/account/add/', fetch_platform_with_existing_accounts, name="add_account_view"),
    path('admin/passwordManager/account/', change_status, name="acc_change_list_view"),
]

admin.site.site_header  =  "Credentials Manager"  
admin.site.site_title  =  "Credentials Manager"
admin.site.index_title  =  "Credentials Manager"