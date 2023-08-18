from django.urls import path, include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('admin/passwordManager/account/add/', fetch_platform_with_existing_accounts, name="fetch_platforms"),
]

admin.site.site_header  =  "Credentials Manager"  
admin.site.site_title  =  "Credentials Manager"
admin.site.index_title  =  "Credentials Manager"