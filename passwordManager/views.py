from django.shortcuts import render
from models import Account, AccountForm
from django.views.generic.edit import CreateView


# Create your views here.

class AccountFormView(CreateView):
    model = Account
    template_name = "templates/admin/add_view.html"
    form = AccountForm

