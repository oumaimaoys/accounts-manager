from django.shortcuts import render
from .models import Account
from .forms import AccountForm
from django.views.generic.edit import CreateView


# Create your views here.

class AccountFormView(CreateView):
    model = Account
    template_name = "admin/add_form.html"
    form_class = AccountForm

