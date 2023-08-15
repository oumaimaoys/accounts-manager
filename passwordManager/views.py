from django.shortcuts import render
from models import Account, AccountForm
from django.views.generic.edit import CreateView, FormView


# Create your views here.

class AccountFormView(FormView):
    model = Account
    template_name = "admin/add_form.html"
    form = AccountForm

